# LexDesk Product Documentation

## Getting Started with LexDesk

Welcome to LexDesk. This guide will help you set up your account and start managing your law firm more efficiently within 30 minutes.

### Account Setup Steps
1. Sign up at lexdesk.io with your work email
2. Verify your email address via the confirmation link
3. Complete your firm profile (name, address, practice areas, bar number)
4. Invite team members under Settings > Team Members
5. Connect your calendar (Google Calendar or Outlook)
6. Import existing clients via CSV upload or manual entry
7. Set up your billing preferences under Settings > Billing

### System Requirements
- Browser: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- Internet: Stable broadband connection (minimum 5 Mbps)
- Mobile: iOS 14+ or Android 10+ for mobile app

---

## Client Intake

### How to Set Up Intake Forms
1. Go to Intake > Form Builder
2. Click "New Form" and select a practice area template
3. Customize fields (drag and drop)
4. Add your conflict check questions
5. Set up e-signature for retainer agreement
6. Copy the intake link and share with prospective clients
7. Set automated follow-up emails under Intake > Automation

### Conflict of Interest Check
LexDesk automatically runs conflict checks when a new intake is submitted:
- System searches all existing clients and matters
- Flags any name, company, or opposing party matches
- Sends alert to the responsible attorney
- Intake is held until conflict is cleared or waived

### How to Review and Accept New Intakes
1. Go to Intake > Pending
2. Click on the intake submission to review
3. Check conflict status (green = clear, red = flagged)
4. Click "Accept" to convert to a client and matter
5. Or click "Decline" and send automated decline email

### Retainer Agreement E-Signature
1. Go to Matter > Documents
2. Select your retainer template
3. Click "Send for Signature"
4. Enter client email
5. Client receives link and signs digitally
6. Signed document is stored automatically in the matter

---

## Case Management

### How to Create a New Matter
1. Go to Matters > New Matter
2. Select the client (or create new client)
3. Enter matter name, practice area, and responsible attorney
4. Set the statute of limitations or key deadline
5. Assign team members
6. Click "Create Matter"

### Managing Deadlines and Tasks
- Go to Matter > Tasks to add deadlines
- Set task assignee, due date, and priority
- Enable reminders: 7 days, 3 days, 1 day before deadline
- Tasks sync with connected Google Calendar or Outlook
- Overdue tasks appear in red on the dashboard

### Court Date Management
1. Go to Matter > Calendar
2. Click "Add Court Date"
3. Enter court, judge, case number, and date/time
4. LexDesk sends automated reminders to assigned attorneys
5. Court dates sync to connected calendars automatically

### Client Portal Access
Each client gets a secure portal link to:
- View case status and updates
- Upload requested documents
- Send secure messages to their attorney
- View and pay invoices online

To enable: Go to Matter > Settings > Enable Client Portal > Send Portal Link

---

## Time Tracking and Billing

### How to Track Time
- Click the timer icon in any matter to start tracking
- Or go to Time > New Entry for manual entry
- Enter description, hours, billing rate, and matter
- Mark as billable or non-billable
- Time entries appear in the matter's billing tab

### How to Generate an Invoice
1. Go to Billing > New Invoice
2. Select client and matter
3. Choose time entries to include (or add flat fees)
4. Add expenses if applicable
5. Review and click "Send Invoice"
6. Client receives invoice via email with online payment link

### Payment Methods Accepted
- Credit card (Visa, Mastercard, Amex) via Stripe
- ACH bank transfer (US clients)
- Wire transfer (Enterprise clients)
- Check (manual recording available)

### LEDES Billing Format
For corporate clients requiring LEDES format:
1. Go to Billing > Invoice Settings
2. Enable LEDES 1998B format
3. Assign task codes and activity codes to time entries
4. Generate invoice — LexDesk exports LEDES automatically

### How to Set Up Recurring Invoices
1. Go to Billing > Recurring
2. Click "New Recurring Invoice"
3. Select client, amount, and frequency (weekly/monthly)
4. Set start date and end date (or ongoing)
5. Invoices generate and send automatically

---

## Document Management

### Uploading Documents
1. Go to Matter > Documents
2. Click "Upload" or drag and drop files
3. Select document category (Pleading, Contract, Correspondence, etc.)
4. Documents are stored securely with version control

### Using Document Templates
LexDesk includes 500+ legal document templates:
- Go to Documents > Template Library
- Search by practice area or document type
- Click "Use Template"
- Fill in matter details — fields auto-populate from matter data
- Edit as needed and save to matter

### Document Version Control
- Every document save creates a new version
- Go to Document > Version History to view all versions
- Click any version to restore or download
- Original document is never deleted

### Supported File Types
- Documents: PDF, DOCX, DOC, TXT, RTF
- Spreadsheets: XLSX, XLS, CSV
- Images: JPG, PNG, TIFF (for scanned documents)
- Maximum file size: 50MB per file
- Storage: Unlimited on Growth and Enterprise plans; 10GB on Solo and Firm plans

---

## Team Management

### How to Invite Team Members
1. Go to Settings > Team Members
2. Click "Invite Member"
3. Enter email and select role (Attorney, Paralegal, Admin, Billing)
4. Member receives invitation email
5. They sign up and are added to your firm automatically

### User Roles and Permissions
| Role | Access Level |
|------|-------------|
| Owner | Full access — billing, settings, all matters |
| Attorney | All matters assigned to them + new matter creation |
| Paralegal | Assigned matters only — no billing access |
| Admin | All matters + billing — no settings access |
| Billing | Billing and invoices only |

### How to Remove a Team Member
1. Go to Settings > Team Members
2. Click on the member's name
3. Click "Deactivate Account"
4. Their matters are reassigned to the owner
5. Their data remains in the system for compliance

---

## Integrations

### Connecting Gmail or Outlook
1. Go to Settings > Integrations
2. Click "Connect" next to Gmail or Outlook
3. Authorize LexDesk to access your email
4. Emails from clients are automatically linked to their matters

### QuickBooks Integration
1. Go to Settings > Integrations > QuickBooks
2. Click "Connect to QuickBooks"
3. Authorize the connection
4. LexDesk invoices sync to QuickBooks automatically
5. Payments recorded in LexDesk reflect in QuickBooks

### DocuSign Integration
1. Go to Settings > Integrations > DocuSign
2. Connect your DocuSign account
3. Send documents for signature directly from LexDesk matters
4. Signed documents sync back automatically

### Clio Migration
Migrating from Clio to LexDesk:
1. Export your data from Clio (Clients, Matters, Documents)
2. Go to LexDesk > Settings > Import Data
3. Upload Clio CSV export
4. LexDesk maps fields automatically
5. Review and confirm import
6. Migration typically completes in under 1 hour

---

## Security and Compliance

### Data Security
- All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- SOC 2 Type II certified — audited annually
- Two-factor authentication (2FA) available and recommended
- Automatic session timeout after 30 minutes of inactivity
- IP allowlisting available on Enterprise plan

### GDPR Compliance (UK/EU)
- Data stored in AWS eu-west-2 (London) for UK customers
- Right to erasure requests processed within 30 days
- Data Processing Agreement (DPA) available on request
- Cookie consent management built-in

### HIPAA Compliance
- Available for firms handling medical malpractice or personal injury with PHI
- Business Associate Agreement (BAA) available on Growth and Enterprise plans
- PHI fields encrypted separately

### Two-Factor Authentication Setup
1. Go to Settings > Security
2. Click "Enable 2FA"
3. Scan QR code with Google Authenticator or Authy
4. Enter verification code to confirm
5. Save backup codes in a secure location

### Password Requirements
- Minimum 12 characters
- Must include uppercase, lowercase, number, and special character
- Password reset available via email link
- Passwords expire every 90 days on Enterprise plan

---

## Billing and Subscription

### How to Upgrade Your Plan
1. Go to Settings > Billing
2. Click "Change Plan"
3. Select new plan
4. Confirm — upgrade is immediate
5. Prorated credit applied for unused days on current plan

### How to Cancel Your Subscription
1. Go to Settings > Billing
2. Click "Cancel Subscription"
3. Select cancellation reason
4. Confirm cancellation
5. Account remains active until end of billing period
6. Data export available for 90 days after cancellation

### Refund Policy
- 14-day free trial — no charge if cancelled before trial ends
- Monthly plans: No refunds for partial months
- Annual plans: Prorated refund within 30 days of purchase
- Refund requests: billing@lexdesk.io

### Adding or Removing Users
- Go to Settings > Billing > Manage Seats
- Add seats: charged prorated for current billing period
- Remove seats: credit applied to next billing period
- Minimum 1 seat required on all plans

---

## Troubleshooting

### Cannot Log In
1. Check you are using the correct email address
2. Try "Forgot Password" at lexdesk.io/login
3. Check spam folder for password reset email
4. Clear browser cache and cookies
5. Try incognito/private browsing mode
6. If 2FA is enabled, ensure your authenticator app time is synced
7. Contact support if issue persists

### Documents Not Loading
1. Check your internet connection
2. Refresh the page (Ctrl+R or Cmd+R)
3. Clear browser cache
4. Try a different browser
5. Check if file size exceeds 50MB limit
6. Disable browser extensions temporarily

### Calendar Not Syncing
1. Go to Settings > Integrations
2. Disconnect and reconnect your calendar
3. Ensure LexDesk has calendar permissions in Google/Outlook settings
4. Check if events are in the correct calendar
5. Allow up to 15 minutes for sync to complete

### Invoice Payment Not Processing
1. Verify client's card details are correct
2. Check if card has sufficient funds
3. Try ACH transfer as alternative
4. Ensure billing address matches card records
5. Contact billing@lexdesk.io for manual processing

### Email Integration Not Working
1. Go to Settings > Integrations
2. Disconnect and reconnect Gmail/Outlook
3. Ensure you authorized all requested permissions
4. Check if your email provider has blocked third-party access
5. For Google: Enable "Less secure app access" or use App Password

### Mobile App Issues
1. Ensure app is updated to latest version
2. Log out and log back in
3. Clear app cache (Settings > Apps > LexDesk > Clear Cache)
4. Uninstall and reinstall the app
5. Ensure iOS 14+ or Android 10+ is installed

---

## Account Management

### How to Update Firm Information
1. Go to Settings > Firm Profile
2. Update name, address, phone, website
3. Upload firm logo
4. Click Save

### How to Change Your Email Address
1. Go to Settings > My Profile
2. Click "Change Email"
3. Enter new email and current password
4. Verification link sent to new email
5. Click link to confirm change

### How to Export Your Data
1. Go to Settings > Data Export
2. Select data types (Clients, Matters, Documents, Time Entries, Invoices)
3. Choose date range
4. Click "Request Export"
5. Download link emailed within 1 hour

### API Access
Available on Growth and Enterprise plans:
1. Go to Settings > API
2. Generate API key
3. Full REST API documentation at docs.lexdesk.io/api
4. Rate limit: 1,000 requests/hour on Growth, unlimited on Enterprise