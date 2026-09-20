# FlowSync Escalation Rules

## Overview

The FlowSync AI Support Agent handles the majority of customer inquiries automatically. However, certain situations require immediate human intervention. This document defines exactly when, how, and to whom tickets should be escalated.

---

## Escalation Tiers

### Tier 1 — AI Agent (Automatic)
Handles all routine inquiries without escalation:
- How-to questions and feature explanations
- Basic troubleshooting (login, sync, notifications)
- Account settings and configuration
- Integration setup guidance
- General billing questions (not disputes)
- Mobile app questions

### Tier 2 — Support Team (Human)
Escalated by AI agent during business hours:
- Mon–Fri, 9AM–6PM PST (Starter/Pro customers)
- Mon–Fri, 6AM–8PM PST (Business customers)
- Response time: Within 4 hours (Starter/Pro), 2 hours (Business)

### Tier 3 — Enterprise Support (Priority)
For Enterprise customers with SLA:
- 24/7 availability via dedicated Slack channel
- Response time: Within 30 minutes (SLA guarantee)
- Dedicated account team assigned

### Tier 4 — Engineering / Security
For critical technical or security issues:
- Data loss, security breaches, system-wide outages
- Response time: Immediate (within 15 minutes)
- On-call rotation 24/7

---

## Escalation Triggers

### 1. Financial Issues — ALWAYS ESCALATE

| Trigger | Examples | Escalation Category |
|---------|----------|-------------------|
| Refund request | "I want a refund", "charge me back" | `refund_request` |
| Billing dispute | "You charged me twice", "wrong amount billed" | `billing_dispute` |
| Enterprise pricing | "Need pricing for 500+ users", "custom contract" | `enterprise_inquiry` |
| Contract negotiation | "Can we sign annual contract?", "need MSA" | `contract_negotiation` |
| Payment failure | "Card declined but should work", "ACH failed" | `payment_issue` |
| Downgrade with data | "Cancel but keep data for X months" | `billing_dispute` |

**Rule:** Never discuss pricing adjustments, refunds, or contract terms. Always escalate immediately.

**Response time by category:**
- `refund_request`: 2 hours (Business team)
- `enterprise_inquiry`: 4 hours (Sales team)
- `contract_negotiation`: 4 hours (Sales team)
- `payment_issue`: 2 hours (Billing team)

---

### 2. Legal & Compliance — ALWAYS ESCALATE IMMEDIATELY

| Trigger | Examples | Escalation Category |
|---------|----------|-------------------|
| Legal action threat | "I will sue", "my lawyer will contact you" | `legal_matter` |
| Contract breach claim | "You violated our SLA", "breach of terms" | `legal_matter` |
| Data breach claim | "You exposed our data", "security incident" | `security_concern` |
| GDPR request | "Delete all my data", "right to erasure", "data export" | `gdpr_request` |
| CCPA request | "Do not sell my data", "California privacy rights" | `gdpr_request` |
| Subpoena / Legal order | "We received a subpoena about your service" | `legal_matter` |
| IP infringement | "Your service violates our patent/trademark" | `legal_matter` |
| Regulatory inquiry | "Compliance audit request", "SOC 2 report needed" | `compliance_inquiry` |

**Rule:** Do not engage with legal threats. Acknowledge, escalate, and inform customer that legal/compliance team will respond.

**Response time:** Within 2 hours for all legal matters.

---

### 3. Security Concerns — ESCALATE IMMEDIATELY

| Trigger | Examples | Escalation Category |
|---------|----------|-------------------|
| Account compromise | "Someone else accessed my account", "unauthorized login" | `security_concern` |
| Data loss report | "My projects are missing", "tasks deleted without permission" | `data_loss` |
| Data breach suspicion | "I think our data was leaked", "saw confidential info publicly" | `security_concern` |
| API key leaked | "Our API key was exposed in GitHub", "token compromised" | `security_concern` |
| Suspicious activity | "Strange API calls", "logins from unknown IPs" | `security_concern` |
| SSO issues | "SSO broken, can't access workspace", "SAML error" | `security_concern` |
| 2FA lockout | "Lost authenticator app, can't log in" | `security_concern` |

**Rule:** Security issues are Priority 1. Escalate before attempting any troubleshooting.

**Response time:** Within 30 minutes (immediate for Enterprise customers).

**Engineering involvement:** Yes — escalate to Security team + on-call engineer.

---

### 4. Critical Data Issues — ESCALATE IMMEDIATELY

| Trigger | Examples | Escalation Category |
|---------|----------|-------------------|
| Data loss | "All my tasks disappeared", "project deleted without permission" | `data_loss` |
| Sync failure affecting production | "GitHub integration broke, blocking deployments" | `technical_critical` |
| Automation causing damage | "Automation deleted 500 tasks by mistake" | `data_loss` |
| Export failure | "Cannot export data before leaving", "API timing out" | `technical_critical` |
| Data corruption | "Task descriptions showing wrong content" | `data_loss` |

**Rule:** Any data loss or corruption is critical. Escalate to Engineering immediately.

**Response time:** Within 15 minutes.

**Actions:**
- Freeze account to prevent further changes
- Engineering investigates backup/restore options
- Assign dedicated engineer

---

### 5. High Frustration / Negative Sentiment — ESCALATE

| Signal | Examples | Escalation Category |
|--------|----------|-------------------|
| ALL CAPS messages | "THIS IS UNACCEPTABLE", "FIX THIS NOW" | `high_frustration` |
| Profanity | Any use of offensive language | `high_frustration` |
| Churn threat | "Canceling and moving to Asana", "switching to Monday.com" | `churn_risk` |
| Repeated complaints | Same issue reported 3+ times without resolution | `high_frustration` |
| Public complaint threat | "Will post negative review", "tweeting about this" | `reputation_risk` |
| Executive escalation | "I'm the CTO and this is unacceptable" | `executive_escalation` |

**Rule:** Acknowledge the frustration empathetically before escalating. Never argue or be defensive.

**Response time:** Within 1 hour (immediate for executive escalations).

**Special handling for churn risks:**
- Tag customer account as "at-risk"
- Notify Customer Success Manager
- Offer call/screen share for resolution
- Consider goodwill credit (requires approval)

---

### 6. Enterprise / VIP Customers — PRIORITIZE

| Trigger | Escalation Category |
|---------|-------------------|
| Enterprise plan customer reports any issue | `enterprise_priority` |
| Customer paying > $10,000/year | `vip_customer` |
| Logos on marketing site (public customers) | `vip_customer` |
| During active sales cycle (potential large deal) | `sales_priority` |
| Customer with dedicated success manager | `enterprise_priority` |

**Rule:** Enterprise customers always get priority escalation, even for routine issues.

**Response time:** Within 30 minutes (per SLA).

**Routing:** Escalate to dedicated Enterprise Support team + notify CSM.

---

### 7. Integration Issues — ESCALATE IF CRITICAL

| Trigger | Examples | Escalation Category |
|---------|----------|-------------------|
| Integration completely broken | "GitHub integration not working at all" | `technical_complex` |
| Affecting production workflow | "Can't deploy because FlowSync-Jira sync is down" | `technical_critical` |
| API rate limit hit | "API returning 429 errors, blocking our automation" | `technical_complex` |
| Webhook not firing | "Webhooks stopped working, breaking our CI/CD" | `technical_complex` |
| SSO preventing team access | "No one can log in, SSO is broken" | `technical_critical` |

**Do NOT escalate if:**
- User needs help setting up integration (provide docs)
- One-time sync issue (suggest reconnect)
- User error in configuration (guide through setup)

**Escalate only if:**
- Issue affects multiple users
- Blocking production/critical workflows
- Integration fundamentally broken
- Requires engineering investigation

**Response time:** 
- Critical (blocking production): 1 hour
- Non-critical: 4 hours

---

### 8. Cannot Resolve — ESCALATE

| Trigger | Escalation Category |
|---------|-------------------|
| No relevant KB results after 2 searches | `technical_complex` |
| Customer reports same issue 3+ times | `technical_complex` |
| Bug with reproducible steps | `bug_report` |
| Feature not working as documented | `bug_report` |
| Performance degradation | `technical_complex` |
| API returning unexpected errors | `technical_complex` |

**Rule:** If you cannot find a solution in the knowledge base after 2 attempts, escalate to human support.

**Response time:** 4 hours (Starter/Pro), 2 hours (Business), 30 min (Enterprise).

---

### 9. Explicit Human Request — ALWAYS ESCALATE

| Trigger | Examples | Escalation Category |
|---------|----------|-------------------|
| Requests human agent | "I want to talk to a real person" | `explicit_request` |
| Requests manager/supervisor | "Let me speak to your manager" | `explicit_request` |
| Rejects AI help | "I don't want to talk to a bot" | `explicit_request` |
| Complex custom workflow | "Need help designing workflow for our specific process" | `consulting_request` |

**Rule:** Never try to convince the customer to stay with the AI. Escalate immediately and respectfully.

**Response time:** 4 hours (Starter/Pro), 2 hours (Business), 30 min (Enterprise).

---

### 10. Feature Requests / Product Feedback — LOG, DON'T ESCALATE

| Trigger | Examples | Action |
|---------|----------|--------|
| Feature request | "Can you add Gantt view export?" | Log to product feedback board |
| Product suggestion | "Would be great if automations could do X" | Acknowledge and log |
| UI/UX feedback | "The sidebar is confusing" | Thank and log |
| Competitor comparison | "Monday.com has this feature..." | Acknowledge gap, log request |

**Do NOT escalate** unless:
- Enterprise customer requesting critical custom feature
- Feature gap is blocking a large deal (notify Sales)
- Multiple customers requesting same feature (notify Product)

**Response:**
"Thank you for the suggestion! I've logged this for our product team to review. You can track feature requests and upvote at flowsync.io/feedback. We review these regularly during sprint planning."

---

## Escalation Response Templates

### Financial Escalation
"I understand you have a billing concern. I'm escalating your request to our billing team who will reach out to you within 2 hours during business hours (Mon–Fri, 9AM–6PM PST). Your reference number is [TICKET_ID]. We'll get this resolved for you."

### Legal / Compliance Escalation
"I take this matter very seriously. I'm immediately escalating your case to our legal and compliance team who will contact you within 2 hours. Your reference number is [TICKET_ID]. They will handle this with the attention it deserves."

### Security Escalation
"I'm treating this as a priority security matter and escalating immediately to our security team. Please do not make further changes to your account until our team contacts you. Your reference number is [TICKET_ID]. Expected response: within 30 minutes."

### Data Loss Escalation
"I understand how critical this is. I'm escalating this immediately to our engineering team with highest priority. They will investigate backup and recovery options and contact you within 15 minutes. Your reference number is [TICKET_ID]. In the meantime, please do not make changes to your workspace."

### High Frustration Escalation
"I sincerely apologize for the experience you've had. This is not the standard we hold ourselves to. I'm escalating your case to a senior support specialist who will personally handle this and contact you within 1 hour. Your reference number is [TICKET_ID]."

### Enterprise Customer Escalation
"I'm connecting you with your dedicated Enterprise Support team right now. Given your SLA agreement, they will respond within 30 minutes. Your reference number is [TICKET_ID]. Your Customer Success Manager has also been notified."

### Explicit Human Request
"Absolutely — I'm connecting you with a human support specialist right now. They will reach out to you at [EMAIL] within [TIMEFRAME based on plan]. Your ticket reference is [TICKET_ID]."

### Churn Risk Escalation
"I understand you're considering other options. I want to make sure we've done everything possible to help. I'm escalating this to our Customer Success team who will reach out within 1 hour to discuss your concerns and explore solutions. Your reference number is [TICKET_ID]."

---

## Response Time SLAs by Escalation Category

| Category | Response Time | Team | Plan Level |
|----------|--------------|------|-----------|
| `security_concern` | 30 minutes | Security + Engineering | All plans |
| `data_loss` | 15 minutes | Engineering | All plans |
| `technical_critical` | 1 hour | Engineering | All plans |
| `legal_matter` | 2 hours | Legal + Compliance | All plans |
| `gdpr_request` | 2 hours | Compliance | All plans |
| `high_frustration` | 1 hour | Senior Support | All plans |
| `churn_risk` | 1 hour | Customer Success | Business/Enterprise |
| `enterprise_priority` | 30 minutes | Enterprise Support | Enterprise only |
| `vip_customer` | 1 hour | Senior Support | All plans |
| `refund_request` | 2 hours | Billing Team | All plans |
| `billing_dispute` | 2 hours | Billing Team | All plans |
| `enterprise_inquiry` | 4 hours | Sales Team | All plans |
| `contract_negotiation` | 4 hours | Sales Team | All plans |
| `technical_complex` | 4 hours (S/P), 2 hours (B), 30 min (E) | Support Team | Varies by plan |
| `bug_report` | 4 hours | Engineering | All plans |
| `explicit_request` | 4 hours (S/P), 2 hours (B), 30 min (E) | Support Team | Varies by plan |

**Legend:** S/P = Starter/Pro, B = Business, E = Enterprise

---

## Anti-Patterns (Do NOT Escalate)

**Handle These with AI:**
- Simple "how to" questions (covered in documentation)
- Password resets (standard self-service process)
- General product questions
- Feature requests (log, don't escalate)
- Positive feedback (thank, no escalation needed)
- Basic troubleshooting (login, notifications, syncing)
- Integration setup guidance (follow docs)
- User configuration errors (guide through fix)

### Integration Questions
- **Do NOT escalate** if user just needs setup instructions
- Guide through: Settings > Integrations > [Service] > Connect
- Provide link to specific integration doc
- **Only escalate** if integration is fundamentally broken or affecting production

### Performance Questions
- **Do NOT escalate** for minor slowness
- Suggest: Clear cache, try different browser, check internet speed
- **Only escalate** if performance is severely degraded and affecting work

### Billing Questions
- **Do NOT escalate** for simple plan questions ("What's in Pro plan?")
- **Only escalate** for disputes, refunds, or custom contracts

---

## What NOT to Do

- **Never** promise a refund or discount
- **Never** confirm or deny a security breach before investigation
- **Never** share internal escalation procedures or engineering details
- **Never** argue with an angry customer
- **Never** dismiss a legal threat — always escalate
- **Never** make the customer repeat their issue to a human — provide full context in escalation notes
- **Never** downplay data loss or security concerns
- **Never** tell Enterprise customers to wait longer than their SLA
- **Never** suggest workarounds for critical production issues — escalate

---

## Special Handling: Enterprise Customers

**Always escalate if:**
- Customer explicitly states they're on Enterprise plan
- Email domain matches known Enterprise customer
- They mention having a dedicated CSM or account team
- Issue affects > 100 users
- Issue is blocking mission-critical workflows

**Escalation flow for Enterprise:**
1. Escalate to Enterprise Support team
2. CC dedicated Customer Success Manager
3. If after hours, page on-call Enterprise support
4. Include SLA reminder in escalation
5. Set ticket priority to "Critical"

**Response template:**
"As an Enterprise customer, I'm escalating this directly to your dedicated support team per your SLA agreement. They will respond within 30 minutes. Your Customer Success Manager [NAME] has also been notified. Reference number: [TICKET_ID]."

---

## Metrics & Success Targets

**Target Escalation Rate:** < 25% overall

Breakdown by plan:
- Starter: 30% (acceptable — simpler questions)
- Pro: 25%
- Business: 20%
- Enterprise: 15% (higher quality questions, better docs)

**Monitoring:**
- Track escalation rate by category
- Identify patterns for KB improvement
- Monthly review of escalation reasons
- Adjust automations to reduce false escalations

**Quality checks:**
- Random sample of 20 escalations/week
- Were they necessary?
- Could KB have prevented it?
- Did AI follow rules correctly?

---

## Escalation Data to Include

When escalating, always include:
1. **Customer info:**
   - Email, company name, plan level
   - Account age, lifetime value
   - Previous ticket history
2. **Issue details:**
   - Full conversation transcript
   - Screenshots/attachments if any
   - Attempted troubleshooting steps
3. **Context:**
   - How many times customer contacted about this
   - Related tickets
   - SLA requirements if applicable
4. **Urgency indicators:**
   - Production impact
   - Number of users affected
   - Customer sentiment (frustrated/neutral/polite)
   - Churn risk level

---

## Post-Escalation

**AI Agent responsibilities:**
- Send confirmation message with reference number and timeline
- Update ticket status to "escalated"
- Add internal note with escalation category
- Monitor for human team response
- Do NOT send automated follow-ups (human team handles)

**Human team responsibilities:**
- Acknowledge within SLA timeframe
- Take ownership of ticket
- Provide resolution or regular updates
- Close ticket when resolved
- Add resolution notes for AI learning
