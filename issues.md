# Lab 5 — Issues Found and Fixed (`shuttle_system.py`)

Baseline: Pylint **6.25/10**, Bandit **2** issues (Low), Flake8 **10** issues.
Final: Pylint **10.00/10**, Bandit **0**, Flake8 **0**.

| # | Issue | Type | Tool / Code | Line(s) (original) | Description | Fix Approach |
|---|-------|------|-------------|--------------------|-------------|--------------|
| 1 | Bare `except: pass` | Bug / Security | Bandit B110, Pylint W0702, Flake8 E722 | 26–30 | Swallowed every exception. R3's `"full"` trip raised a TypeError that was silently ignored, so R3 vanished from the under-used report | Removed the try/except. `average_load` returns `None` for routes with no trips, and invalid data is rejected at input time |
| 2 | No input validation on passenger count | Bug (not flagged by tools) | — (found by running) | 11–14, 49–50 | `-6` and `"full"` were stored as trips, which corrupts averages (R2 showed `[4, -6]`) | `add_trip_log` raises `ValueError` for non-int, bool or negative counts and `KeyError` for unknown routes. `main` catches and reports the rejections |
| 3 | Use after delete | Bug (not flagged by tools) | — (runtime `KeyError`) | 55, 58 | `remove_route("R3")` ran before `average_load("R3")`, so the script crashed at the end | Print the R3 average before removing the route |
| 4 | Unchecked user input | Bug (not flagged by tools) | — (runtime `KeyError`) | 56–57 | Any route id other than R1–R3 crashed the lookup | Strip and upper-case the input, and print "No such route" when it isn't found |
| 5 | Mutable default argument | Bug | Pylint W0102 | 11 | `logs=[]` was shared across every call, so logs leaked between calls | Default to `None` and create a new list inside the function |
| 6 | Insecure / unneeded PRNG | Security (Low) | Bandit B311, Pylint W0613 | 33–35 | `random.choice` picked drivers and ignored `route_id`. Not crypto, but the assignment was nondeterministic and the argument was unused | Replaced with a fixed `DRIVER_ROSTER` lookup keyed by `route_id` |
| 7 | `global` reassignment | Design | Pylint W0603 | 38, 43 | `sync_fleet_data` rebound the global `routes` | Removed `global`; refresh the existing dict with `clear()` + `update()` |
| 8 | Files not closed safely / no encoding | Resource leak | Pylint R1732, W1514 | 39–43 | Manual open/close, the second file handle was never closed, and no encoding was given | `with open(..., encoding="utf-8")` plus `json.dump` / `json.load` |
| 9 | Function naming | Style | Pylint C0103 | 33 | `assignDriver` isn't snake_case | Renamed to `assign_driver` |
| 10 | Old-style formatting | Style | Pylint C0209 | 13 | `%` string formatting | Switched to f-strings |
| 11 | Missing docstrings | Documentation | Pylint C0114, C0116 | 1, all functions | No module or function docs | Added docstrings |
| 12 | Module-level `main()` call | Design | — | 60 | Importing the module runs the demo | Wrapped in an `if __name__ == "__main__":` guard |
| 13 | Blank lines between definitions | Style | Flake8 E302, E305 | 11–60 | One blank line instead of two | Two blank lines around top-level definitions |
| 14 | Line too long | Style | Flake8 E501 | 13 | 82 > 79 chars | Resolved by the f-string rewrite; long conditions are wrapped |

Commits: `Fix Bandit findings…` → `Fix Pylint findings…` → `Fix Flake8 PEP 8 findings`.
Reports: `reports/before/` and `reports/after/`.
