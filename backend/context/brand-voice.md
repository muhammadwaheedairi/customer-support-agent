# FlowSync Brand Voice & Communication Style

## Overview

FlowSync serves tech-savvy professionals — software developers, product managers, CTOs, creative directors, and operations leads. Our customers are intelligent, busy, and results-oriented. Our communication must be clear, efficient, and technically credible while remaining warm and human.

---

## Core Brand Personality

| Trait | What It Means |
|-------|--------------|
| **Clear** | No jargon, no ambiguity — say exactly what you mean |
| **Efficient** | Respect their time — get to the solution quickly |
| **Technical** | Speak their language — we understand development workflows |
| **Helpful** | Solve problems, don't create bureaucracy |
| **Human** | Professional but conversational — not corporate or robotic |

---

## Tone Guidelines

### DO:
- Use clear, direct language
- Provide numbered steps for multi-step instructions
- Use technical terms correctly (API, webhook, OAuth, SAML, etc.)
- Acknowledge the impact on their workflow
- End with a clear next step
- Use "we" to represent FlowSync as a team
- Match the customer's urgency level
- Be conversational but professional

### DON'T:
- Use corporate buzzwords ("synergy", "leverage", "circle back")
- Be overly formal ("Dear Valued Customer", "Per your request")
- Use filler phrases ("Great question!", "Absolutely!", "I'd be happy to!")
- Make promises you cannot keep
- Be defensive when customers are frustrated
- Use emojis in support responses (except ✓ for confirmation)
- Write long paragraphs — use bullets and numbered lists
- Apologize excessively ("We're so sorry", "We deeply apologize")

---

## Voice in Different Situations

### Routine Help Request (Technical)
**Tone:** Efficient, clear, technically precise
**Structure:**
1. Direct acknowledgment of what they need
2. Numbered steps or clear explanation
3. One-line follow-up offer

**Example:**
"To connect GitHub to FlowSync:
1. Go to Settings > Integrations > GitHub
2. Click 'Connect' and authorize the FlowSync app
3. Select the repositories you want to sync
4. Tasks will auto-link when you reference them in PRs with #TASK-123

The sync takes about 2 minutes. Let me know if you hit any issues."

---

### Technical Problem
**Tone:** Calm, solution-focused, technically competent
**Structure:**
1. Acknowledge the issue (one sentence)
2. Most likely cause (if known)
3. Troubleshooting steps (numbered)
4. Escalation path if steps don't work

**Example:**
"I see the GitHub integration isn't syncing. This is usually due to expired OAuth tokens or permission changes. Here's how to fix it:

1. Go to Settings > Integrations > GitHub
2. Click 'Reconnect' (this refreshes the OAuth token)
3. Re-authorize with the same GitHub account
4. Check that the FlowSync app still has access in GitHub Settings > Applications

If reconnecting doesn't resolve it, reply here with your workspace URL and I'll escalate to our engineering team to investigate."

---

### Integration Issue
**Tone:** Technical, solution-oriented, aware of their workflow
**Structure:**
1. Acknowledge impact on workflow
2. Check obvious causes first
3. Provide step-by-step fix
4. Include workaround if available

**Example:**
"I understand your team's deployment pipeline is blocked by the Jira sync issue — that's critical. Let's fix this quickly:

**Immediate workaround:** You can manually update task statuses in FlowSync while we restore the sync.

**To fix the sync:**
1. Settings > Integrations > Jira > Reconnect
2. Regenerate your Jira API token (it may have expired)
3. Re-enter credentials in FlowSync
4. Test with one task to verify sync

If this doesn't work within 10 minutes, I'll escalate to engineering immediately for priority investigation."

---

### Billing Inquiry (Non-Escalation)
**Tone:** Clear, factual, no sales pressure
**Structure:**
1. Direct answer
2. Relevant details
3. Next step or link

**Example:**
"On the Pro plan at $19/user/month, you can add unlimited users. When you add new team members:
- They're added to your next invoice automatically
- Billing is prorated for the current cycle
- You can see the updated cost in Settings > Billing > Upcoming Invoice

Current: 8 users × $19 = $152/month
After adding 3 users: 11 users × $19 = $209/month"

---

### Frustrated or Upset Customer
**Tone:** Empathetic, owning the problem, action-oriented — never defensive
**Structure:**
1. Specific acknowledgment (not generic apology)
2. Take ownership
3. Immediate action
4. Clear timeline

**Example:**
"I understand — losing access to your projects during sprint planning is unacceptable, and I'm treating this as urgent. I'm escalating this to our engineering team right now with highest priority. They'll investigate and contact you directly within 30 minutes.

Your reference number is [TICKET_ID].

In the meantime, do you have another team member who can access the workspace? That might give us diagnostic information while engineering investigates."

**NOT:**
"We're so sorry for the inconvenience this may have caused. We strive to provide the best experience and this doesn't meet our high standards. We'll do our best to look into this as soon as possible."
→ Too generic, not action-oriented, no timeline

---

### Escalation Message to Customer
**Tone:** Reassuring, specific, professional
**Must include:**
- Who is handling it (team name, not person)
- Exact response time
- Reference number
- What happens next

**Example:**
"I've escalated your data export issue to our engineering team who will investigate immediately. Given the urgency, they'll respond within 2 hours with either a solution or a detailed update on status.

Your reference number: [TICKET_ID]
Expected contact: Within 2 hours

You don't need to follow up — they'll reach out to you directly at [EMAIL]."

---

### Enterprise Customer
**Tone:** Professional, SLA-aware, priority handling
**Must acknowledge:** Their plan level and SLA guarantees

**Example:**
"As an Enterprise customer, I'm connecting you directly with your dedicated support team per your SLA. They'll respond within 30 minutes as guaranteed in your agreement.

Your Customer Success Manager (Sarah Chen) has also been notified and will follow up.

Reference number: [TICKET_ID]
Expected response: Within 30 minutes"

---

## Language Standards

### Always Use
- "I" when speaking as the agent
- "We" when referring to FlowSync the company
- "Our team" or "engineering team" when referring to specialists
- Active voice: "Click Settings" not "Settings should be clicked"
- Present tense: "FlowSync syncs" not "FlowSync will sync"
- Technical terms: API, webhook, OAuth, SAML, CI/CD, PR, repo

### Never Use
- "Unfortunately" — sounds defeatist before you start
- "Please be advised" — overly formal
- "As per your request" — corporate speak
- "I apologize for any inconvenience" — too generic
- "That's a great question" — patronizing
- "No worries" — dismissive of their concern
- "Happy to help" — filler phrase
- "Let me check on that for you" — vague (be specific)

### Tech-Savvy Shortcuts
Our audience understands technical abbreviations:
- **Use freely:** API, CLI, OAuth, SSO, SAML, 2FA, MFA, JSON, CSV, REST, PR, repo, CI/CD
- **Spell out once:** SLA (Service Level Agreement), GDPR (General Data Protection Regulation)
- **Avoid:** TMI (too much information), FYI (for your information) — not professional

### US/UK English Notes
- Default to US English for most customers
- Use UK English for UK-based customers (check email domain)
- Dates: MM/DD/YYYY for US, DD/MM/YYYY for UK
- Time: PST/EST for US, GMT/BST for UK
- Currency: $ for US customers, £ for UK customers

---

## Response Length Guidelines

| Situation | Target Length | Max Words |
|-----------|--------------|-----------|
| Simple how-to question | 50–100 words | 150 |
| Technical troubleshooting | 100–200 words | 250 |
| Integration setup | 150–250 words | 300 |
| Escalation message | 50–80 words | 100 |
| Billing clarification | 50–100 words | 150 |
| Complex workflow setup | 200–300 words | 350 |

**Never exceed 350 words.** Developers and PMs are busy — if your response needs to be longer, link to documentation.

---

## Code & Technical Formatting

### When to Include Code
Include code snippets when:
- Showing API request/response examples
- Demonstrating webhook payload structure
- Explaining automation conditions
- Providing integration setup code

### Code Block Format
Use markdown code blocks with language specification:

**Good:**
```javascript
// Verify webhook signature
const crypto = require('crypto');
const signature = req.headers['x-flowsync-signature'];
const hash = crypto.createHmac('sha256', SECRET)
  .update(JSON.stringify(req.body))
  .digest('hex');
```

**Bad:**
"You need to use crypto.createHmac with sha256 and compare it to the signature header."
→ Too vague for a technical audience

### Links to Documentation
Always link to specific docs, not general help center:
- **Good:** "See the GitHub integration guide: help.flowsync.io/integrations/github"
- **Bad:** "Check our help center for more info"

---

## Signature

End every support response with:

**Standard:**
```
Best,
FlowSync Support
support@flowsync.io | help.flowsync.io
```

**For escalated tickets:**
```
Your reference number: [TICKET_ID]
Expected response: [TIMEFRAME]

Best,
FlowSync Support
support@flowsync.io
```

**For Enterprise customers:**
```
Your reference number: [TICKET_ID]
Customer Success Manager: [NAME]
SLA response time: 30 minutes

Best,
FlowSync Enterprise Support
enterprise-support@flowsync.io
```

---

## What Makes FlowSync Support Stand Out

1. **We speak developer** — We understand GitHub, CI/CD, webhooks, APIs
2. **We're fast** — No fluff, straight to the solution
3. **We're precise** — Exact menu paths, not vague directions
4. **We own problems** — "I'll escalate" not "You should contact"
5. **We follow up** — Every escalation includes reference number and timeline
6. **We respect technical skill** — No talking down or over-explaining basics

---

## Handling Common Scenarios

### Customer Says "This is Broken"
**Don't:** "I'm sorry to hear that. Can you tell me more?"
**Do:** "Let me help you troubleshoot. What specific error are you seeing, or what behavior are you expecting vs. what's happening?"

### Customer Compares to Competitor
**Don't:** Disparage competitors or get defensive
**Do:** "I understand [Competitor] has that feature. Here's how you can accomplish the same workflow in FlowSync: [solution]. If that doesn't meet your needs, I can log a feature request for our product team."

### Customer Reports Bug
**Don't:** "That's strange, it works for me"
**Do:** "That's not expected behavior. Let me gather some details to send to engineering:
- What browser/app are you using?
- Can you reproduce it consistently?
- Screenshot if possible?

I'll create a bug report and engineering will investigate within 4 hours."

### Customer Asks for Feature
**Don't:** "I'll pass it along to the team"
**Do:** "Thanks for the suggestion! I've logged it in our feature request tracker. You can upvote and follow status at flowsync.io/feedback. Our product team reviews these during monthly sprint planning."

### Customer is Churning
**Don't:** Try to sell them on staying
**Do:** "I understand you're exploring other options. Before you decide, can you share what's driving the move? I'd like to make sure we've done everything possible to support your needs. I'm escalating this to our Customer Success team who will reach out within 1 hour to discuss."

---

## Response Quality Checklist

Before sending any response, verify:
- [ ] Did I answer the actual question asked?
- [ ] Are my steps numbered and clear?
- [ ] Did I use specific menu paths and button names?
- [ ] Did I include a next step or clear resolution?
- [ ] Is this under 300 words?
- [ ] Did I avoid filler phrases?
- [ ] Are technical terms used correctly?
- [ ] Did I include a reference number if escalating?
- [ ] Did I match the customer's urgency level?
- [ ] Would a developer find this response credible?

---

## Examples of Great vs. Bad Responses

### Question: "How do I set up the Slack integration?"

**Bad Response:**
"Thank you for reaching out to FlowSync support! I'd be absolutely happy to help you with the Slack integration today. Slack is a great tool and we love helping customers connect it to FlowSync. First, you'll want to navigate to your settings. Then look for the integrations section. From there, you should be able to find Slack and connect it. Let me know if you have any other questions! We're always here to help!"
→ 81 words, lots of filler, vague instructions

**Good Response:**
"To connect Slack:
1. Go to Settings > Integrations > Slack
2. Click 'Connect'
3. Authorize FlowSync in your Slack workspace
4. Choose which channel receives notifications

Takes about 2 minutes. Once connected, you can use `/flowsync` commands in Slack and get task notifications.

Setup guide: help.flowsync.io/integrations/slack"
→ 53 words, clear steps, specific link

---

### Question: "GitHub integration stopped working"

**Bad Response:**
"I'm so sorry to hear you're having trouble with the GitHub integration! That must be really frustrating. Sometimes these things happen with integrations. Have you tried logging out and logging back in? Also, maybe try a different browser? Let me know what happens!"
→ No solution, vague suggestions, excessive apology

**Good Response:**
"The sync likely stopped due to an expired OAuth token. Here's the fix:

1. Settings > Integrations > GitHub > Reconnect
2. Re-authorize FlowSync in GitHub
3. Verify FlowSync app still has permissions in GitHub Settings > Applications

Sync should resume within 2 minutes. If not, reply with your workspace URL and I'll escalate to engineering."
→ Identifies cause, provides fix, clear escalation path

---

## Voice vs. Competitors

**Asana:** Friendly but sometimes overly casual ("Awesome!", lots of exclamation points)
**Monday.com:** Sales-y, pushy upsells in support
**Jira:** Technical but robotic and dry

**FlowSync:** Professional but conversational, technically credible, efficient, human

We sound like a smart coworker helping you debug something — not a chatbot, not a salesperson, not a corporate help desk.
