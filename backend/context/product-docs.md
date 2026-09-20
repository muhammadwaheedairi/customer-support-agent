# FlowSync Product Documentation

## Getting Started & Onboarding

### Create Your First Account

To get started with FlowSync:
1. Go to flowsync.io/signup
2. Enter your work email address
3. Choose your plan (14-day free trial included)
4. Create your workspace name (e.g., "Acme Engineering")
5. Invite your team members via email

Your workspace URL will be: `acmengineering.flowsync.io`

### Initial Workspace Setup

After creating your account:
1. Navigate to Settings > Workspace Settings
2. Upload your company logo
3. Set your timezone and working hours
4. Configure notification preferences
5. Import existing data from Asana, Trello, or CSV

### Invite Team Members

To invite team members:
1. Go to Settings > Team Members
2. Click "Invite Members"
3. Enter email addresses (comma-separated for bulk)
4. Choose their role: Owner, Admin, Member, or Guest
5. Click "Send Invitations"

Team members will receive an email with a signup link.

### Understanding Roles

**Owner:**
- Full workspace access
- Billing and subscription management
- Can delete workspace
- Only one owner per workspace (transferable)

**Admin:**
- Create/edit/delete projects
- Manage team members and permissions
- Access all projects
- Configure integrations and automations

**Member:**
- Access assigned projects
- Create tasks and comments
- Use integrations
- Cannot manage billing or team settings

**Guest:**
- Limited to specific projects
- Cannot see other projects
- Cannot invite others
- Ideal for clients or contractors

---

## Task & Project Management

### Create a New Project

1. Click the "+" icon in the sidebar
2. Select "New Project"
3. Choose a project template or start blank
4. Add project name and description
5. Set privacy (Team-wide or Private)
6. Click "Create Project"

### Project Views

FlowSync offers 5 views for every project:

**Board View:**
- Kanban-style columns
- Drag and drop tasks between stages
- Perfect for agile workflows
- Customize columns: Add, rename, reorder

**List View:**
- Linear task list with sorting and filtering
- Fastest for bulk task creation
- Grouping by assignee, status, priority, or custom field

**Timeline View:**
- Gantt chart visualization
- See task dependencies and blockers
- Drag tasks to adjust dates
- Critical path highlighting

**Calendar View:**
- See all tasks with due dates
- Drag to reschedule
- Monthly, weekly, or daily views
- Sync with Google Calendar or Outlook

**Gantt View (Business/Enterprise only):**
- Advanced project planning
- Resource allocation
- Milestone tracking
- Baseline comparison

### Create Tasks

To create a task:
1. Click "+ Add Task" in any view
2. Enter task title
3. Press Enter to save, or click to expand for details:
   - Assignee
   - Due date
   - Priority (Low, Medium, High, Urgent)
   - Tags
   - Custom fields
   - Description with markdown support
   - Attachments (up to 100MB per file)

**Keyboard shortcut:** Press `C` anywhere to quick-create a task

### Task Dependencies

Set dependencies to control task order:
1. Open a task
2. Click "Add Dependency"
3. Search for the blocking task
4. Choose relationship:
   - **Blocks:** This task must finish before the other starts
   - **Blocked by:** This task cannot start until the other finishes
   - **Related to:** Informational link only

Dependencies show in Timeline and Gantt views.

### Subtasks

Break down complex tasks:
1. Open a task
2. Click "+ Add Subtask"
3. Enter subtask title
4. Subtasks inherit parent task's project and assignee (editable)

Progress bar shows completion percentage based on subtasks.

### Task Templates

Save time with reusable templates:
1. Create a task with all details
2. Click task menu (•••) > "Save as Template"
3. Name your template (e.g., "Bug Report Template")
4. Use it: Click "+ Add Task" > "From Template"

Templates include custom fields, checklists, and description formatting.

---

## Workflows & Automations

### Understanding Automations

Automations trigger actions based on events. Available on Pro plans and above.

### Create an Automation

1. Go to Project Settings > Automations
2. Click "Create Automation"
3. Choose a trigger:
   - Task created
   - Status changed
   - Due date approaching
   - Task assigned
   - Priority changed
   - Custom field updated
4. Add conditions (optional):
   - If assignee is...
   - If priority is...
   - If tag contains...
5. Add actions:
   - Send notification
   - Change status
   - Assign to someone
   - Add comment
   - Create subtask
   - Send to Slack
6. Click "Save Automation"

### Popular Automation Examples

**Auto-escalate overdue tasks:**
- Trigger: Due date is past
- Condition: Status is not "Done"
- Action: Set priority to "Urgent" and notify project admin

**Welcome new team members:**
- Trigger: Team member added
- Action: Assign onboarding checklist and send Slack message

**Bug triage workflow:**
- Trigger: Task created with tag "bug"
- Action: Assign to QA lead and move to "Triage" status

**Sprint reminders:**
- Trigger: 2 days before due date
- Condition: Status is "In Progress"
- Action: Send Slack notification to assignee

### Recurring Tasks

Set up tasks that repeat:
1. Create a task
2. Click "Set Recurrence"
3. Choose frequency:
   - Daily, Weekly, Monthly, Yearly
   - Custom (e.g., "Every 2 weeks on Monday")
4. Set end condition:
   - Never
   - After X occurrences
   - On a specific date

New instances create automatically when the previous is completed.

### Custom Approval Workflows

Create multi-step approval processes (Business/Enterprise):
1. Go to Workspace Settings > Workflows
2. Click "Create Approval Workflow"
3. Define stages (e.g., "Designer Review → PM Approval → Dev")
4. Set approvers for each stage
5. Configure actions on approval/rejection
6. Apply workflow to specific projects or task types

---

## Team Management & Permissions

### Manage Team Members

View all team members:
1. Go to Settings > Team Members
2. See status: Active, Invited, Deactivated
3. Click a member to:
   - Change role
   - Deactivate account
   - View activity history

### Project-Level Permissions

Control who can access projects:
1. Open Project Settings
2. Click "Members & Permissions"
3. Add members and set permissions:
   - **Can Edit:** Full access (create, edit, delete)
   - **Can Comment:** View and comment only
   - **View Only:** Read-only access

Projects default to "Team-wide" (all members) or "Private" (invited only).

### Guest Access

Invite external collaborators:
1. Go to Project Settings > Members
2. Click "Invite Guest"
3. Enter email and set project access
4. Guests see only their assigned projects

**Guest limitations:**
- Cannot see team directory
- Cannot access workspace settings
- Cannot invite others
- 5 guests free; unlimited on Business/Enterprise

### Single Sign-On (Enterprise)

Set up SSO:
1. Go to Workspace Settings > Security
2. Click "Configure SSO"
3. Choose provider: Okta, Azure AD, OneLogin, Google Workspace
4. Enter SAML 2.0 metadata
5. Map user attributes
6. Test SSO login
7. Enable for all users or specific domains

**Supported SSO providers:**
- Okta
- Azure Active Directory
- OneLogin
- Google Workspace
- Auth0
- Custom SAML 2.0

---

## Integrations

### Slack Integration

Connect FlowSync to Slack:
1. Go to Settings > Integrations
2. Click "Connect" next to Slack
3. Authorize FlowSync app in your Slack workspace
4. Choose default channel for notifications

**Slack commands:**
- `/flowsync create [task name]` — Create task from Slack
- `/flowsync search [query]` — Search tasks
- `/flowsync due today` — Show tasks due today

**Notification settings:**
- Per-project: Choose Slack channel in Project Settings
- Personal: Get DMs for assigned tasks, mentions, due dates
- Customize: Mute specific notification types

### GitHub Integration

Connect GitHub repositories:
1. Go to Settings > Integrations > GitHub
2. Click "Connect GitHub"
3. Authorize FlowSync app
4. Select repositories to connect
5. Map repositories to projects

**Features:**
- Link pull requests to tasks (use `#TASK-123` in PR description)
- Auto-update task status when PR merges
- See PR status in task view
- Create tasks from GitHub issues
- Branch naming from tasks

**GitHub Actions:**
When PR references a task:
- Task status changes to "In Review"
- PR link appears in task
- Comments on PR sync to task
- Merge triggers "Done" status (configurable)

### GitLab Integration

Similar to GitHub:
1. Settings > Integrations > GitLab
2. Enter GitLab instance URL (gitlab.com or self-hosted)
3. Generate personal access token in GitLab
4. Paste token in FlowSync
5. Select projects to sync

Use `Closes #TASK-123` in merge request description to auto-complete tasks.

### Jira Integration

Sync with existing Jira projects:
1. Go to Settings > Integrations > Jira
2. Click "Connect Jira"
3. Enter Jira URL and API token
4. Map Jira projects to FlowSync projects
5. Choose sync direction:
   - One-way: Jira → FlowSync (read-only)
   - Two-way: Full bidirectional sync

**Field mapping:**
- Jira Issue Type → FlowSync Custom Field
- Jira Status → FlowSync Status
- Jira Priority → FlowSync Priority
- Comments and attachments sync automatically

**Note:** Two-way sync requires Business or Enterprise plan.

### Google Drive Integration

Attach files from Google Drive:
1. Connect: Settings > Integrations > Google Drive
2. Authorize FlowSync to access Drive
3. In any task, click "Attach from Google Drive"
4. Browse and select files
5. Files appear as links (not copies)

Changes in Drive reflect in FlowSync automatically.

### Zapier Integration

Automate with 5,000+ apps:
1. Go to zapier.com
2. Search "FlowSync"
3. Create a Zap with FlowSync triggers/actions

**Popular Zaps:**
- Gmail → Create task from starred emails
- Typeform → Create task from form submission
- HubSpot → Sync deals with FlowSync projects
- Twitter → Create task from mentions

**Available triggers:**
- New task created
- Task completed
- Task assigned
- Due date approaching

**Available actions:**
- Create task
- Update task
- Add comment
- Create project

---

## Reporting & Analytics

### Project Dashboard

Every project has a real-time dashboard:
- Tasks by status (pie chart)
- Tasks by assignee (bar chart)
- Completion rate over time (line graph)
- Overdue tasks count
- Average time to completion

Access: Click "Dashboard" tab in any project.

### Workload View

See team capacity:
1. Go to Home > Workload
2. View by: Week, Month, or Custom range
3. See each person's task count and estimated hours
4. Identify overallocated team members (red indicator)
5. Drag tasks to reassign

**Color coding:**
- Green: Under capacity (< 80%)
- Yellow: At capacity (80-100%)
- Red: Over capacity (> 100%)

### Time Tracking Reports

View time spent:
1. Go to Reports > Time Tracking
2. Filter by: Date range, Project, Team member, Billable/Non-billable
3. View:
   - Total hours logged
   - Hours by project
   - Hours by person
   - Billable vs. non-billable breakdown
4. Export to CSV or Excel

### Custom Reports (Business/Enterprise)

Build custom reports:
1. Go to Reports > Create Custom Report
2. Choose data source: Tasks, Projects, Time entries
3. Add filters and groupings
4. Choose visualization: Table, Chart, or Mixed
5. Save and schedule email delivery (daily, weekly, monthly)

**Example reports:**
- Sprint velocity over last 6 months
- Bug resolution time by severity
- Tasks completed per team member
- Time to completion by project type

### Export Data

Export options:
- **CSV:** Click "Export" button on any view
- **Excel:** Advanced export with formatting (Business+)
- **PDF:** Generate reports with charts (Business+)
- **API:** Programmatic access (all plans)

---

## Time Tracking

### Start Tracking Time

Track time on tasks:
1. Open a task
2. Click the timer icon in task header
3. Timer starts counting
4. Click "Stop" when done
5. Time entry saves automatically

**Keyboard shortcut:** Press `T` on any task to toggle timer.

### Manual Time Entry

Add time retroactively:
1. Open a task
2. Click "Add Time Entry"
3. Enter:
   - Start and end time (or duration)
   - Date
   - Description (optional)
   - Billable toggle
4. Click "Save"

### Time Estimates

Set estimates for planning:
1. Open a task
2. Add "Estimated Time" custom field
3. Enter hours (e.g., "4h" or "2d")
4. Compare actual vs. estimate in reports

Estimates appear in Workload view for capacity planning.

### Billable Hours

Mark time as billable:
1. In task, check "Billable" on time entry
2. Set hourly rate:
   - Per person: Settings > Team > Edit Member
   - Per project: Project Settings > Billing Rate
   - Per task: Add "Billing Rate" custom field

Generate invoices from billable time:
1. Go to Reports > Time Tracking
2. Filter by billable + date range
3. Click "Generate Invoice"
4. Export to PDF or integrate with QuickBooks/Xero

---

## Billing & Subscription

### Upgrade Your Plan

To upgrade:
1. Go to Settings > Billing & Plans
2. Click "Upgrade" next to desired plan
3. Enter payment method (credit card or ACH)
4. Choose billing cycle: Monthly or Annual (20% discount)
5. Confirm upgrade

**Prorated billing:** You're charged only for the remaining billing period when upgrading mid-cycle.

### Add More Users

Plans are priced per user:
1. Go to Settings > Team Members > Invite Members
2. New users added to next invoice automatically
3. View cost: Settings > Billing > Upcoming Invoice

**Billing examples:**
- Pro plan: $19/user/month
- Add 3 users mid-month: Prorated charge
- Annual billing: $19 × 12 × 0.8 = $182.40/user/year

### Change Billing Information

Update payment method:
1. Settings > Billing > Payment Methods
2. Click "Add Payment Method"
3. Enter card details or ACH info
4. Set as default
5. Remove old payment method (optional)

### Download Invoices

Access past invoices:
1. Settings > Billing > Invoice History
2. Click any invoice to download PDF
3. Invoices emailed to billing admin on payment

### Cancel Subscription

To downgrade or cancel:
1. Settings > Billing > Current Plan
2. Click "Change Plan" or "Cancel Subscription"
3. Choose:
   - Downgrade to free tier (data retained for 30 days)
   - Cancel immediately (lose access now)
   - Cancel at end of billing period (recommended)
4. Confirm cancellation

**Data retention:** 30 days after cancellation. Export your data before this period.

### Enterprise Contracts

For custom contracts:
- Contact sales@flowsync.io
- Minimum 100 users
- Annual commitment required
- Custom pricing, SLA, and support terms
- Net-30 or Net-60 payment terms available

---

## Security & Compliance

### Two-Factor Authentication (2FA)

Enable 2FA:
1. Go to Your Profile > Security
2. Click "Enable Two-Factor Authentication"
3. Scan QR code with authenticator app (Authy, Google Authenticator)
4. Enter verification code
5. Save backup codes

**Enforce 2FA (Admin):**
Workspace Settings > Security > Require 2FA for all members

### Data Encryption

FlowSync encrypts data:
- **In transit:** TLS 1.3 for all connections
- **At rest:** AES-256 encryption for database
- **Backups:** Encrypted and stored in separate region

### Data Residency

Choose where data is stored (Enterprise):
1. Workspace Settings > Security > Data Residency
2. Choose region: US (Oregon), EU (Ireland), UK (London), Australia (Sydney)
3. Contact support to migrate existing data

Default: US for American accounts, EU for European accounts.

### Audit Logs

View security events (Business/Enterprise):
1. Settings > Security > Audit Logs
2. See events:
   - User login/logout
   - Permission changes
   - File exports
   - Settings modifications
   - API access
3. Filter by user, date, event type
4. Export logs for compliance

### IP Allowlisting (Enterprise)

Restrict access by IP:
1. Settings > Security > IP Allowlist
2. Click "Add IP Range"
3. Enter IP addresses or CIDR ranges
4. Enable "Block all other IPs"
5. Test with secondary admin account first

### SOC 2 Compliance

FlowSync is SOC 2 Type II certified:
- Request report: compliance@flowsync.io
- NDA required
- Available to Business and Enterprise customers
- Updated annually

### GDPR Compliance

For GDPR requests:
- **Data export:** User can self-export via Settings > Privacy > Export My Data
- **Data deletion:** Contact support@flowsync.io with "GDPR Deletion Request"
- **DPA:** Download Data Processing Agreement at flowsync.io/dpa
- **Privacy policy:** flowsync.io/privacy

Processing time: Up to 30 days for deletion requests.

---

## Troubleshooting

### Login Issues

**Cannot log in / "Invalid credentials" error:**
1. Check Caps Lock is off
2. Clear browser cache and cookies
3. Try incognito/private browsing mode
4. Click "Forgot Password" to reset
5. Check spam folder for reset email
6. If using SSO, contact your IT admin

**Account locked after multiple attempts:**
- Wait 15 minutes for automatic unlock
- Or contact support@flowsync.io for immediate unlock

### Sync Problems

**Changes not appearing for teammates:**
1. Check internet connection
2. Refresh browser (Cmd/Ctrl + R)
3. Check Status Page: status.flowsync.io
4. Try logging out and back in
5. Clear browser cache

**GitHub/Jira sync stopped working:**
1. Settings > Integrations > [Service]
2. Check connection status
3. Click "Reconnect" if showing disconnected
4. Regenerate API token/OAuth connection
5. Check that FlowSync app still has permissions in GitHub/Jira

### Notification Issues

**Not receiving email notifications:**
1. Check Settings > Notifications > Email Preferences
2. Check spam/junk folder
3. Add notifications@flowsync.io to contacts
4. Verify email address in Profile settings
5. Check workspace admin hasn't disabled emails

**Too many notifications:**
1. Settings > Notifications
2. Adjust per-notification type:
   - Assigned to task
   - Mentioned in comment
   - Task due soon
   - Status changed
3. Use "Do Not Disturb" mode
4. Mute specific projects: Project Settings > Notifications > Mute

### Performance Issues

**Slow loading / Lag:**
1. Check internet speed (minimum 5 Mbps recommended)
2. Close unused browser tabs
3. Disable browser extensions temporarily
4. Try different browser (Chrome, Firefox, Safari, Edge supported)
5. Clear cache: Settings > Advanced > Clear Cache

**Large attachments fail to upload:**
- Maximum file size: 100MB per file (Starter/Pro), 500MB (Business/Enterprise)
- Supported formats: All common formats (PDF, images, Office files, ZIP)
- For larger files, use Google Drive or Dropbox integration

---

## API & Webhooks

### API Access

All plans include API access:
- Base URL: `https://api.flowsync.io/v1`
- Authentication: Bearer token
- Rate limits:
  - Starter/Pro: 1,000 requests/hour
  - Business: 5,000 requests/hour
  - Enterprise: 20,000 requests/hour

### Generate API Token

1. Go to Settings > Integrations > API
2. Click "Create API Token"
3. Name your token (e.g., "CI/CD Pipeline")
4. Set permissions: Read-only or Read/Write
5. Copy token (shown once only)
6. Store securely (treat like a password)

### API Documentation

Full API docs: api.flowsync.io/docs

**Common endpoints:**
- `GET /projects` — List all projects
- `POST /projects` — Create project
- `GET /tasks` — List tasks (with filters)
- `POST /tasks` — Create task
- `PATCH /tasks/:id` — Update task
- `DELETE /tasks/:id` — Delete task
- `GET /users` — List team members

### Webhooks

Receive real-time events:
1. Settings > Integrations > Webhooks
2. Click "Create Webhook"
3. Enter endpoint URL (must be HTTPS)
4. Choose events:
   - task.created
   - task.updated
   - task.completed
   - task.deleted
   - project.created
5. Add secret for signature verification
6. Click "Save"

**Webhook payload format:**
```json
{
  "event": "task.created",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "id": "TSK-12345",
    "title": "Fix login bug",
    "assignee": "john@company.com",
    "status": "To Do",
    "project_id": "PRJ-456"
  }
}
```

### Webhook Security

Verify webhook authenticity:
1. Check `X-FlowSync-Signature` header
2. Compute HMAC SHA-256 of payload with your secret
3. Compare signatures

Example (Node.js):
```javascript
const crypto = require('crypto');
const signature = req.headers['x-flowsync-signature'];
const hash = crypto.createHmac('sha256', SECRET)
  .update(JSON.stringify(req.body))
  .digest('hex');
if (signature !== hash) throw new Error('Invalid signature');
```

---

## Mobile App

### Download Mobile App

Available for iOS and Android:
- **iOS:** App Store (requires iOS 15+)
- **Android:** Google Play Store (requires Android 11+)

### Mobile App Features

**Full functionality:**
- View and edit tasks
- Create new tasks and projects
- Comment and attach files
- Start/stop time tracking
- Receive push notifications
- Offline mode (sync when back online)

**Mobile-optimized views:**
- Quick Actions: Swipe task to complete, assign, or reschedule
- Voice input: Dictate task descriptions
- Photo attachments: Take photo directly from task
- Home screen widgets (iOS/Android)

### Push Notifications

Configure on mobile:
1. Open FlowSync app
2. Go to Settings > Notifications
3. Enable push notifications
4. Choose notification types (same as web)
5. Set quiet hours

### Offline Mode

Mobile app works offline:
- Create and edit tasks while offline
- Changes sync automatically when back online
- Conflict resolution: Last edit wins (shows warning)

### Mobile Shortcuts

**iOS Shortcuts:**
- "Create task in FlowSync"
- "Show my tasks due today"
- "Start timer on last task"

**Android widgets:**
- Quick Add Task widget
- My Tasks widget
- Project Overview widget

---

## Best Practices

### Project Organization

**Use templates:**
- Save project templates for recurring work types
- Include standard tasks, automations, and custom fields
- Templates maintain your team's workflow consistency

**Folder structure:**
- Group related projects into folders
- Name projects clearly: "[CLIENT] - [PROJECT TYPE]"
- Archive completed projects (not delete) for reference

### Task Hygiene

**Keep tasks actionable:**
- Start with verb: "Design homepage", "Review PR", "Deploy to staging"
- One owner per task (avoid shared responsibility)
- Break down tasks over 3 days into subtasks

**Use due dates wisely:**
- Set realistic deadlines
- Use "Start date" for tasks that can't begin immediately
- Don't set dates on every task (creates noise)

### Communication

**Use @mentions:**
- Mention teammates to notify them: @john
- Mention entire project: @team
- Keep discussions in task comments (not external email/Slack)

**Status updates:**
- Weekly project updates via Status Update feature
- Tag updates with mood emoji and blocker flag
- Share publicly or with specific stakeholders

### Automation Tips

**Start simple:**
- Begin with 2-3 automations
- Test on small project first
- Add complexity gradually

**Common mistakes:**
- Too many automations (creates confusion)
- Overlapping automations (duplicate notifications)
- Missing conditions (applies to wrong tasks)

### Performance Optimization

**Keep projects manageable:**
- Archive old tasks regularly
- Aim for < 500 active tasks per project
- Use multiple projects instead of one giant project

**File management:**
- Use Google Drive/Dropbox links for large files
- Delete old file versions
- Don't attach files > 50MB

---

## Getting Help

### Help Center

Browse 400+ articles: help.flowsync.io

**Popular articles:**
- Getting started guide
- Integration setup tutorials
- Automation examples
- Troubleshooting common issues
- Video tutorials

### Live Chat

Chat with support team:
- Click "?" icon in bottom right
- Available 24/7 for urgent issues
- Business hours for complex questions

### Email Support

Email: support@flowsync.io

**Response times:**
- Starter/Pro: Within 4 hours
- Business: Within 2 hours
- Enterprise: Within 30 minutes (SLA)

### Community Forum

Join 5,000+ users: community.flowsync.io

- Ask questions
- Share workflows and automations
- Vote on feature requests
- Learn from other teams

### Feature Requests

Submit ideas:
1. Go to flowsync.io/feedback
2. Search existing requests first
3. Upvote existing or submit new
4. Track status: Under Review → Planned → In Development → Shipped

### Status Page

Check system status: status.flowsync.io

- Real-time uptime monitoring
- Incident history
- Subscribe to updates
- Maintenance schedule
