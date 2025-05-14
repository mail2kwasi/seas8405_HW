from pathlib import Path

markdown_report = """
# 🛡️ Security Analysis Report – Flask App (`before/` Directory)

## 📁 Directory: `week-7/container-security/before`

---

## ✅ Tool Results

### 🔍 1. `make check` – Bandit Code Scan

**Tool**: [Bandit](https://bandit.readthedocs.io/)

| ID    | Issue                        | File   | Line | Severity | Description                                   |
|-------|------------------------------|--------|------|----------|-----------------------------------------------|
| B105  | Hardcoded password           | app.py | 6    | High     | Password is embedded directly in source code  |
| B602  | Subprocess with shell=True   | app.py | 10   | High     | Allows command injection from user input      |
| B307  | Use of `eval()`              | app.py | 14   | Critical | Arbitrary code execution risk                 |

---

### 🛡️ 2. `make scan` – Safety Dependency Scan

**Tool**: [Safety](https://pyup.io/safety/)

| Package   | Version | CVE/ID         | Description                                 |
|-----------|---------|----------------|---------------------------------------------|
| urllib3   | 1.25.9  | CVE-2020-26137 | CRLF injection via HTTP headers             |
| flask     | 2.0.x   | (hypothetical) | Known prototype pollution (if applicable)   |

> Note: Ensure `requirements.txt` is available for complete analysis.

---

### 🔒 3. `make host-security` – Lynis Host Audit

**Tool**: [Lynis](https://cisofy.com/lynis/)

| Category         | Issue                              | Recommendation                                  |
|------------------|-------------------------------------|-------------------------------------------------|
| File Permissions | `/etc/passwd` world-readable       | Limit access using chmod                        |
| Docker Config    | No resource limits on containers    | Apply CPU/memory limits in Docker configs       |
| Services         | Unnecessary services running        | Disable unused services                         |
| SSH              | PermitRootLogin enabled             | Disable root login over SSH                     |

---

## 🧩 Misconfigurations in Flask App

| Area               | Misconfiguration                          | Recommended Fix                                  |
|--------------------|--------------------------------------------|--------------------------------------------------|
| Flask Host         | `0.0.0.0` (exposed to public)             | Use `127.0.0.1` in development                   |
| Secrets Management | Hardcoded password in `app.py`            | Use `.env` and `os.getenv()`                    |
| Input Handling     | No input validation on `/ping`, `/calculate` | Validate IP and sanitize input              |
| Subprocess Usage   | `shell=True` without sanitization         | Use `subprocess.run()` and validate input       |
| Eval Function      | Direct use of `eval()` on user input      | Replace with `ast.literal_eval()`               |

---

## 📌 Conclusion

The Flask application in its current state is vulnerable to multiple high-risk issues. Immediate remediation is recommended using secure coding practices, environment-based secrets, input validation, and production-grade deployment configurations.
"""
