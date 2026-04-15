# Nmap Micro-Report: scanme.nmap.org

## Target Overview

| Field | Value |
|---|---|
| **Target** | scanme.nmap.org |
| **Resolved IP** | 45.33.32.156 |
| **IPv6** | 2600:3c01::f03c:91ff:fe18:bb2f |
| **Scan Timestamp** | 2026-04-10T22:31:46Z |
| **Scan Type** | TCP Connect (-sT), Service Version (-sV), NSE Scripts |

---

## Open Ports

| Port | Protocol | Service | Version |
|---|---|---|---|
| 22 | tcp | ssh | tcpwrapped (OpenSSH-style) |
| 80 | tcp | http | Apache httpd 2.4.7 (Ubuntu) |
| 9929 | tcp | nping-echo | Nping echo |
| 31337 | tcp | tcpwrapped | (unknown service) |

---

## OS Detection

OS detection did not return conclusive results. The target responded with TCP RST to OS fingerprint probes, which can occur when `--osscan-limit` restricts probing or when the target's TCP stack does not exhibit distinctive fingerprint characteristics. Based on the service banners (Ubuntu-labeled Apache), the target is likely **Linux (Ubuntu)**.

---

## NSE Findings

### Port 22/tcp (SSH)

- **Authentication methods**: `publickey`, `password`
  - Password authentication is enabled -- this is a potential security concern for hardened systems.
- **Key Exchange Algorithms**: 8 algorithms supported, including modern (curve25519-sha256, ecdh-sha2-nistp256/384/521) and legacy (diffie-hellman-group1-sha1, diffie-hellman-group-exchange-sha1).
- **Server Host Key Algorithms**: ssh-rsa, ssh-dss, ecdsa-sha2-nistp256, ssh-ed25519
- **Encryption Algorithms**: 16 algorithms including several weak/deprecated ciphers: `arcfour256`, `arcfour128`, `arcfour`, `3des-cbc`, `blowfish-cbc`, `cast128-cbc`, `aes192-cbc`, `aes256-cbc`, `rijndael-cbc@lysator.liu.se`
- **MAC Algorithms**: 19 algorithms including legacy MD5/SHA1-based MACs.

### Port 80/tcp (HTTP)

- **Page title**: "Go ahead and ScanMe!"
- **Server banner**: Apache/2.4.7 (Ubuntu)
- **HTTP Methods**: POST, OPTIONS, GET, HEAD
- **HTTP Headers**:
  - `Server: Apache/2.4.7 (Ubuntu)` -- version disclosed
  - `Content-Type: text/html`
  - No security-related headers present (no HSTS, CSP, X-Frame-Options, X-Content-Type-Options)
- **Directory enumeration**: `/images/` -- Potentially interesting directory with listing enabled on Apache
- **http-security-headers**: Script returned no output (possible script bug on this Nmap version)
- **http-robots.txt**: No robots.txt found

### Port 9929/tcp (Nping Echo)

- Standard Nmap echo service used for debugging/testing. No additional scripts run.

### Port 31337/tcp (tcpwrapped)

- Port is open but service is tcpwrapped (connection wrapped before service identification). No additional information available.

---

## Security Notes

1. **Weak SSH encryption algorithms**: The SSH service supports several deprecated/weak ciphers including `arcfour`, `3des-cbc`, `blowfish-cbc`, and `rijndael-cbc@lysator.liu.se`. These should be disabled in production environments.
2. **Legacy SSH key exchange**: `diffie-hellman-group1-sha1` is considered cryptographically weak and should be removed.
3. **SSH password authentication enabled**: Password-based auth is available alongside publickey, increasing brute-force attack surface.
4. **Server version disclosure**: Apache/2.4.7 (Ubuntu) is an outdated version (circa Ubuntu 14.04 LTS) and may contain known CVEs. The server banner explicitly reveals the version.
5. **Missing HTTP security headers**: No `Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, or `Referrer-Policy` headers are set.
6. **Directory listing enabled**: `/images/` allows directory browsing, which may expose sensitive files.
7. **Port 31337/tcpwrapped**: This non-standard port is open but the service is tcpwrapped. Further investigation recommended to identify the running service.

---

## Scan Artifacts

| File | Description |
|---|---|
| `scans/discovery.nmap` | Phase 1 human-readable output |
| `scans/discovery.xml` | Phase 1 XML output |
| `scans/discovery.gnmap` | Phase 1 grepable output |
| `scans/detailed.nmap` | Phase 2 human-readable output |
| `scans/detailed.xml` | Phase 2 XML output |
| `scans/detailed.gnmap` | Phase 2 grepable output |
| `scans/report.md` | This report |

---

```json
{
  "target": "scanme.nmap.org",
  "scan_timestamp": "2026-04-10T22:31:46Z",
  "open_ports": [22, 80, 9929, 31337],
  "services": {
    "22": "ssh tcpwrapped (publickey, password auth)",
    "80": "http Apache httpd 2.4.7 (Ubuntu)",
    "9929": "nping-echo Nping echo",
    "31337": "tcpwrapped (unknown service)"
  },
  "os": "Linux (Ubuntu) - OS detection inconclusive",
  "nse_findings": {
    "22": {
      "auth_methods": ["publickey", "password"],
      "kex_algorithms": ["curve25519-sha256@libssh.org", "ecdh-sha2-nistp256", "ecdh-sha2-nistp384", "ecdh-sha2-nistp521", "diffie-hellman-group-exchange-sha256", "diffie-hellman-group-exchange-sha1", "diffie-hellman-group14-sha1", "diffie-hellman-group1-sha1"],
      "host_key_algorithms": ["ssh-rsa", "ssh-dss", "ecdsa-sha2-nistp256", "ssh-ed25519"],
      "weak_ciphers": ["arcfour256", "arcfour128", "arcfour", "3des-cbc", "blowfish-cbc", "cast128-cbc", "aes192-cbc", "aes256-cbc", "rijndael-cbc@lysator.liu.se"]
    },
    "80": {
      "http_title": "Go ahead and ScanMe!",
      "http_server_header": "Apache/2.4.7 (Ubuntu)",
      "http_methods": ["POST", "OPTIONS", "GET", "HEAD"],
      "missing_headers": ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options"],
      "directory_listing": ["/images/"],
      "robots_disallowed": []
    }
  },
  "notes": [
    "SSH supports weak/deprecated ciphers: arcfour, 3des-cbc, blowfish-cbc, rijndael-cbc",
    "SSH supports weak key exchange: diffie-hellman-group1-sha1",
    "SSH password authentication is enabled alongside publickey",
    "Apache 2.4.7 is outdated and may have known CVEs",
    "Server version disclosed in HTTP banner",
    "Missing security headers on port 80 (HSTS, CSP, X-Frame-Options, X-Content-Type-Options)",
    "Directory listing enabled on /images/",
    "Port 31337 is open but tcpwrapped - service unidentified",
    "OS detection was inconclusive - likely Linux (Ubuntu) based on service banners"
  ]
}
```
