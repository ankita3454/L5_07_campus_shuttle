# Lab 5 — Reflection

**1. Which issues were the easiest to fix, and which were the hardest?**
The easiest were the Flake8 spacing issues, the snake_case rename, the f-strings and the docstrings. They are mechanical and don't change behaviour. The hardest was the bare `except: pass`. Deleting it is easy, but it was hiding real bugs (a string `"full"` and a negative count stored as trips). Fixing it properly meant adding validation at the input and deciding what `average_load` should return for a route with no trips. The `global` in `sync_fleet_data` also needed some thought: I refreshed the existing dict in place instead of rebinding it.

**2. Did the static analysis tools report any false positives? If so, describe one example.**
Bandit B311 is close to a false positive here. Choosing a shuttle driver has nothing to do with security, so a non-cryptographic PRNG is fine in principle. I still replaced it, because a fixed roster keyed by `route_id` is better design and also fixes Pylint's unused-argument warning. Otherwise, `# nosec B311` with a comment explaining why would have been reasonable. Pylint's missing-docstring warnings are also low-value on a script this small, but they are cheap to fix.

**3. How would you integrate static analysis tools into your actual software development workflow?**
I would run Flake8 and Pylint as a pre-commit hook so style problems never reach review, and run all three tools in CI (for example, a GitHub Actions job) that fails if Bandit reports anything Medium or above or Pylint drops below a threshold such as 9.5. I would also enable linting in the editor for instant feedback. Any suppressions (`# nosec`, `# pylint: disable`) should carry a comment explaining why.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**
Pylint went from 6.25 to 10.00, and Bandit and Flake8 both went to zero findings. More importantly, the program no longer crashes (it used to end in a `KeyError` on R3), rejects bad data instead of quietly corrupting averages, closes its files, and no longer shares a log list between calls. The tools did not catch three of the bugs: the use-after-delete, the missing input validation and the unchecked user lookup. I only found those by running the program, which shows that static analysis complements testing but does not replace it.
