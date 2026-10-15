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

---

## [2026-10-15] Fix 3: Refactor process_order to Reduce Cognitive Complexity

### Description
Resolved SonarQube Maintainability issue (rule `python:S3776`) in `bookstore/orders.py`.

### Context & Root Cause
In `bookstore/orders.py:8`, `process_order` had a Cognitive Complexity score of 42 (exceeding the threshold of 15 allowed). This was caused by deeply nested conditional blocks, loops, stock availability checks, coupon evaluations, and shipping options inside a single monolithic function.

### Changes Made
- Decomposed `process_order` in `bookstore/orders.py`:
  - Inverted the session verification check to a guard clause (`if username == None:` early exit) to eliminate outer nesting.
  - Extracted cart item processing and inventory check logic into helper function `_process_cart_item(item)`.
  - Extracted coupon discount calculation into helper function `_apply_coupon(total, coupon, token)`.
  - Extracted shipping cost calculation into helper function `_apply_shipping(total, shipping)`.
- Reduced Cognitive Complexity of `process_order` from 42 to well below 15.
- Verified that execution of `bookstore/main.py` remains functional with identical outputs.

---

## [2026-10-15] Fix 4: Replace Insecure MD5 Hashing with SHA-256 for Password Storage

### Description
Resolved SonarQube Security issue (rule `python:S4790`) in `bookstore/auth.py`.

### Context & Root Cause
In `bookstore/auth.py:12`, the `hash_password` function utilized `hashlib.md5()` to hash user credentials. MD5 is an obsolete, cryptographically broken algorithm susceptible to collision and rainbow table attacks, leaving stored user passwords vulnerable to compromise.

### Changes Made
- Modified `bookstore/auth.py`:
  - Replaced `hashlib.md5(password.encode()).hexdigest()` with `hashlib.sha256(password.encode()).hexdigest()`.
- Verified that user registration and authentication flow in `bookstore/main.py` executes without errors.

---

## [2026-10-15] Fix 10: Remove Control Flow 'return' Statement from 'finally' Block

### Description
Resolved SonarQube Reliability issue (rule `python:S1143` / `python:S2737`) in `bookstore/database.py`.

### Context & Root Cause
In `bookstore/database.py:62`, `update_stock` placed a `return True` statement inside a `finally:` block. In Python, returning from a `finally` block suppresses and swallows any unhandled exception raised within the preceding `try` block, masking critical database execution errors and triggering runtime `SyntaxWarning`.

### Changes Made
- Modified `bookstore/database.py`:
  - Removed the anti-pattern `try/finally: return True` block in `update_stock`.
  - Moved `return True` directly to the end of `update_stock` after committing the database transaction.
- Verified that `database.update_stock` functions correctly and the Python interpreter syntax warning is eliminated.

---

## [2026-10-15] Fix 11: Use Cryptographically Secure Pseudo-Random Number Generator for Session Tokens

### Description
Resolved SonarQube Security issue (rule `python:S2245`) in `bookstore/auth.py`.

### Context & Root Cause
In `bookstore/auth.py:29`, authentication session tokens were generated using `random.randint()`. Standard pseudo-random number generators (PRNG) like Python's `random` module rely on the Mersenne Twister algorithm, which is completely predictable once sufficient outputs are observed. This enables session hijacking and user impersonation attacks.

### Changes Made
- Modified `bookstore/auth.py`:
  - Replaced `import random` with `import secrets`.
  - Replaced insecure `token = str(random.randint(100000, 999999))` with cryptographically strong `token = secrets.token_hex(16)`.
- Verified that login, session storage, and subsequent order operations function securely in `bookstore/main.py`.

