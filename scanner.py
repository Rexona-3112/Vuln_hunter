import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def get_forms(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get").lower()
    inputs = [
        {"type": input_tag.attrs.get("type", "text"), "name": input_tag.attrs.get("name")}
        for input_tag in form.find_all("input") if input_tag.attrs.get("name")
    ]
    return {"action": action, "method": method, "inputs": inputs}

def submit_form(form_details, url, payload):
    target_url = urljoin(url, form_details["action"])
    data = {}
    for input in form_details["inputs"]:
        data[input["name"]] = payload if input["type"] == "text" else "test"
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

def scan_xss(url):
    findings = []
    xss_payload = "<script>alert('XSS')</script>"
    for form in get_forms(url):
        details = get_form_details(form)
        res = submit_form(details, url, xss_payload)
        if xss_payload in res.text:
            findings.append({
                "type": "XSS",
                "description": "Reflected XSS in form input.",
                "level": "Medium",
                "location": details["action"],
                "recommendation": "Escape user input using proper encoding."
            })
    return findings

def scan_sqli(url):
    findings = []
    sqli_payload = "' OR '1'='1"
    for form in get_forms(url):
        details = get_form_details(form)
        res = submit_form(details, url, sqli_payload)
        if "syntax" in res.text.lower() or sqli_payload in res.text:
            findings.append({
                "type": "SQL Injection",
                "description": "SQLi vulnerability in form input.",
                "level": "High",
                "location": details["action"],
                "recommendation": "Use parameterized queries or ORM libraries."
            })
    return findings

def scan_command_injection(url):
    findings = []
    for form in get_forms(url):
        details = get_form_details(form)
        for payload in ["; whoami", "| whoami", "&& whoami"]:
            res = submit_form(details, url, payload)
            if any(keyword in res.text for keyword in ["root", "admin", "user"]):
                findings.append({
                    "type": "Command Injection",
                    "description": f"Detected command execution with payload '{payload}'.",
                    "level": "High",
                    "location": details["action"],
                    "recommendation": "Sanitize inputs and avoid unsafe shell calls."
                })
                break
    return findings

def scan_ssrf(url):
    findings = []
    test_url = "http://127.0.0.1"
    for form in get_forms(url):
        details = get_form_details(form)
        res = submit_form(details, url, test_url)
        if "127.0.0.1" in res.text or "localhost" in res.text:
            findings.append({
                "type": "SSRF",
                "description": "Potential SSRF via internal address.",
                "level": "Medium",
                "location": details["action"],
                "recommendation": "Block internal IP access in requests."
            })
    return findings

def scan_weak_auth(url):
    findings = []
    creds = [("admin", "admin"), ("root", "toor"), ("user", "user")]
    for form in get_forms(url):
        details = get_form_details(form)
        inputs = [i["name"] for i in details["inputs"] if i["type"] in ["text", "password"]]
        if len(inputs) < 2:
            continue
        for u, p in creds:
            data = {inputs[0]: u, inputs[1]: p}
            target = urljoin(url, details["action"])
            res = requests.post(target, data=data)
            if "logout" in res.text.lower() or "dashboard" in res.text.lower():
                findings.append({
                    "type": "Weak Authentication",
                    "description": f"Weak credentials found: {u}/{p}",
                    "level": "High",
                    "location": details["action"],
                    "recommendation": "Enforce strong passwords and rate-limiting."
                })
                break
    return findings

def scan_security_misconfig(url):
    findings = []
    res = requests.get(url)
    missing = []
    for h in [
        "X-Frame-Options", "Strict-Transport-Security",
        "Content-Security-Policy", "X-Content-Type-Options"
    ]:
        if h not in res.headers:
            missing.append(h)
    if missing:
        findings.append({
            "type": "Security Misconfiguration",
            "description": f"Missing headers: {', '.join(missing)}",
            "level": "Low",
            "location": url,
            "recommendation": "Configure headers to secure HTTP responses."
        })
    return findings

def scan_outdated_components(url):
    findings = []
    vulnerable = {
        "jquery": ["1.7", "1.8"],
        "bootstrap": ["3.2", "3.3"],
        "angular": ["1.2", "1.3"]
    }
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    for script in soup.find_all("script", src=True):
        src = script["src"]
        for lib, versions in vulnerable.items():
            for v in versions:
                if lib in src and v in src:
                    findings.append({
                        "type": "Outdated Component",
                        "description": f"{lib} version {v} detected at {src}",
                        "level": "Medium",
                        "location": src,
                        "recommendation": "Update to latest secure version."
                    })
    return findings

def generate_pdf_report(url, findings):
    os.makedirs("reports", exist_ok=True)
    domain = url.split("//")[-1].replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{domain}_{timestamp}.pdf"
    path = os.path.join("reports", filename)

    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica", 11)
    y = 750
    c.drawString(40, y, f"Vulnerability Report for {url}")
    y -= 30
    for vuln in findings:
        color = {"High": "red", "Medium": "orange", "Low": "yellow"}[vuln["level"]]
        c.setFillColor(color)
        c.drawString(40, y, f"- {vuln['type']} ({vuln['level']}): {vuln['description']}")
        y -= 14
        c.setFillColor("white")
        c.drawString(50, y, f"Location: {vuln['location']}")
        y -= 14
        c.drawString(50, y, f"Fix: {vuln['recommendation']}")
        y -= 24
        if y < 80:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = 750
    c.save()
    return filename