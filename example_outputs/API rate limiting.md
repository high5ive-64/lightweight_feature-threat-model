# Threat model: API rate limiting by API key

## Feature summary
Enforce per-key rate limits on API endpoints to prevent abuse.

## Assets
- API keys and secrets
- Rate limit counters
- Usage metrics
- Client IP addresses

## Trust boundaries
- API gateway to rate limiter
- Rate limiter to data store
- Admin dashboard to rate limit config

## Threats

### 1. Rate limit bypass via key rotation
- **STRIDE:** Denial of Service
- **Severity:** Medium
- **Likelihood:** Medium
- **Scenario:** An attacker rapidly rotates API keys to bypass per-key rate limits.
- **Impact:** Rate limiting becomes ineffective, allowing API abuse.
- **Mitigations:**
  - Implement rate limits at multiple levels (key, IP, account)
  - Add rate limit on key creation itself
  - Track usage patterns across key rotations
  - Implement anomaly detection for unusual key usage
- **Assumptions:**
  - API keys can be created programmatically

### 2. Rate limit configuration tampering
- **STRIDE:** Elevation of Privilege
- **Severity:** High
- **Likelihood:** Low
- **Scenario:** An attacker modifies their own rate limit configuration via API parameter manipulation.
- **Impact:** Attacker gains higher rate limits than entitled, enabling abuse.
- **Mitigations:**
  - Never trust client-provided rate limit values
  - Enforce rate limits server-side only
  - Audit all rate limit configuration changes
  - Separate rate limit config from API endpoints
- **Assumptions:**
  - Rate limits are configurable per tier

### 3. Rate limit counter manipulation
- **STRIDE:** Tampering
- **Severity:** High
- **Likelihood:** Low
- **Scenario:** An attacker manipulates rate limit counters stored in Redis or similar data store.
- **Impact:** Rate limiting bypassed or legitimate users unfairly blocked.
- **Mitigations:**
  - Use atomic operations for counter updates
  - Secure data store with authentication and network isolation
  - Implement counter integrity checks
  - Monitor for unusual counter patterns
- **Assumptions:**
  - Rate limit counters stored in Redis or similar

## Abuse cases
- Create multiple API keys to bypass per-key rate limits
- Manipulate rate limit configuration via API parameter injection
- Flood API with requests just under rate limit threshold

## Security questions
- What rate limiting algorithm is used (fixed window, sliding window, token bucket)?
- How are rate limit counters persisted and synced?
- What happens when rate limit is exceeded (429, queue, degrade)?