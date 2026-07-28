# Threat model: SAML SSO integration for enterprise customers

## Feature summary
Enable enterprise customers to authenticate via their identity provider.

## Assets
- SAML assertions and tokens
- User session data
- IdP metadata and certificates
- User attribute mappings
- Audit logs

## Trust boundaries
- External IdP to application SSO endpoint
- SSO service to user session store
- Admin configuration interface

## Threats

### 1. SAML assertion forgery
- **STRIDE:** Spoofing
- **Severity:** Critical
- **Likelihood:** Medium
- **Scenario:** An attacker creates a forged SAML assertion to impersonate a legitimate user.
- **Impact:** Unauthorized access to user accounts, potential admin access.
- **Mitigations:**
  - Validate SAML signatures using IdP certificate
  - Enforce strict audience restriction (Your entity ID)
  - Verify assertion timestamps (NotBefore, NotOnOrAfter)
  - Implement certificate pinning for IdP certificates
  - Use SAML encryption for sensitive assertions
- **Assumptions:**
  - SAML assertions are received from external IdPs

### 2. Attribute manipulation for privilege escalation
- **STRIDE:** Elevation of Privilege
- **Severity:** Critical
- **Likelihood:** Medium
- **Scenario:** An attacker modifies SAML attributes to gain elevated privileges (e.g., admin role).
- **Impact:** Attacker gains admin or elevated access to application.
- **Mitigations:**
  - Never trust client-provided role or group attributes
  - Map IdP attributes to roles server-side only
  - Implement strict attribute allowlisting
  - Audit role assignments and changes
  - Use separate admin authentication flow
- **Assumptions:**
  - User roles are derived from SAML attributes

### 3. Missing SSO audit trail
- **STRIDE:** Repudiation
- **Severity:** Medium
- **Likelihood:** Low
- **Scenario:** SSO logins are not properly logged, preventing investigation of unauthorized access.
- **Impact:** Inability to detect or investigate security incidents.
- **Mitigations:**
  - Log all SSO authentication attempts with timestamps
  - Include IdP, user ID, and session ID in logs
  - Store logs in immutable storage
  - Alert on unusual SSO patterns (e.g., multiple IdPs for same user)
- **Assumptions:**
  - SSO logins are currently not logged

## Abuse cases
- Forge SAML assertion to impersonate admin user
- Manipulate SAML attributes to escalate privileges
- Replay captured SAML assertion for unauthorized access

## Security questions
- Which SAML profile is supported (SP-initiated, IdP-initiated, or both)?
- How are IdP certificates managed and rotated?
- What happens when SSO fails (fallback to local auth)?