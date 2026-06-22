# TaskFlow - Escalation Rules

## When to Escalate to Human Support

The AI agent must escalate to human support immediately when ANY of the following conditions are met:

## 1. Pricing & Financial Matters

**ALWAYS ESCALATE:**
- Pricing negotiations or custom pricing requests
- Refund requests
- Billing disputes or incorrect charges
- Payment method issues requiring manual intervention
- Enterprise plan inquiries (custom pricing)
- Contract negotiations

**Examples:**
- "I want a refund"
- "Can you give us a discount for 100 users?"
- "I was charged twice"
- "What's the Enterprise pricing?"

## 2. Legal & Compliance

**ALWAYS ESCALATE:**
- Legal threats or mentions of lawyers
- GDPR, CCPA, or compliance documentation requests
- Data breach concerns
- Terms of Service disputes
- Privacy policy questions requiring legal review
- Security audit requests from legal teams

**Trigger Words:**
- "lawyer", "legal", "sue", "attorney", "litigation"
- "GDPR", "CCPA", "compliance audit"
- "data breach", "security incident"

## 3. Negative Sentiment

**ESCALATE IF:**
- Customer uses profanity or aggressive language
- ALL CAPS messages with angry tone
- Multiple frustrated messages in succession
- Sentiment score < 0.3 (calculated from message content)
- Threats to cancel or switch competitors

**Examples:**
- "This is RIDICULOUS!"
- "I'm DONE with TaskFlow!"
- Messages with excessive exclamation marks and anger

## 4. Cannot Resolve After Attempts

**ESCALATE IF:**
- Cannot find relevant information after 2 knowledge base searches
- Customer reports the same issue 3+ times without resolution
- Technical issue beyond agent's capability
- Requires system access or backend changes

## 5. Explicit Human Request

**ALWAYS ESCALATE:**
- Customer explicitly asks for human support
- "I want to speak to a real person"
- "Can I talk to a human?"
- "Transfer me to your manager"

## 6. Account & Security Issues

**ESCALATE IF:**
- Account lockout/suspension issues
- Suspected unauthorized access
- Password reset failures (after basic troubleshooting)
- SSO configuration (Enterprise feature)
- API security concerns

## 7. Data & Privacy

**ESCALATE IF:**
- Account deletion requests (GDPR right to erasure)
- Data export for legal purposes
- Questions about data retention policies
- Concerns about data location/sovereignty

## Escalation Process

### 1. Acknowledge & Explain

"I understand this requires specialized attention. I'm escalating your request to our human support team who will respond within [timeframe]."

### 2. Create Escalated Ticket

- Mark ticket status as "escalated"
- Add escalation reason and category
- Include full conversation history
- Assign appropriate priority level

### 3. Set Expectations

**Response Timeframes:**
- **High Priority** (billing, legal, security): 2 hours
- **Medium Priority** (complex technical): 4 hours  
- **Low Priority** (general inquiries): 24 hours

### 4. Provide Ticket Reference

"Your ticket reference is [TICKET_ID]. Our team will contact you at [EMAIL] within [TIMEFRAME]."

## Escalation Categories

When escalating, use these categories:

- `pricing_inquiry` - Custom pricing, discounts, Enterprise plans
- `refund_request` - Any refund or billing dispute
- `legal_matter` - Legal threats, compliance, GDPR
- `high_frustration` - Angry customer, negative sentiment
- `technical_complex` - Cannot resolve technically
- `security_concern` - Account security, data breach
- `explicit_request` - Customer asked for human

## Anti-Patterns (Do NOT Escalate)

**Handle These with AI:**
- Simple "how to" questions (covered in documentation)
- Password resets (standard process)
- General product questions
- Feature requests (acknowledge and log)
- Positive feedback
- Basic troubleshooting (syncing issues, refresh browser)

## Special Cases

### Feature Requests
- **Do NOT escalate** unless Enterprise custom development
- Log in ticket system
- Acknowledge: "Thank you for the suggestion! I've logged this for our product team."

### Competitor Comparisons
- **Do NOT discuss competitors**
- Focus on TaskFlow capabilities
- If pressed, escalate with reason `competitor_inquiry`

### Bug Reports
- **Escalate only if:**
  - Data loss involved
  - Affects multiple users (potential outage)
  - Security vulnerability
- Otherwise: Log bug, provide workaround, set expectation for fix timeline

## Success Metrics

**Target Escalation Rate:** < 20%

A well-functioning AI agent should resolve 80%+ of inquiries without human intervention. Monitor escalation rates and adjust knowledge base accordingly.
