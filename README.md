# 🛡️ VulnHunter – Cybersecurity Vulnerability Scanner

**VulnHunter** is a simple yet powerful web-based vulnerability scanner built with Flask. It scans web applications for common security issues including OWASP Top 10 vulnerabilities and generates a PDF report of the findings.

![VulnHunter Banner](https://img.shields.io/badge/Flask-WebApp-blue?style=flat-square)  
🔒 **Security-focused** | ⚡ **Fast scanning** | 📄 **Auto-generated reports**

---

## 🚀 Features

- ✨ Beautiful cyber-themed user interface
- ✅ Detects common web vulnerabilities:
  - Cross-Site Scripting (XSS)
  - SQL Injection (SQLi)
  - Command Injection
  - Server-Side Request Forgery (SSRF)
  - Weak Authentication
  - Security Header Misconfiguration
  - Outdated JavaScript Components
- 🧾 Generates a detailed **PDF report**
- 📁 Saves reports in a `reports/` directory
- 🌐 Deployable on **Render**, **Replit**, or any Python server

---

## 🖥️ Live Demo

> 🟢 https://vuln-hunter.onrender.com

---

## 🛠️ Installation & Usage

### 🧪 Run Locally

```bash
git clone https://github.com/your-username/vulnhunter.git
cd vulnhunter
pip install -r requirements.txt
python app.py
````

Then open your browser at:
`http://localhost:5000`

---


## 📋 PDF Report Example

Each report includes:

* Target URL
* Type of vulnerabilities found
* Severity level (color-coded)
* Recommendations
* A timestamped file name

---

## ⚠️ Disclaimer

This tool is for **educational and authorized testing only**. Do **NOT** scan websites you do not own or have permission to test. Unauthorized use may violate laws and terms of service.

---

## 🧠 Credits

Made with ❤️ by [Shayan Chakraborty](https://github.com/Rexona-3112)

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
