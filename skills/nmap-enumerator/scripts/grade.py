#!/usr/bin/env python3
"""
Grading script for nmap-enumerator skill evals.
Checks assertions against with_skill output directories.
Usage: python grade.py <eval_run_directory>
Example: python grade.py iteration-1/web-app-assessment/with_skill
"""

import json
import os
import re
import sys
from pathlib import Path


def check_file_exists(base_dir, rel_path):
    """Check if a file exists relative to the outputs directory."""
    return os.path.exists(os.path.join(base_dir, rel_path))


def read_file(base_dir, rel_path):
    """Read a file and return its content, or None if not found."""
    full_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(full_path):
        return None
    with open(full_path, "r") as f:
        return f.read()


def check_authorization(text):
    """Check if the output mentions authorization confirmation."""
    if text is None:
        return False, "No output text to check"
    keywords = ["authorization", "authorized", "permission", "own infrastructure", "written authorization", "engagement"]
    for kw in keywords:
        if kw.lower() in text.lower():
            return True, f"Found authorization reference: '{kw}'"
    return False, "No authorization check found"


def check_two_phase_scan(text):
    """Check if both Phase 1 (full-port) and Phase 2 (targeted) commands are present."""
    if text is None:
        return False, "No output text to check"
    has_phase1 = bool(re.search(r'-p-', text))  # full port scan
    has_phase2 = bool(re.search(r'-sV', text))  # version detection
    if has_phase1 and has_phase2:
        return True, "Both -p- (full port) and -sV (version detection) flags found"
    reasons = []
    if not has_phase1:
        reasons.append("missing -p- flag")
    if not has_phase2:
        reasons.append("missing -sV flag")
    return False, "; ".join(reasons)


def check_adaptive_scripts(text):
    """Check that NSE scripts are targeted/adaptive, not blanket --script all."""
    if text is None:
        return False, "No output text to check"
    if re.search(r'--script\s+(all|"all")', text):
        return False, "Uses blanket '--script all' instead of targeted selection"
    # Check for specific NSE script names being used
    nse_scripts = [
        "ssh-auth-methods", "ssh2-enum-algos", "http-title", "http-server-header",
        "http-headers", "http-methods", "http-robots.txt", "http-enum",
        "http-security-headers", "http-waf-detect", "ssl-enum-ciphers",
        "ssl-cert", "ssl-heartbleed", "mysql-info", "mysql-empty-password",
        "redis-info", "ftp-anon", "smtp-enum-users", "smb-vuln-ms17-010",
        "dns-recursion", "snmp-sysdescr", "mongodb-info"
    ]
    found = [s for s in nse_scripts if s in text]
    if len(found) >= 2:
        return True, f"Found {len(found)} specific NSE scripts: {', '.join(found[:5])}{'...' if len(found) > 5 else ''}"
    return False, f"Only found {len(found)} specific NSE scripts (need >= 2 for adaptive selection)"


def check_markdown_report(report_text):
    """Check if report.md exists and has proper sections."""
    if report_text is None:
        return False, "report.md not found"
    required_sections = ["open port", "service", "os detect", "nse", "note"]
    found_sections = []
    for section in required_sections:
        if section.lower() in report_text.lower():
            found_sections.append(section)
    if len(found_sections) >= 3:
        return True, f"Found sections: {', '.join(found_sections)}"
    return False, f"Missing sections. Found: {', '.join(found_sections)}"


def check_valid_json(report_text):
    """Check if the embedded JSON block is valid and has required fields."""
    if report_text is None:
        return False, "report.md not found"
    json_match = re.search(r'```(?:json)?\s*\n([\s\S]*?)\n```', report_text)
    if not json_match:
        return False, "No JSON code block found in report"
    try:
        data = json.loads(json_match.group(1))
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    required_fields = ["target", "open_ports", "services", "os", "notes"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing required JSON fields: {', '.join(missing)}"
    # Additional structural checks
    if not isinstance(data["open_ports"], list) or len(data["open_ports"]) == 0:
        return False, "open_ports is empty or not a list"
    if not isinstance(data["services"], dict) or len(data["services"]) == 0:
        return False, "services is empty or not a dict"
    if not isinstance(data["notes"], list):
        return False, "notes is not a list"
    return True, f"Valid JSON with all required fields. {len(data['open_ports'])} ports, {len(data['services'])} services"


def check_output_files(outputs_dir):
    """Check that scans/ directory has both discovery and detailed outputs."""
    required_files = [
        "scans/discovery.nmap", "scans/discovery.xml", "scans/discovery.gnmap",
        "scans/detailed.nmap", "scans/detailed.xml", "scans/detailed.gnmap"
    ]
    missing = []
    for f in required_files:
        if not os.path.exists(os.path.join(outputs_dir, f)):
            missing.append(f)
    if missing:
        return False, f"Missing files: {', '.join(missing)}"
    return True, f"All {len(required_files)} output files present"


def check_nse_findings(report_text):
    """Check that the report includes NSE-based discoveries."""
    if report_text is None:
        return False, "report.md not found"
    nse_indicators = [
        "ssl_grade", "ssl_cipher", "cipher", "heartbleed",
        "http_title", "security header", "missing header",
        "robots", "vuln", "auth method", "enum",
        "mysql", "redis", "ssh", "ftp"
    ]
    found = [ind for ind in nse_indicators if ind.lower() in report_text.lower()]
    if len(found) >= 2:
        return True, f"Found NSE-based findings: {', '.join(found[:5])}"
    return False, "Insufficient NSE-based findings in report"


def grade_eval(eval_run_dir):
    """Run all assertions against an eval run directory."""
    # eval_run_dir is typically <eval>/<config>/run-N/
    # Outputs are in <eval>/<config>/outputs/scans/
    run_dir = Path(eval_run_dir)
    # Try to find outputs: look for outputs/ sibling to this run dir
    config_dir = run_dir.parent  # e.g., with_skill
    outputs_dir = str(config_dir / "outputs")
    if not os.path.isdir(outputs_dir):
        # Fallback: try the run dir itself
        outputs_dir = str(eval_run_dir)

    # Read the combined output (report.md + any log/notes)
    report_text = read_file(outputs_dir, "scans/report.md")
    # Also check for any output text files
    all_text = ""
    for f in ["scans/report.md", "scans/detailed.nmap", "scans/discovery.nmap"]:
        content = read_file(outputs_dir, f)
        if content:
            all_text += "\n" + content

    checks = [
        ("has_authorization_check", lambda: check_authorization(all_text)),
        ("has_two_phase_scan", lambda: check_two_phase_scan(all_text)),
        ("has_adaptive_script_selection", lambda: check_adaptive_scripts(all_text)),
        ("has_markdown_report", lambda: check_markdown_report(report_text)),
        ("has_valid_json", lambda: check_valid_json(report_text)),
        ("has_output_files", lambda: check_output_files(outputs_dir)),
        ("has_nse_findings", lambda: check_nse_findings(report_text)),
    ]

    expectations = []
    passed_count = 0
    for name, check_fn in checks:
        try:
            passed, evidence = check_fn()
        except Exception as e:
            passed, evidence = False, f"Error: {e}"
        if passed:
            passed_count += 1
        expectations.append({
            "text": name,
            "passed": passed,
            "evidence": evidence
        })

    total = len(expectations)
    results = {
        "expectations": expectations,
        "summary": {
            "pass_rate": round(passed_count / total, 4) if total > 0 else 0.0,
            "passed": passed_count,
            "failed": total - passed_count,
            "total": total
        }
    }

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python grade.py <eval_run_directory>")
        print("Example: python grade.py iteration-1/web-app-assessment/with_skill")
        sys.exit(1)

    eval_dir = sys.argv[1]
    results = grade_eval(eval_dir)

    # Save grading results
    grading_path = os.path.join(eval_dir, "grading.json")
    with open(grading_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Grading saved to {grading_path}")
    print(f"Assertions: {len(results['expectations'])}")
    passed = sum(1 for a in results["expectations"] if a["passed"])
    print(f"Passed: {passed}/{len(results['expectations'])}")
    for a in results["expectations"]:
        status = "PASS" if a["passed"] else "FAIL"
        print(f"  [{status}] {a['text']}: {a['evidence']}")


if __name__ == "__main__":
    main()
