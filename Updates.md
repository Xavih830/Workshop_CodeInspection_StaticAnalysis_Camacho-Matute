# Workshop 2 – Code Inspection: Project Updates Log

This document serves as an immutable chronological registry of all changes, refactoring steps, and static analysis fixes applied throughout the workshop. Each entry includes the date, a descriptive title, and the detailed content of the modification.

---

## [2026-10-15] Initial Project Setup and Baseline Verification

### Description
Configured the initial repository structure for static code analysis with SonarQube Cloud. Verified base application functionality and initialized tracking controls.

### Actions Taken
1. Added root-level `.gitignore` to prevent tracking runtime artifacts (`*.db`, `__pycache__/`, `*.pyc`).
2. Configured root-level `.sonarcloud.properties` targeting Python 3.12 and specifying `sonar.sources=bookstore`.
3. Executed baseline run of `bookstore/main.py` to capture baseline program execution output and observed runtime warning:
   - `database.py:62: SyntaxWarning: 'return' in a 'finally' block`
4. Created this `Updates.md` log file to record all subsequent modifications sequentially without overwriting previous history.

---

## [2026-10-15] Fix 1: Replace Identity Operator 'is' with Equality Operator '==' in Order Processing

### Description
Resolved SonarQube Reliability issue (rule `python:S5727`) in `bookstore/orders.py`.

### Context & Root Cause
In `bookstore/orders.py:11`, the empty order check used the identity operator `items is []`. In Python, testing identity against a newly instantiated list literal (`[]`) always evaluates to `False`, allowing empty item lists to bypass the guard clause.

### Changes Made
- Modified line 11 of `bookstore/orders.py`:
  - Replaced `if items is []:` with `if items == []:`.
- Verified that execution of `bookstore/main.py` remains functional and preserves expected behavior.

---

## [2026-10-15] Fix 2: Remove Redundant Branch with Identical Implementation in Coupon Handling

### Description
Resolved SonarQube Reliability issue (rule `python:S1871`) in `bookstore/orders.py`.

### Context & Root Cause
In `bookstore/orders.py:37`, the evaluation of the `STAFF` coupon code contained an `if/else` block where both the `if auth.is_admin(token):` and the `else:` branches executed the exact same statement (`total = total * 0.7`). This was a logic bug that granted the staff discount even to unauthorized users while creating redundant code branches.

### Changes Made
- Modified `bookstore/orders.py`:
  - Removed the duplicate `else:` branch under the `STAFF` coupon condition, ensuring that the discount is exclusively applied when `auth.is_admin(token)` evaluates to `True`.
- Verified that execution of `bookstore/main.py` remains functional and preserves expected behavior.


