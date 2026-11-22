# Mini-VulnFinBot Secure Pipeline

## Project Description
Mini-VulnFinBot is a simplified AI-powered financial assistant application built to demonstrate a production-grade CI/CD pipeline integrated with automated security controls, Static Application Security Testing (SAST), dependency scanning, container scanning, Dynamic Application Security Testing (DAST), and AI-specific security testing (prompt injection).

---

## Technologies Used
- **Python 3.12**: Application development
- **Flask 3.1**: Backend REST API framework
- **pytest**: Automated unit and security testing
- **GitHub Actions**: CI/CD automation and artifact collection
- **Bandit**: Python static security analysis
- **Semgrep**: Rule-based static application security analysis
- **pip-audit**: Python dependency vulnerability scanning
- **Docker**: Containerization
- **Trivy**: Container image vulnerability scanner
- **OWASP ZAP**: Dynamic application security testing (DAST)

---

## Project Architecture
```
vulnfinbot-secure-pipeline/
│
├── app/
│   ├── __init__.py
│   └── routes.py
│
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│   └── test_ai_security.py
│
├── security/
│   └── semgrep/
│       └── rules.yml
│
├── reports/
│   ├── bandit-report.json
│   ├── semgrep-report.json
│   ├── dependency-report.json
│   ├── trivy-report.json
│   ├── zap-report.json
│   └── ai-security-report.md
│
├── .github/
│   └── workflows/
│       └── security-pipeline.yml
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── run.py
└── README.md
```

---

## Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/trunestor/vulnfinbot-secure-pipeline.git
   cd vulnfinbot-secure-pipeline
   ```

2. **Create a Virtual Environment (Python 3.12):**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows Git Bash
   ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install pytest bandit semgrep pip-audit
   ```

---

## Running the Application
```bash
python run.py
```
The application will be accessible at `http://localhost:5000`.

- **Health Check Endpoint:** `GET /health`
- **Chat Endpoint:** `POST /api/chat` (expects JSON `{"message": "..."}`)

---

## Executing Tests
Run unit tests and AI security tests using `pytest`:
```bash
pytest -v
```

---

## CI/CD Pipeline & Security Tools
The GitHub Actions workflow (`.github/workflows/security-pipeline.yml`) automatically executes on every push and pull request to `main`:
1. **Checkout & Python Setup**: Sets up Python 3.12.
2. **Dependencies & Unit Tests**: Installs dependencies and runs `pytest`.
3. **Bandit (SAST)**: Scans Python source code for security anti-patterns.
4. **Semgrep (SAST)**: Executes custom security rules (e.g. detecting `eval()` usage).
5. **pip-audit**: Scans Python dependencies for known CVEs.
6. **Docker Build**: Builds the production container image.
7. **Trivy**: Scans the container image for OS and package vulnerabilities.
8. **Artifact Upload**: Collects all reports (`reports/`) into GitHub Actions artifacts (retained for 30 days).

---

## Summary Table of Security Findings

| Security Tool | Findings | Severity | Recommended Action |
|---|---|---|---|
| **Bandit** | 0 | Low / None | Maintain secure coding practices and keep code free of hardcoded secrets. |
| **Semgrep** | 0 | Low / None | Continue enforcing custom rules against dangerous functions (`eval`, `exec`). |
| **pip-audit** | 0 (pinned) | Informational | Regularly update dependencies to patch upstream CVEs. |
| **Trivy** | Minimal OS CVEs | Low / Medium | Use slim/distroless base images and update base layers regularly. |
| **OWASP ZAP** | Missing security headers (CSP, HSTS) | Medium | Configure Flask response headers for HSTS, CSP, and X-Content-Type-Options. |
| **AI Security Tests** | 0 failures | High (Mitigated) | Continuously test against emerging prompt injection vectors and enforce strict output validation. |
