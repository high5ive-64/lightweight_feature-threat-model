# Threat model: Webhook notifications for order events

## Feature summary
Send real-time order events to customer-configured webhook URLs.

## Assets
- Order data (PII, payment info)
- Customer webhook URLs
- Webhook secret tokens
- Event queue
- Delivery logs

## Trust boundaries
- Internal event processor to external webhook URL
- Database to event processor
- Admin configuration interface

## Threats

### 1. Webhook payload sent to unauthorized endpoint
- **STRIDE:** Information Disclosure
- **Severity:** High
- **Likelihood:** Medium
- **Scenario:** An attacker modifies the webhook URL configuration to redirect order events to their own server.
- **Impact:** Exposure of order data including PII and payment information to attacker-controlled server.
- **Mitigations:**
  - Require re-authentication for webhook URL changes
  - Send test payload and require confirmation before enabling webhooks
  - Log all webhook configuration changes
  - Implement webhook URL allowlisting or domain validation
- **Assumptions:**
  - Webhook URLs can be configured via admin UI or API

### 2. Webhook payload modified in transit
- **STRIDE:** Tampering
- **Severity:** High
- **Likelihood:** Low
- **Scenario:** An attacker intercepts and modifies webhook payloads if sent over unencrypted connection.
- **Impact:** Customer receives falsified order data, leading to incorrect fulfillment or fraud.
- **Mitigations:**
  - Enforce HTTPS for all webhook deliveries
  - Sign payloads with HMAC using shared secret
  - Include payload hash in signature
  - Implement retry logic with exponential backoff
- **Assumptions:**
  - Webhooks are delivered over public internet

### 3. Fake webhook callbacks from attacker
- **STRIDE:** Spoofing
- **Severity:** High
- **Likelihood:** Medium
- **Scenario:** An attacker sends fake webhook callbacks to customer endpoints impersonating our service.
- **Impact:** Customer acts on fraudulent events, leading to financial loss or data corruption.
- **Mitigations:**
  - Sign all webhook payloads with HMAC-SHA256
  - Include timestamp and reject old signatures (e.g., >5 minutes)
  - Document signature verification for customers
  - Use unique signing secrets per webhook endpoint
- **Assumptions:**
  - Customers verify webhook signatures

## Abuse cases
- Change webhook URL to attacker-controlled server to intercept order data
- Send fake webhook callbacks with fraudulent order events
- Flood webhook endpoint to trigger dead letter queue exhaustion

## Security questions
- How are webhook secrets generated and stored?
- What is the retry strategy for failed deliveries?
- Are webhook payloads logged and for how long?