# Threat model: Support ticket attachments

## Feature summary
Customers can upload files when submitting a support ticket.

## Threats

### 1. Malicious file upload bypasses validation
- **STRIDE:** Tampering
- **Severity:** High
- **Likelihood:** Medium
- **Scenario:** An attacker uploads a crafted file that bypasses content-type or extension checks and is later processed by downstream systems.
- **Impact:** Malware delivery, downstream processing compromise, or stored malicious content.
- **Mitigations:**
  - Validate file type server-side using magic bytes, not just extension
  - Scan all uploads with malware detection before processing
  - Store files outside direct web root with no direct URL access
  - Generate random object names to prevent enumeration
  - Implement file size limits (e.g., max 10MB)

### 2. Unauthorized access to uploaded files
- **STRIDE:** Information Disclosure
- **Severity:** High
- **Likelihood:** Medium
- **Scenario:** A user guesses or reuses file URLs and accesses attachments belonging to another customer.
- **Impact:** Exposure of PII or sensitive support content.
- **Mitigations:**
  - Enforce object-level authorization on every download request
  - Use short-lived signed URLs (e.g., 5-minute expiry)
  - Avoid predictable object identifiers in URLs
  - Log and alert on repeated access failures

### 3. File type masquerading attack
- **STRIDE:** Spoofing
- **Severity:** Medium
- **Likelihood:** Medium
- **Scenario:** An attacker uploads a file with a misleading extension (e.g., .exe renamed to .pdf) to trick downstream systems or users.
- **Impact:** Malware execution, phishing, or social engineering attacks.
- **Mitigations:**
  - Validate file content using magic bytes/file signatures
  - Display file type warnings to users when downloading
  - Set Content-Disposition: attachment to prevent inline execution
  - Use Content-Type headers that match actual file content

## Abuse cases
- Upload malware disguised as a document (e.g., .exe renamed to .pdf)
- Attempt IDOR against attachment download endpoints

## Security questions
- Are uploads scanned synchronously or asynchronously?
- Are attachments ever rendered inline in the browser?
- What file types and size limits are allowed?