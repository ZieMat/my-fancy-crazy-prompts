---
name: nmap-enumerator
description: >
  Performs adaptive, structured Nmap scans and service enumeration for security testing and web application assessment.
  Use this skill whenever the user wants to scan a target (host, IP, range, or domain) with Nmap, discover open ports,
  identify services and versions, run relevant NSE scripts, and produce a structured report for downstream analysis.
  Trigger on requests like "scan this host", "run nmap", "enumerate services", "check for open ports", "recon this target",
  "pentest scan", "service discovery", or any security assessment workflow involving network reconnaissance.
  Always confirm the user has authorization to scan the target before proceeding.
---

# Nmap Enumerator

Adaptive, two-phase Nmap scanning that discovers open ports, then dynamically constructs targeted follow-up scans based on what it finds. Produces a structured micro-report (markdown + JSON) for downstream analysis.

## Authorization check

Before running any scan, confirm the user has explicit authorization to scan the target. Ask:
- "Do you own this target, or do you have explicit written authorization (e.g., a pentest engagement letter) to scan it?"

If the user cannot confirm authorization, **do not proceed**. Explain that scanning systems without authorization may be illegal and against terms of service.

## Execution method

**Prefer MCP tools for Nmap if available.** Check your available MCP tools first — if an Nmap-related MCP tool exists (e.g., `nmap_scan`, `nmap_discover`, `nmap_enumerate`, or similar), use it instead of raw shell commands. The two-phase workflow and adaptive logic below still apply; just map the flags to the MCP tool's parameters.

**If no Nmap MCP tool is available**, fall back to CLI commands via `run_shell_command`. The commands below are written in CLI form for reference — translate them as needed for MCP tool calls.

## Phase 1: Full-port discovery

Run a fast, full-port scan to discover all open ports:

**CLI form:**
```bash
nmap -p- --open -T4 --min-rate 1000 -sS -Pn -oA scans/discovery <target>
```

**Key flags** (apply equivalent parameters in MCP tool calls):
- `-p-` — scan all 65535 ports
- `--open` — only show open/possibly open ports
- `-T4 --min-rate 1000` — aggressive timing for speed
- `-sS` — SYN scan (stealthier and faster than full TCP connect); fall back to `-sT` if not root
- `-Pn` — skip host discovery (treat target as up)
- `-oA scans/discovery` — writes `.nmap`, `.xml`, and `.gnmap` simultaneously

Parse the output to extract the list of open ports. If no ports are open, report that and stop.

## Phase 2: Adaptive service + script scan

Using only the discovered open ports, construct a targeted follow-up scan:

**CLI form:**
```bash
nmap -sV -O --osscan-limit -p <comma_separated_open_ports> \
  --script "<dynamically_built_script_list>" \
  --script-args safe=1 \
  -oA scans/detailed <target>
```

**MCP form:** Pass the same parameters (`ports`, `scripts`, `service_detection`, `os_detection`) to the equivalent MCP tool call.

### Dynamic script selection

Build the `--script` argument by checking which ports are open and appending relevant NSE scripts:

| Open port(s) | Add these NSE scripts |
|---|---|
| 22 (SSH) | `ssh-auth-methods,ssh2-enum-algos` |
| 21 (FTP) | `ftp-anon,ftp-bounce` |
| 25 (SMTP) | `smtp-enum-users,smtp-open-relay,smtp-commands` |
| 53 (DNS) | `dns-recursion,dns-zone-transfer` |
| 80, 443, 8080, 8443, 8000, 8888 (HTTP/S) | `http-title,http-server-header,http-headers,http-methods,http-robots.txt,http-enum,http-security-headers,http-waf-detect` |
| 443 (HTTPS specifically) | also add `ssl-enum-ciphers,ssl-cert,ssl-heartbleed,ssl-date` |
| 139, 445 (SMB) | `smb-os-discovery,smb-enum-shares,smb-enum-users,smb-vuln-ms17-010` |
| 161 (SNMP) | `snmp-sysdescr` |
| 389 (LDAP) | `ldap-rootdse` |
| 1433 (MSSQL) | `ms-sql-info,ms-sql-empty-password` |
| 3306 (MySQL) | `mysql-info,mysql-empty-password,mysql-databases` |
| 5432 (PostgreSQL) | `pgsql-brute` (safe info-gathering only, skip actual brute-force unless user requests) |
| 6379 (Redis) | `redis-info` |
| 27017 (MongoDB) | `mongodb-info` |
| 2049 (NFS) | `nfs-showmount,nfs-ls` |
| 8080, 8443, 9090, 9200, 11211, etc. (other web-adjacent) | treat as HTTP: `http-title,http-headers,http-methods` |
| 4443, 8443 (alt HTTPS) | treat as HTTPS: add SSL scripts too |

After building the list, deduplicate and join with commas. If no specific scripts matched, fall back to `default,vuln,safe`.

### Scan type adjustments

- If Phase 1 used `-sS` (root), keep `-sS` in Phase 2. If it fell back to `-sT`, use `-sT` here too.
- If the target appears to be behind a WAF/CDN (detected via `http-waf-detect` or unusual TTL/response patterns), add `--scanflags` with stealthier flags and reduce timing to `-T2`.
- If Phase 1 shows >100 open ports (likely a honeypot or misconfigured target), limit Phase 2 to the top 50 most common service ports and note this in the report.

## Parsing results

Parse the Phase 2 XML output (`scans/detailed.xml`) to extract:

1. **Open ports** — list of port numbers with protocol (tcp/udp)
2. **Service names and versions** — from the `<service>` elements with `name`, `product`, `version`, `extrainfo` attributes
3. **OS fingerprint** — from the `<os>` section, extract `<osmatch name="...">` entries with accuracy scores
4. **NSE findings** — from `<script>` elements within each `<port>`:
   - `http-title`: page title
   - `http-server-header`: server version banner
   - `http-robots.txt`: disallowed entries
   - `http-security-headers`: missing headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options, etc.)
   - `ssl-enum-ciphers`: cipher grades, weak cipher warnings
   - `ssl-heartbleed`: vulnerable or not
   - `ssh-auth-methods`: supported auth methods
   - `ssh2-enum-algos`: encryption/MAC/kex algorithms
   - `ftp-anon`: anonymous login status
   - `smb-vuln-*`: vulnerability detection results
   - `mysql-info`/`redis-info`/`mongodb-info`: service details
   - Any other script output with findings

Use Python's `xml.etree.ElementTree` or `lxml` to parse the XML, or use `grep`/`awk` on the `.gnmap` file for quick extraction.

## Micro-report generation

Generate a structured markdown report with an embedded JSON block at the end. The report should have these sections:

### Markdown sections
1. **Target overview** — target address, scan timestamp
2. **Open ports** — table of port/protocol/service/version
3. **OS detection** — detected OS with confidence
4. **NSE findings** — bullet list of notable discoveries per port
5. **Security notes** — any suspicious/exposed items (weak ciphers, outdated versions, missing security headers, anonymous FTP, exposed databases, etc.)

### JSON block

At the end of the report, output a JSON code block with this exact structure:

```json
{
  "target": "<user_provided_target>",
  "scan_timestamp": "<ISO 8601 timestamp>",
  "open_ports": [22, 80, 443, 3306],
  "services": {
    "22": "ssh OpenSSH 8.9p1",
    "80": "http nginx 1.20.1",
    "443": "https nginx 1.20.1 (TLS 1.2/1.3)",
    "3306": "mysql MySQL 8.0.31"
  },
  "os": "Linux 5.x (96% confidence)",
  "nse_findings": {
    "443": {
      "ssl_grade": "B",
      "weak_ciphers": ["TLS_RSA_WITH_AES_128_CBC_SHA"],
      "heartbleed": "not vulnerable"
    },
    "80": {
      "http_title": "Welcome to Example",
      "missing_headers": ["Strict-Transport-Security", "Content-Security-Policy"],
      "robots_disallowed": ["/admin", "/backup"]
    }
  },
  "notes": [
    "HTTP server exposes version in banner",
    "SSL supports weak ciphers (grade B)",
    "Missing security headers on port 80",
    "robots.txt exposes /admin and /backup paths"
  ]
}
```

This JSON is designed for machine consumption by downstream agents or MCP-style toolchains.

## Output files

Save all scan outputs and reports in a `scans/` directory relative to the current working directory:
```
scans/
├── discovery.nmap
├── discovery.xml
├── discovery.gnmap
├── detailed.nmap
├── detailed.xml
├── detailed.gnmap
└── report.md          ← the micro-report
```

## Error handling

- If neither an Nmap MCP tool nor the `nmap` CLI is available, tell the user they need to provide access to Nmap (install via `apt install nmap` or connect an Nmap MCP server)
- If a scan times out (use `--host-timeout 10m --script-timeout 5m`), note the timeout and report partial results
- If output is malformed or missing, fall back to parsing whatever format is available
- If the target is unreachable, report that clearly and suggest checking connectivity/firewall rules
