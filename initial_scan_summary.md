@"
# ❌ Initial Security Scan Summary – Pre-Hardening

## 🔍 Bandit Findings
- ❌ B105: Hardcoded password in `app.py`
- ❌ B602: `subprocess` call with `shell=True` (command injection risk)
- ❌ B307: Insecure use of `eval()` (arbitrary code execution)

## 🛡️ Safety Findings
- ❌ `urllib3` v1.25.9 - CVE-2020-26137 (CRLF injection vulnerability)
- ❌ Other packages outdated or lacking pinned versions

## 🔒 Lynis Host Scan (Container-Level)
- ❌ Container ran as `root`
- ❌ No memory or PID limits
- ❌ File system fully writable
- ❌ SSH configuration allows root login

## ⚠️ Configuration Issues
| Area                | Issue                                   |
|---------------------|-----------------------------------------|
| Flask Binding       | `0.0.0.0` (exposed to public)           |
| Secrets             | Password hardcoded in code              |
| Code Execution      | `eval()` directly executes user input   |
| Command Handling    | User input sent to shell via `ping`     |
| Docker Base         | Full-size image with unused packages    |

"@ | Out-File -FilePath .\initial_scan_summary.md -Encoding utf8
