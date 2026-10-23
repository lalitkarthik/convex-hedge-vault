// promoted: 2026-10-23
// Watchdog for the implied against realised volatility orchestrator (feature #265). It is started outside the
// Claude desktop app, so an app restart no longer takes the build down with it. It resumes the
// orchestrator's SAME session on the max account and blocks until that turn ends; when the turn
// ends in a crash or a kill it resumes again, after a usage limit it waits and tries again, and
// it exits when the orchestrator ends its turn cleanly (finished, parked, or the PR left open)
// or after 4 crashes in a row.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const cx = await import(pathToFileURL(path.join(os.homedir(), '.claude', 'accounts', 'cx.mjs')).href);
const NAME = 'orch-iv-vs-rv';
const REC = path.join(os.homedir(), '.claude', 'accounts', 'runs', `${NAME}.json`);
const LOG = path.join(os.tmpdir(), 'feature-loop-orch-watch-iv-vs-rv.log');
const HANDOFF = 'C:/Users/Acer/AppData/Local/Temp/feature-loop-handoff-orchestrator-iv-vs-rv-20261007-1101.md';
const log = (m) => fs.appendFileSync(LOG, `${new Date().toISOString()} ${m}\n`);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const FIRST = 'Resume. Your process and every worker you started were killed at about 13:00 IST on 7 October 2026, '
  + 'when the Claude desktop app restarted: they were its children. Nothing had failed. You now run under a watchdog '
  + 'outside the app, on account max, and it resumes you if you stop. '
  + 'Docker Desktop is still answering; check `docker info` before any test run all the same, and if it is not running '
  + 'start it with `explorer.exe "C:\Users\Acer\AppData\Local\Programs\DockerDesktop\Docker Desktop.exe"`. '
  + `Read your state file and the hand-off ${HANDOFF} again; its rules are unchanged, including the owner's Account rule `
  + '(workers on accounts b and c through the account script, never a). '
  + 'The cx records of ticket-269 and ticket-271 still say running but no process exists, so do not wait for them. '
  + 'Both worktrees are clean and hold commits on their branches (three on ticket-269, four on ticket-271), so each '
  + 'worker may have been finished or close to it and had not replied. Restart each as loop step 7 says: a new worker '
  + 'in the same worktree, told to check its ticket against what is already committed, finish what is missing, run its '
  + 'checks and reply DONE. Then continue the loop. The pull request is opened and never merged.';
const AGAIN = (why) => `Resume. Your process stopped (${why}) and is resumed on account max. Read your state file and `
  + `the hand-off ${HANDOFF}, and continue from where the state file says you are. A worker whose cx record says `
  + 'running while no reply arrives was stopped with you: restart it as loop step 7 says, on the account the Account rule in the hand-off gives. '
  + 'Check `docker info` answers before any test run. The pull request is opened and never merged.';

let crashes = 0;
let text = FIRST;
log('watching (resume mode, account max)');
for (;;) {
  let rec;
  try { rec = JSON.parse(fs.readFileSync(REC, 'utf8')); } catch (e) { log(`read failed: ${e.message}`); await sleep(60_000); continue; }
  log(`resuming session ${rec.session} on ${rec.account}`);
  const code = cx.send(NAME, text); // blocks until this resumed turn ends
  try { rec = JSON.parse(fs.readFileSync(REC, 'utf8')); } catch { rec = {}; }
  const last = rec.last || {};
  const limited = code === 10 || last.exit === 10 || /usage limit|resume after|spent until|hit your .*limit/i.test(last.result || '');
  if (limited) {
    crashes = 0;
    log(`${NAME} stopped on a usage limit; trying again in 20 minutes`);
    text = AGAIN('a usage limit');
    await sleep(20 * 60_000);
    continue;
  }
  if (last.exit === 0) { log(`${NAME} ended its turn cleanly; done`); break; }
  if (++crashes > 4) { log(`${NAME} stopped (exit ${last.exit}) 4 times in a row; giving up`); break; }
  log(`${NAME} stopped (exit ${last.exit}); resuming in a minute`);
  text = AGAIN(`exit ${last.exit}`);
  await sleep(60_000);
}
