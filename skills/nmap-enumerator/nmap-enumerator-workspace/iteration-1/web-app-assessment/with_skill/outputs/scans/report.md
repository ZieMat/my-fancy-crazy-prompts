# Nmap Enumeration Report

**Target:** 192.168.1.50  
**Scan Date:** 2026-04-11T14:22:05Z  
**Hostname:** webapp-staging.internal  
**Scanner:** Nmap 7.98  

---

## Target Overview

| Attribute   | Value                           |
|-------------|---------------------------------|
| Target      | 192.168.1.50                    |
| Hostname    | webapp-staging.internal         |
| Scan Time   | 2026-04-11T14:22:05Z            |
| Phase 1     | 42.15s (full port scan)         |
| Phase 2     | 85.42s (service + script scan)  |
| Open Ports  | 5                               |

---

## Open Ports

| Port  | Protocol | Service      | Version                                    |
|-------|----------|--------------|--------------------------------------------|
| 22    | tcp      | ssh          | OpenSSH 8.9p1 Ubuntu 3ubuntu0.6            |
| 80    | tcp      | http         | nginx 1.24.0                               |
| 443   | tcp      | ssl/http     | nginx 1.24.0                               |
| 3306  | tcp      | mysql        | MySQL 8.0.36                               |
| 8080  | tcp      | http         | Apache Tomcat 10.1.18                      |

---

## OS Detection

| OS Match                              | Confidence |
|---------------------------------------|------------|
| Linux 5.15 - 6.1 (Ubuntu 22.04 / 24.04) | 96%        |

---

## NSE Findings

### Port 22/tcp (SSH)

- **Authentication methods:** publickey, password, keyboard-interactive
- **Key exchange algorithms:** curve25519-sha256, diffie-hellman-group-exchange-sha256, diffie-hellman-group16-sha512, diffie-hellman-group18-sha512
- **Host key algorithms:** rsa-sha2-512, rsa-sha2-256, ecdsa-sha2-nistp256, ssh-ed25519
- **Encryption algorithms:** chacha20-poly1305, aes256-gcm, aes128-gcm, aes256-ctr, aes192-ctr, aes128-ctr
- **MAC algorithms:** hmac-sha2-256-etm, hmac-sha2-512-etm, hmac-sha2-256

### Port 80/tcp (HTTP)

- **Page title:** Welcome to MyApp Dashboard
- **Server header:** nginx/1.24.0
- **X-Powered-By:** PHP/8.2.14
- **HTTP methods:** GET, HEAD, POST, OPTIONS (OPTIONS flagged as potentially risky)
- **robots.txt:** 5 disallowed entries: `/admin/`, `/backup/`, `/config/`, `/wp-admin/`, `/.env`
- **Missing security headers:** Strict-Transport-Security, Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
- **Session cookie:** `session_id=abc123def456; Path=/; HttpOnly` (HttpOnly flag present, no Secure flag)
- **WAF:** Not protected by a WAF

### Port 443/tcp (HTTPS)

- **Page title:** Welcome to MyApp Dashboard
- **SSL Certificate:**
  - Subject: CN=webapp-staging.internal, O=MyApp Inc, ST=California, C=US
  - Issuer: CN=R3, O=Let's Encrypt, C=US
  - Key: RSA 2048-bit
  - Valid: 2026-01-15 to 2026-04-15 (expires in 4 days -- WARNING)
  - Signature: sha256WithRSAEncryption
- **SSL/TLS cipher grade:** B
  - TLSv1.2 ciphers: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256, TLS_RSA_WITH_AES_128_CBC_SHA (weak), TLS_RSA_WITH_AES_256_CBC_SHA (weak)
  - TLSv1.3 ciphers: TLS_AKE_WITH_AES_128_GCM_SHA256, TLS_AKE_WITH_AES_256_GCM_SHA384, TLS_AKE_WITH_CHACHA20_POLY1305_SHA256
  - **Warnings:** CBC-mode cipher in TLSv1.2 (CVE-2015-5242), Weak ciphers detected
- **Heartbleed:** VULNERABLE (NOT exploitable with current OpenSSL version) -- flagged for review
- **Missing security headers:** Content-Security-Policy, X-Frame-Options
- **WAF:** Not protected by a WAF

### Port 3306/tcp (MySQL)

- **Version:** MySQL 8.0.36
- **Auth plugin:** caching_sha2_password
- **Protocol:** 10, Status: Autocommit
- **CRITICAL:** Account `root@192.168.1.50` has empty password
- **Exposed databases:** information_schema, myapp_production, myapp_staging, performance_schema, sys

### Port 8080/tcp (HTTP - Tomcat)

- **Page title:** Apache Tomcat/10.1.18 - Manager App
- **Server header:** Apache-Coyote/1.1
- **HTTP methods:** GET, HEAD, POST, PUT, DELETE, OPTIONS (PUT and DELETE are risky)
- **Missing security headers:** Strict-Transport-Security, Content-Security-Policy, X-Frame-Options, X-Content-Type-Options
- **Manager app exposed:** Tomcat Manager application accessible on port 8080

---

## Security Notes

### Critical

1. **MySQL root account has empty password** -- The `root` MySQL user on 192.168.1.50 has no password set. This allows unauthenticated database access.
2. **Tomcat Manager exposed** -- Apache Tomcat Manager app is accessible on port 8080 without apparent access controls. This is a common attack vector.
3. **SSL certificate expiring soon** -- The Let's Encrypt certificate expires on 2026-04-15 (4 days from scan date).
4. **robots.txt exposes sensitive paths** -- Disallowed entries reveal `/admin/`, `/backup/`, `/config/`, `/wp-admin/`, and `/.env`. The `.env` file may contain credentials and secrets.

### High

5. **Weak SSL ciphers** -- TLS_RSA_WITH_AES_128_CBC_SHA and TLS_RSA_WITH_AES_256_CBC_SHA are weak CBC-mode ciphers vulnerable to padding oracle attacks (CVE-2015-5242). SSL grade is B.
6. **MySQL service exposed externally** -- MySQL (port 3306) is accessible from the network. It should be restricted to application-tier hosts only.
7. **Heartbleed flag** -- Script flagged Heartbleed as VULNERABLE (though noted as not exploitable with the current OpenSSL version). Manual verification recommended.

### Medium

8. **Missing security headers** -- Both HTTP (80) and HTTPS (443) are missing critical security headers: CSP, X-Frame-Options, X-Content-Type-Options. Port 80 is additionally missing HSTS and Referrer-Policy.
9. **Server version disclosure** -- nginx 1.24.0, PHP 8.2.14, and Apache Tomcat 10.1.18 versions are exposed in HTTP response headers.
10. **HTTP OPTIONS method enabled** -- OPTIONS method is enabled on ports 80 and 8080, which can be used for HTTP verb tampering.
11. **Tomcat PUT/DELETE enabled** -- PUT and DELETE methods are enabled on Tomcat (port 8080), allowing potential file upload/deletion if not properly configured.
12. **Session cookie missing Secure flag** -- The `session_id` cookie on port 80 has the HttpOnly flag but is missing the Secure flag, meaning it can be transmitted over plaintext HTTP.

### Low

13. **SSH password authentication enabled** -- SSH allows password-based authentication alongside publickey. Consider disabling password auth to prevent brute-force attacks.
14. **No WAF detected** -- Neither the HTTP (80) nor HTTPS (443) endpoints appear to be protected by a Web Application Firewall.

---

```json
{
  "target": "192.168.1.50",
  "scan_timestamp": "2026-04-11T14:22:05Z",
  "open_ports": [22, 80, 443, 3306, 8080],
  "services": {
    "22": "ssh OpenSSH 8.9p1 Ubuntu 3ubuntu0.6",
    "80": "http nginx 1.24.0",
    "443": "https nginx 1.24.0 (TLS 1.2/1.3)",
    "3306": "mysql MySQL 8.0.36",
    "8080": "http Apache Tomcat 10.1.18"
  },
  "os": "Linux 5.15 - 6.1 (Ubuntu 22.04 / 24.04) (96% confidence)",
  "nse_findings": {
    "22": {
      "auth_methods": ["publickey", "password", "keyboard-interactive"],
      "kex_algorithms": ["curve25519-sha256", "diffie-hellman-group-exchange-sha256", "diffie-hellman-group16-sha512", "diffie-hellman-group18-sha512"],
      "host_key_algorithms": ["rsa-sha2-512", "rsa-sha2-256", "ecdsa-sha2-nistp256", "ssh-ed25519"]
    },
    "80": {
      "http_title": "Welcome to MyApp Dashboard",
      "server_header": "nginx/1.24.0",
      "x_powered_by": "PHP/8.2.14",
      "missing_headers": ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"],
      "robots_disallowed": ["/admin/", "/backup/", "/config/", "/wp-admin/", "/.env"],
      "waf_detected": false
    },
    "443": {
      "ssl_grade": "B",
      "weak_ciphers": ["TLS_RSA_WITH_AES_128_CBC_SHA", "TLS_RSA_WITH_AES_256_CBC_SHA"],
      "heartbleed": "VULNERABLE (NOT exploitable with current OpenSSL version)",
      "cert_subject": "CN=webapp-staging.internal, O=MyApp Inc, ST=California, C=US",
      "cert_issuer": "CN=R3, O=Let's Encrypt, C=US",
      "cert_expiry": "2026-04-15T23:59:59",
      "cert_key_bits": 2048,
      "missing_headers": ["Content-Security-Policy", "X-Frame-Options"],
      "waf_detected": false
    },
    "3306": {
      "mysql_version": "8.0.36",
      "empty_password_root": true,
      "databases": ["information_schema", "myapp_production", "myapp_staging", "performance_schema", "sys"]
    },
    "8080": {
      "http_title": "Apache Tomcat/10.1.18 - Manager App",
      "server_header": "Apache-Coyote/1.1",
      "risky_methods": ["PUT", "DELETE", "OPTIONS"],
      "missing_headers": ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options"],
      "manager_exposed": true
    }
  },
  "notes": [
    "MySQL root account has empty password -- CRITICAL",
    "Tomcat Manager application exposed on port 8080 -- CRITICAL",
    "SSL certificate expires in 4 days (2026-04-15) -- CRITICAL",
    "robots.txt exposes sensitive paths including /.env -- CRITICAL",
    "Weak SSL ciphers detected (CBC mode, grade B) -- HIGH",
    "MySQL service exposed externally on port 3306 -- HIGH",
    "Heartbleed flagged for manual verification -- HIGH",
    "Missing security headers on HTTP and HTTPS -- MEDIUM",
    "Server version disclosure (nginx, PHP, Tomcat) -- MEDIUM",
    "HTTP OPTIONS method enabled on ports 80 and 8080 -- MEDIUM",
    "Tomcat PUT/DELETE methods enabled -- MEDIUM",
    "Session cookie missing Secure flag -- MEDIUM",
    "SSH password authentication enabled -- LOW",
    "No WAF detected on web endpoints -- LOW"
  ]
}
```
