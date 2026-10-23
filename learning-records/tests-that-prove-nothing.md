# Tests that prove nothing

Six of them in one epic. Here is how to find yours, in order of what it costs you.

## Do this first — 2 minutes

Pick any test that consumes from a queue, a stream or a buffer. Look for this shape:

```python
received = await take(subscription, 10)
assert len(received) == 10
```

That test is green with eleven items in the queue. **Drain to empty and assert empty.**

```python
received = await take(subscription, 10)
assert len(received) == 10
assert await drain(subscription) == []
```

That one correction fixed both halves of the worst defect found this epic.

## The five checks, ranked by what they caught

1. **Drain to empty.** A test that takes exactly what it expects is an assertion about a
   prefix. Duplicates live in the suffix. Cost of missing it: a restarted store folded its
   replay tail twice, inflating tick counts and leaving a position index of 20 against a
   stream of 15 entries.
2. **Run it, do not read it.** Four of the six were found by executing something — a
   `--help` probe, a trial migration on copied data, a full suite under load. Reading
   found two.
3. **Seed the regression back.** Put the wrong value in and watch the test fail. If it does
   not fail, it was never a test. Two minutes per test, and it is the only check that
   cannot be fooled.
4. **Assert against the narrowest text that can carry the value.** A compose test read the
   whole service block, comments included. The comment always named a ceiling, so prose
   satisfied it and the configuration was never read.
5. **Check that something can raise before you trust "nothing raised".** A bus that
   isolates reader failures by design turns every such test against it into a no-op.

## The six, in order

1. `migrate_store.py` had no `__main__` block. Run as a command it printed nothing, moved
   nothing, exited 0. **1,120 tests passed.**
2. `smoke_stack.py` had `main(argv)` then `del argv`, so every invocation — `--help`
   included — built six images and started six containers. **1,214 tests passed.**
3. `fakeredis` never returns the empty-result shape a real blocking `XREADGROUP` returns,
   so a flag that never cleared was invisible until the Docker parametrisation ran.
4. A compose test asserted `"1gb" in blocks["redis"]`. Satisfied by a comment. It passed
   unchanged when the real ceiling moved to 2gb.
5. A `BUSYGROUP` rejoin test had **no assertion at all**. Proved by making the call raise
   unconditionally: the test still passed.
6. A replay test took ten and asserted ten, while five duplicates sat behind it. Its
   sibling published nothing during the restart gap, so the over-read had nothing to
   over-read. Together they hid the blocker.

## What to do when you find the sixth

Stop fixing them one at a time. Add the scan:

```python
def test_every_test_in_this_module_has_an_assertion() -> None:
    """Fails if any test_* function has no Assert node and no raises call."""
```

It walks the module's AST, nested `async def scenario()` bodies included. Six instances in
one epic means the individual repairs are not keeping up with the rate they are written.

## Three mechanisms wore one symptom

"The suite is flaky under load" was three separate things, and only one of them was load.

1. **`--basetemp` with a missing parent.** pytest creates that directory with
   `parents=False`, so **315 tests error at setup**, are reported as *errors* rather than
   failures, and the run finishes **faster** because they never ran. Four agents read it as
   load and moved on.
2. **A shared test Redis container.** Two suites in two worktrees share one fixed container
   name and delete each other's stream keys.
3. **One genuine duration-bet.** A `time.sleep(0.6)` waiting for two 0.2 s passes of a loop
   running on another thread's event loop.

The repository's own verification command caused the first one: it prescribed the flag
*and* told every worker to delete the directory as its last command, so the next run was
always a first run.

**A ticket that closes on the wrong mechanism is worse than one left open**, because the
next person stops looking.

## Time estimates, measured

| Task | Time |
|---|---|
| Seed one regression and watch it fail | 2 minutes |
| Add the AST scan to one module | 15 minutes |
| Audit one file's tests by the five checks | 30 minutes |
| Fix a defect the checks find | an afternoon, if it is real |

## Later evidence — 2026-10-08

Check 3, made automatic. On the feature-experiments package (`convex-hedge-strategy`, local branch
`feature/feature-experiments`), a reviewer agent seeded 33 deliberate mistakes into the code. **19
got past the first test suite.** A test was added for each. Mutation by an agent finds what reading
the tests does not — the same lesson as check 3, at the scale of a whole package.

## Next action

Open the test file you touched most recently. Search it for `take(`, `sleep(`, and any test
whose body ends without `assert`. That is under two minutes and it is where yours will be.
