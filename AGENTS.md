## Scope
Code that generates figures, tables, and outputs for the manuscript.

## Workflow
- Prefer running existing `.sh` scripts that orchestrate `.py` scripts.
- If multiple scripts exist, ask which entrypoint to use.
- Avoid changing outputs or seeds unless requested.

## Conventions
- Keep changes minimal and localized.
- Document any new scripts or flags you add.
- Use concise colored step markers in shell scripts and prefer `tqdm` for long Python loops.
- Keep documentation up to date; if logic changes, update any related docs.

## Tests (manual)
- Test suite lives in `test/` with inputs/outputs under `test/data` and `test/output`.
- Run all tests with `test/run_tests.sh`.
- Add new tests by creating a `test_*.py` file and any needed small graph fixtures in `test/data`.
- Keep test output verbose (`unittest -v`) and document each test in `test/README.md` with inputs, outputs, entrypoint, and expected behavior.
