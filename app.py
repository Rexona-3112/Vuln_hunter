from flask import Flask, render_template, request, send_from_directory, session
from scanner import (
    scan_xss, scan_sqli, scan_command_injection, scan_ssrf,
    scan_weak_auth, scan_security_misconfig, scan_outdated_components,
    generate_pdf_report
)
import os

app = Flask(__name__)
app.secret_key = 'vulnhunter_secret'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        if not url.startswith("http"):
            url = "http://" + url

        selected_scans = request.form.keys()
        findings = []

        if 'xss' in selected_scans:
            findings += scan_xss(url)
        if 'sqli' in selected_scans:
            findings += scan_sqli(url)
        if 'cmd' in selected_scans:
            findings += scan_command_injection(url)
        if 'ssrf' in selected_scans:
            findings += scan_ssrf(url)
        if 'auth' in selected_scans:
            findings += scan_weak_auth(url)
        if 'headers' in selected_scans:
            findings += scan_security_misconfig(url)
        if 'js' in selected_scans:
            findings += scan_outdated_components(url)

        session["results"] = findings
        session["url"] = url

        pdf_file = generate_pdf_report(url, findings)
        session["pdf"] = pdf_file

        show_intro = False
        return render_template("index.html", findings=findings, report=pdf_file, show_intro=show_intro)

    # GET method
    session.pop("results", None)
    session.pop("url", None)
    session.pop("pdf", None)

    show_intro = True
    return render_template("index.html", findings=None, report=None, show_intro=show_intro)

@app.route("/download-report")
def download_report():
    filename = session.get("pdf")
    if filename and os.path.exists(os.path.join("reports", filename)):
        return send_from_directory("reports", filename, as_attachment=True)
    return "No report available", 404

# ✅ Only one launch block, suitable for Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))