# LexDesk Escalation Rules

## Overview

The LexDesk AI Support Agent handles the majority of customer inquiries automatically. However, certain situations require immediate human intervention. This document defines exactly when, how, and to whom tickets should be escalated.

---

## Escalation Tiers

### Tier 1 — AI Agent (Automatic)
Handles all routine inquiries without escalation:
- How-to questions
- Feature explanations
- Troubleshooting standard issues
- Account information requests
- Billing plan information (not disputes)

### Tier 2 — Support Team (Human)
Escalated by AI agent during business hours:
- Mon–Fri, 9AM–6PM EST (US customers)
- Mon–Fri, 9AM–6PM GMT (UK customers)
- Response time: Within 4 hours

### Tier 3 — Senior Support / Management
For critical or sensitive issues:
- Response time: Within 2 hours
- Available: Mon–Fri, 9AM–6PM EST/GMT

---

## Escalation Triggers

### 1. Financial Issues — ALWAYS ESCALATE

| Trigger | Examples | Escalation Category |
|---------|----------|-------------------|
| Refund request | "I want my money back", "please refund me" | `refund_request` |
| Billing dispute | "You charged me twice", "wrong amount charged" | `billing_dispute` |
| Pricing negotiation | "Can I get a discount?", "that's too expensive" | `pricing_inquiry` |
| Enterprise inquiry | "We have 30+ attorneys", "need custom pricing" | `enterprise_inquiry` |
| Chargeback threat | "I will dispute this with my bank" | `billing_dispute` |

**Rule:** Never discuss pricing adjustments, discounts, or refunds. Always escalate immediately.

---

### 2. Legal Threats — ALWAYS ESCALATE IMMEDIATELY

| Trigger | Examples | Escalation Category |
|---------|----------|-------------------|
| Legal action threat | "I will sue you", "my attorney will contact you" | `legal_matter` |
| Regulatory complaint | "I am reporting you to the FTC", "ICO complaint" | `legal_matter` |
| Data breach claim | "You leaked my client data" | `security_concern` |
| GDPR/CCPA request | "Delete all my data", "right to erasure" | `legal_matter` |
| Negligence claim | "Your software caused me to miss a court deadline" | `legal_matter` |

**Rule:** Do not engage with legal threats. Acknowledge, escalate, and inform the customer that a senior team member will respond.

---

### 3. Security Concerns — ESCALATE IMMEDIATELY

| Trigger | Examples | Escalation Category |
|---------|----------|-------------------|
| Account compromise | "Someone else is accessing my account" | `security_concern` |
| Data loss report | "My documents are missing/deleted" | `security_concern` |
| 2FA lockout | Customer locked out due to lost authenticator | `security_concern` |
| Unauthorized access | "I see logins from unknown locations" | `security_concern` |
| Suspected breach | "I think my account was hacked" | `security_concern` |

**Rule:** Security issues are always Priority 1. Escalate before attempting any troubleshooting.

---

### 4. High Frustration / Negative Sentiment — ESCALATE

| Signal | Examples | Escalation Category |
|--------|----------|-------------------|
| ALL CAPS messages | "THIS IS UNACCEPTABLE", "FIX THIS NOW" | `high_frustration` |
| Profanity | Any use of offensive language | `high_frustration` |
| Cancellation threat | "I am leaving LexDesk", "switching to Clio" | `high_frustration` |
| Repeated complaints | Same issue reported 3+ times | `high_frustration` |
| Emotional distress | "This is destroying my practice" | `high_frustration` |

**Rule:** Acknowledge the frustration empathetically before escalating. Never argue or be defensive.

---

### 5. Compliance and Regulatory — ALWAYS ESCALATE

| Trigger | Examples | Escalation Category |
|---------|----------|-------------------|
| GDPR right to erasure | "Delete all my personal data" | `legal_matter` |
| HIPAA inquiry | "Is LexDesk HIPAA compliant for our use case?" | `legal_matter` |
| SOC 2 audit request | "We need your SOC 2 report for our audit" | `legal_matter` |
| Bar compliance question | "Does LexDesk comply with ABA ethics rules?" | `legal_matter` |
| Data residency question | "Where exactly is our data stored?" | `legal_matter` |

---

### 6. Cannot Resolve — ESCALATE

| Trigger | Escalation Category |
|---------|-------------------|
| No relevant KB results after 2 searches | `technical_complex` |
| Customer reports same issue 3+ times | `technical_complex` |
| Bug report with reproducible steps | `technical_complex` |
| Feature not working as documented | `technical_complex` |
| Data integrity issue (missing/corrupted data) | `security_concern` |

---

### 7. Explicit Human Request — ALWAYS ESCALATE

| Trigger | Examples | Escalation Category |
|---------|----------|-------------------|
| Requests human agent | "I want to speak to a real person" | `explicit_request` |
| Requests manager | "Let me speak to your manager" | `explicit_request` |
| Rejects AI help | "I don't want to talk to a bot" | `explicit_request` |

**Rule:** Never try to convince the customer to stay with the AI. Escalate immediately and respectfully.

---

## Escalation Response Templates

### Financial Escalation
"I understand you have a billing concern. I'm escalating your request to our billing team who will reach out to you within 2 hours during business hours (Mon–Fri, 9AM–6PM EST). Your reference number is [TICKET_ID]. We appreciate your patience."

### Legal Threat Escalation
"I understand your concern and I take this very seriously. I'm immediately escalating your case to our senior team who will contact you within 2 hours. Your reference number is [TICKET_ID]. We are committed to resolving this for you."

### Security Escalation
"I'm treating this as a priority security matter and escalating immediately to our security team. Please do not attempt to log in further until our team contacts you. Your reference number is [TICKET_ID]. Expected response: within 2 hours."

### High Frustration Escalation
"I sincerely apologize for the experience you've had. This is not the standard we hold ourselves to. I'm escalating your case to a senior support specialist who will personally handle your case and contact you within 1 hour. Reference: [TICKET_ID]."

### Explicit Human Request
"Absolutely — I'm connecting you with a human support specialist right now. They will reach out to you at [EMAIL] within 4 hours during business hours. Your ticket reference is [TICKET_ID]."

---

## Response Time SLAs by Escalation Category

| Category | Response Time | Team |
|----------|--------------|------|
| `security_concern` | 2 hours | Security + Senior Support |
| `legal_matter` | 2 hours | Legal + Senior Management |
| `high_frustration` | 1 hour | Senior Support |
| `refund_request` | 2 hours | Billing Team |
| `billing_dispute` | 2 hours | Billing Team |
| `pricing_inquiry` | 4 hours | Sales Team |
| `enterprise_inquiry` | 4 hours | Sales Team |
| `technical_complex` | 4 hours | Technical Support |
| `explicit_request` | 4 hours | Support Team |

---

## Anti-Patterns (Do NOT Escalate)

**Handle These with AI:**
- Simple "how to" questions (covered in documentation)
- Password resets (standard process)
- General product questions
- Feature requests (acknowledge and log)
- Positive feedback
- Basic troubleshooting (syncing issues, refresh browser)

### Feature Requests
- **Do NOT escalate** unless it requires Enterprise custom development
- Log in ticket system
- Acknowledge: "Thank you for the suggestion! I've logged this for our product team."

### Competitor Comparisons
- **Do NOT discuss competitors**
- Focus on LexDesk capabilities
- If pressed, escalate with reason `competitor_inquiry`

### Bug Reports
- **Escalate only if:**
  - Data loss involved
  - Affects multiple users (potential outage)
  - Security vulnerability
- Otherwise: Log bug, provide workaround, set expectation for fix timeline

---

## What NOT to Do

- **Never** promise a refund or discount
- **Never** confirm or deny a security breach before investigation
- **Never** share internal system details or escalation procedures
- **Never** argue with an angry customer
- **Never** dismiss a legal threat — always escalate
- **Never** make the customer repeat their issue to a human — provide full context in escalation notes

---

## Success Metrics

**Target Escalation Rate:** < 20%

A well-functioning AI agent should resolve 80%+ of inquiries without human intervention. Monitor escalation rates and adjust the knowledge base accordingly.