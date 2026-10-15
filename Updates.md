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
