# MASTER PROJECT SPECIFICATION

## Cloud-Based Student Task Manager

**Document purpose:** A single source of truth for planning, building,
testing, deploying, and documenting a resume-ready cloud application.

**Primary goal:** Build a polished, secure, responsive student
task-management web application using Python and cloud services while
keeping costs at â‚¹0 wherever possible.

**Important execution rule for the AI coding tool:** Do not merely
describe or print code. Create and edit the actual project files in the
workspace when file access is available. Run the application and tests,
fix errors, and report honestly what was and was not verified. Do not
claim deployment succeeded unless it was actually completed and checked.

------------------------------------------------------------------------

# 1. PROJECT SUMMARY

## 1.1 Project name

Cloud-Based Student Task Manager

## 1.2 Problem statement

Students often manage assignments, exams, study sessions, and deadlines
across notebooks and separate apps. This project provides one central
place to organize tasks, prioritize work, monitor progress, and access
data from different devices.

## 1.3 Target users

Students who need to manage academic tasks, deadlines, and study
progress.

## 1.4 Core objectives

-   Build a responsive, professional web application.
-   Allow users to register, sign in, and manage only their own tasks.
-   Support creating, viewing, editing, completing, searching,
    filtering, sorting, and deleting tasks.
-   Store task data persistently in a database.
-   Deploy using services with suitable free tiers, subject to current
    provider terms and quotas.
-   Maintain clean code, tests, documentation, and a presentable GitHub
    repository.
-   Make the project understandable enough for the developer to explain
    in interviews.

## 1.5 Success criteria

The project is complete only when: - A new user can register and sign in
securely. - A user can create, edit, complete, and delete tasks. - Task
data remains after logging out and back in. - One user cannot access
another user's tasks by changing a URL or request. - Search, filters,
sorting, validation, empty states, and error states work. - The
interface works on desktop and mobile sizes. - Automated tests pass. -
Setup and deployment instructions are documented. - No passwords, API
keys, or real environment secrets are committed to Git. - Any live demo
is actually deployed and checked, or is clearly labelled as not yet
deployed.

------------------------------------------------------------------------

# 2. REQUIRED TECHNOLOGY STACK

Use a simple stack that is appropriate for a Python learner and can be
maintained with minimal cost.

## 2.1 Application

-   Python 3.11 or a currently supported compatible version.
-   Flask for the web application.
-   HTML templates using Jinja.
-   CSS for styling.
-   Small amounts of JavaScript for interactions.
-   SQLAlchemy for database access.
-   Flask-Migrate or a clearly documented database initialization
    approach.
-   Flask-Login or an equivalent established session-authentication
    library.
-   Werkzeug's secure password hashing utilities.
-   pytest for automated tests.

## 2.2 Database and hosting

Preferred low-cost approach: - Supabase PostgreSQL Free plan for
persistent hosted data, if its current limits and policies suit the
project. - A compatible Python web host with a free tier, if one is
available and appropriate at build time. - GitHub for version control
and source hosting. - A local SQLite configuration for development and
tests where appropriate.

The AI tool must verify current provider pricing, inactivity policies,
free-tier quotas, supported Python versions, and deployment requirements
before selecting a production host. Do not assume a provider has a free
tier simply because it previously did.

If a free host cannot run a persistent Flask application, explain the
limitation and recommend a compatible alternative or a local/demo
deployment. Do not silently substitute a paid service.

## 2.3 Cost policy

-   Target total cost: â‚¹0.
-   Use free tiers only within their terms and quotas.
-   Use a provider's default subdomain instead of buying a domain.
-   Do not enable paid upgrades or paid resources without explicit user
    approval.
-   Warn the user before any step that could incur charges.
-   Do not ask the user to paste credentials or secrets into chat.
-   If a credit card is required, explain that requirement before
    proceeding and offer an alternative when feasible.

------------------------------------------------------------------------

# 3. FEATURES AND REQUIREMENTS

## 3.1 Authentication

-   Registration with name, email, and password.
-   Login and logout.
-   Secure password hashing; never store plain-text passwords.
-   Server-side validation.
-   Helpful but safe error messages.
-   Session cookies configured appropriately for local and production
    environments.
-   Protect authenticated pages.
-   Prevent access to other users' data.
-   Do not implement social login unless explicitly added later.

## 3.2 Task management

Each task should support: - Title (required). - Description
(optional). - Subject or category (optional). - Due date (optional). -
Priority: Low, Medium, High. - Status: Pending, In Progress,
Completed. - Created timestamp. - Updated timestamp. - Owner/user ID.

Actions: - Create a task. - View task details. - Edit a task. - Mark it
complete or reopen it. - Delete it after confirmation. - Search by title
and, if practical, description. - Filter by status, priority, and
subject. - Sort by due date, priority, or most recently updated. -
Paginate or otherwise limit results if the list becomes large.

## 3.3 Dashboard

The dashboard must use real database data for the signed-in user. Do not
hardcode summary numbers.

Required sections: - Welcome message using the user's display name. -
Summary cards: Total Tasks, Pending, In Progress, Completed, and
Overdue. - Completion percentage calculated from task records. - Task
list with priority, status, and due-date indicators. - Quick action to
add a task. - Search and filter controls. - Weekly progress
visualization if it can be implemented accessibly and accurately. -
Recent tasks or upcoming deadlines. - Useful empty state for a new
account. - Clear success and error notifications. - Responsive
navigation and profile/logout controls.

Metric definitions must be documented: - Total Tasks: all tasks owned by
the current user. - Pending: tasks whose status is Pending. - In
Progress: tasks whose status is In Progress. - Completed: tasks whose
status is Completed. - Overdue: incomplete tasks with a due date earlier
than the current date in the application's chosen timezone. - Completion
Rate: completed tasks divided by total tasks, with a safe zero-task
case.

## 3.4 Explicitly out of scope for the first version

Do not add these unless requested: - Paid subscriptions. - AI-generated
task suggestions. - Team collaboration or sharing. - Calendar provider
integrations. - Email/SMS notifications requiring paid services. -
Mobile native applications. - Complex microservices. - Kubernetes or
other infrastructure that is unnecessary for this small project.

------------------------------------------------------------------------

# 4. DASHBOARD DESIGN SPECIFICATION

## 4.1 Visual direction

Create a polished, modern SaaS dashboard that looks like a credible
productivity product rather than a tutorial demo.

Visual style: - Clean, uncluttered layout. - Light neutral page
background. - White or near-white cards. - Indigo/blue as the primary
accent. - Use semantic colors sparingly for task states and
priorities. - Consistent spacing and alignment. - Subtle borders and
shadows, not excessive gradients. - Readable typography and clear
heading hierarchy. - Consistent corner radius and icon style. - Avoid
unnecessary animations, decorative clutter, and oversized empty areas.

## 4.2 Main application shell

Desktop: - Fixed or sticky left sidebar with logo/name and navigation. -
Main content area with top header. - Main dashboard content aligned to a
consistent maximum width. - Responsive grid for summary cards. - Task
list or table with clear column alignment.

Sidebar items: - Dashboard - My Tasks - Calendar (only if implemented;
otherwise do not show a nonfunctional item) - Analytics (only if
implemented) - Settings (only if implemented) - User profile and Logout

Do not show links that do nothing. For a smaller first version,
Dashboard and My Tasks plus profile/logout are sufficient.

## 4.3 Dashboard top section

Include: - Welcome headline, such as "Good morning, \[Name\]" where
practical. - Concise supporting text, such as "Here's your study
progress." - Primary "Add Task" button. - Optional date label, but do
not rely on it as a core feature.

## 4.4 Summary cards

Display Total Tasks, Pending, In Progress, Completed, and Overdue. Each
card should have: - Clear label. - Prominent number. - Small consistent
icon. - Optional comparison/progress only if based on actual data. -
Consistent height and spacing. - Responsive layout: 4--5 columns on wide
screens where readable, 2 columns on tablets, and 1--2 columns on narrow
mobile screens.

Do not use misleading charts or fake trend percentages.

## 4.5 Task list

Include: - Title and optional subject. - Due date. - Priority badge. -
Status badge or select control. - Actions for edit, complete/reopen, and
delete. - Clear hover/focus states. - Search, filter, and sort
controls. - Mobile-friendly layout: horizontally scroll only if
necessary; preferably transform rows into stacked task cards on small
screens.

Priority appearance: - Low: subtle neutral/green indicator. - Medium:
amber indicator. - High: red/orange indicator. Use text labels as well
as color so meaning is not color-only.

Status appearance: - Pending: neutral. - In Progress: blue. - Completed:
green. Use accessible contrast.

## 4.6 Charts and analytics

A simple weekly completion chart may be included using a maintained
lightweight chart library or an accessible CSS/SVG visualization. Charts
must use actual user-specific task data. Include a text summary or
accessible label. If chart complexity delays core functionality, finish
the task manager first and add the chart only after tests pass.

## 4.7 Empty, loading, and error states

Design these deliberately: - No tasks: friendly message and "Create your
first task" action. - No search matches: explain that no tasks match and
offer "Clear filters." - Form errors: show near the relevant field and
in an accessible summary if useful. - Network/database error: show a
calm user-facing message; log details server-side without exposing
secrets. - Loading: use a subtle loading state only where real
asynchronous loading occurs. - Delete confirmation: clearly identify the
action and provide Cancel and Delete. - Success: concise notification
after create/edit/delete/status change.

## 4.8 Responsive and accessibility requirements

-   Support narrow mobile screens, tablets, and desktop.
-   Use semantic HTML.
-   Labels must be associated with form inputs.
-   All core actions must be keyboard accessible.
-   Visible focus indicators.
-   Adequate color contrast.
-   Do not communicate priority or status through color alone.
-   Respect reduced-motion preferences if animation is used.
-   Test common widths such as 360px, 768px, and 1280px.

## 4.9 Dashboard acceptance checklist

-   [ ] Layout is consistent and visually polished.
-   [ ] Sidebar/navigation works.
-   [ ] Summary numbers are calculated from the current user's data.
-   [ ] Search, filters, and sorting work.
-   [ ] Create/edit/delete/complete actions work.
-   [ ] Confirmation is shown before deletion.
-   [ ] Empty and error states are present.
-   [ ] Layout is usable at mobile, tablet, and desktop widths.
-   [ ] Buttons and links are functional; no placeholder controls.
-   [ ] Accessibility labels and keyboard focus are present.
-   [ ] No hardcoded fake analytics are shown.

------------------------------------------------------------------------

# 5. DATA MODEL

Use a relational database.

## 5.1 User table

Suggested fields: - id: primary key. - name: required display name. -
email: required, unique, normalized. - password_hash: required. -
created_at: timestamp.

## 5.2 Task table

Suggested fields: - id: primary key. - user_id: foreign key to User,
required and indexed. - title: required, length-limited. - description:
optional, length-limited. - subject: optional, length-limited. -
due_date: optional date. - priority: constrained to Low, Medium, High. -
status: constrained to Pending, In Progress, Completed. - created_at:
timestamp. - updated_at: timestamp.

Use database constraints where appropriate. Ensure each query that
reads, updates, or deletes a task also checks that the task belongs to
the authenticated user. Never rely only on hiding another user's task in
the UI.

Document any timezone assumptions. Store timestamps consistently and
display them according to a documented approach.

------------------------------------------------------------------------

# 6. PROPOSED PROJECT STRUCTURE

The AI coding tool may adjust this structure if it has a clear technical
reason, but it must document the change and update all instructions
consistently.

cloud-student-task-manager/ â”œâ”€â”€ app/ â”‚ â”œâ”€â”€ **init**.py â”‚ â”œâ”€â”€
extensions.py â”‚ â”œâ”€â”€ models.py â”‚ â”œâ”€â”€ auth/ â”‚ â”‚ â”œâ”€â”€ **init**.py â”‚ â”‚ â””â”€â”€
routes.py â”‚ â”œâ”€â”€ tasks/ â”‚ â”‚ â”œâ”€â”€ **init**.py â”‚ â”‚ â””â”€â”€ routes.py â”‚ â”œâ”€â”€ main/
â”‚ â”‚ â”œâ”€â”€ **init**.py â”‚ â”‚ â””â”€â”€ routes.py â”‚ â”œâ”€â”€ templates/ â”‚ â”‚ â”œâ”€â”€ base.html
â”‚ â”‚ â”œâ”€â”€ auth/ â”‚ â”‚ â”‚ â”œâ”€â”€ login.html â”‚ â”‚ â”‚ â””â”€â”€ register.html â”‚ â”‚ â”œâ”€â”€ main/
â”‚ â”‚ â”‚ â””â”€â”€ dashboard.html â”‚ â”‚ â”œâ”€â”€ tasks/ â”‚ â”‚ â”‚ â”œâ”€â”€ list.html â”‚ â”‚ â”‚ â”œâ”€â”€
form.html â”‚ â”‚ â”‚ â””â”€â”€ detail.html â”‚ â”‚ â””â”€â”€ errors/ â”‚ â”‚ â”œâ”€â”€ 403.html â”‚ â”‚ â”œâ”€â”€
404.html â”‚ â”‚ â””â”€â”€ 500.html â”‚ â””â”€â”€ static/ â”‚ â”œâ”€â”€ css/ â”‚ â”‚ â””â”€â”€ style.css â”‚
â”œâ”€â”€ js/ â”‚ â”‚ â””â”€â”€ main.js â”‚ â””â”€â”€ images/ â”œâ”€â”€ tests/ â”‚ â”œâ”€â”€ conftest.py â”‚ â”œâ”€â”€
test_auth.py â”‚ â”œâ”€â”€ test_tasks.py â”‚ â””â”€â”€ test_dashboard.py â”œâ”€â”€ docs/ â”‚ â”œâ”€â”€
SPECIFICATION.md â”‚ â”œâ”€â”€ ARCHITECTURE.md â”‚ â”œâ”€â”€ DATABASE.md â”‚ â”œâ”€â”€
DEPLOYMENT.md â”‚ â”œâ”€â”€ TESTING.md â”‚ â””â”€â”€ TROUBLESHOOTING.md â”œâ”€â”€ instance/ â”‚
â””â”€â”€ (local instance configuration/data if applicable; do not commit
private data) â”œâ”€â”€ .env.example â”œâ”€â”€ .gitignore â”œâ”€â”€ requirements.txt â”œâ”€â”€
config.py â”œâ”€â”€ run.py â”œâ”€â”€ wsgi.py â””â”€â”€ README.md

Do not create empty or fake modules merely to match the tree. Every
included file must have a clear purpose. If a file is unnecessary,
remove it from the tree and explain why. Generated directories such as
.venv/, **pycache**/, test caches, and local database files must be
ignored by Git where appropriate.

------------------------------------------------------------------------

# 7. FILE CREATION AND CONTENT RULES

For every file, the implementation guide must state: 1. Exact relative
path. 2. Purpose. 3. Whether it is created manually, by a command, by a
migration, or automatically at runtime. 4. Full contents or exact
command that generates it. 5. Dependencies and imports. 6. How to verify
it works.

Important distinctions: - Creating a file does not populate it with
code. - A directory creation command creates the directory only. -
`python -m venv .venv` generates the virtual environment. - Installing
dependencies generates installed package files in the environment. -
Python may create `__pycache__/` automatically. - Database tables must
be created through migrations or documented initialization code. -
`.env` is a local configuration file that contains private values and
must not be committed. - `.env.example` contains placeholder variable
names and safe example values only. - Never include real API keys,
database passwords, session secrets, or production credentials in the
repository or documentation.

Use one consistent approach for schema creation and migrations. Document
how a fresh database is initialized and how future schema changes are
applied.

------------------------------------------------------------------------

# 8. CONFIGURATION AND ENVIRONMENT VARIABLES

Create `.env.example` with variable names and placeholders appropriate
to the chosen implementation, for example: - FLASK_APP - FLASK_ENV or
the appropriate supported configuration setting - SECRET_KEY -
DATABASE_URL

Do not assume every variable is necessary. Use supported Flask
configuration practices for the selected Python version. Do not commit
`.env`.

Requirements: - Fail safely when a required production secret is
missing. - Use a random, private secret in production. - Never hardcode
credentials in Python source. - Validate database configuration and
provide useful startup errors without revealing secrets. - Document how
to create and activate a virtual environment on Windows and
macOS/Linux. - Document how to install dependencies and run the app
locally.

------------------------------------------------------------------------

# 9. SECURITY REQUIREMENTS

-   Hash passwords using a recognized secure library.
-   Enforce authentication for private pages.
-   Enforce user ownership on every task operation.
-   Validate and normalize form input server-side.
-   Use ORM parameterization rather than constructing SQL with untrusted
    strings.
-   Protect against cross-site request forgery for state-changing form
    submissions using a suitable Flask extension or equivalent.
-   Use secure cookie settings in production, including HTTPS-aware
    settings.
-   Do not expose stack traces or secrets to end users.
-   Use safe template escaping; avoid rendering user content as trusted
    HTML.
-   Limit field lengths and validate allowed enum values.
-   Apply safe error handling and logging.
-   Do not log passwords, tokens, or full secret-bearing connection
    strings.
-   Avoid collecting unnecessary personal data.
-   Explain that a public demo must not contain real student records or
    sensitive information.
-   Add rate limiting for authentication only if it can be implemented
    and maintained safely within the project's scope; document the
    choice.
-   Ensure debug mode is disabled in production.

------------------------------------------------------------------------

# 10. IMPLEMENTATION PHASES

Build the application in phases. After each phase, run relevant checks
and summarize the results.

## Phase 1: Workspace and environment

-   Check installed Python version and tooling.
-   Create project directory and virtual environment.
-   Create dependency list.
-   Add `.gitignore`, `.env.example`, configuration, and application
    entry points.
-   Verify a minimal Flask route runs locally.

## Phase 2: Application structure and database

-   Set up Flask application factory or a similarly clear application
    structure.
-   Configure extensions.
-   Implement User and Task models.
-   Add migrations or a documented database initialization workflow.
-   Verify database connection and schema.

## Phase 3: Authentication

-   Build registration, login, logout, and protected routes.
-   Add password hashing and server-side validation.
-   Test duplicate email, invalid credentials, and unauthenticated
    access.
-   Test that sessions work as expected.

## Phase 4: Task CRUD

-   Build task creation, listing, detail, editing, completion, and
    deletion.
-   Add validation, search, filtering, and sorting.
-   Enforce task ownership in every route.
-   Test normal cases and unauthorized access attempts.

## Phase 5: Dashboard and design

-   Build the navigation shell and responsive visual system.
-   Implement data-backed summary cards and task lists.
-   Add empty, success, validation, and error states.
-   Add charts only if they use real data and remain accessible.
-   Check mobile and desktop layouts.

## Phase 6: Testing and quality

-   Run all automated tests.
-   Run a manual acceptance checklist.
-   Check logs, accessibility basics, and security behavior.
-   Fix errors rather than hiding them.
-   Verify that no secrets or local data are tracked by Git.

## Phase 7: GitHub

-   Initialize Git.
-   Create useful commits.
-   Review `.gitignore`.
-   Add a complete README with setup, features, architecture,
    screenshots instructions, testing, and deployment.
-   Do not upload secrets or real personal data.

## Phase 8: Cloud deployment

-   Recheck current provider pricing and free-tier limits.
-   Select a compatible host and database.
-   Configure environment variables through the provider's secure
    settings.
-   Run database migrations safely.
-   Deploy and verify the health of the application.
-   Test registration, login, task CRUD, persistence, and user isolation
    on the deployed version.
-   Document cold starts, sleeping behavior, usage limits, and other
    known constraints.
-   If deployment cannot be completed due to provider limits or required
    user credentials, provide precise remaining steps without claiming
    success.

## Phase 9: Resume readiness

-   Add architecture diagram and screenshots.
-   Document design decisions and limitations.
-   Record genuine test results and performance measurements.
-   Prepare resume bullets that describe only implemented and verified
    features.
-   Prepare interview explanations for architecture, authentication,
    database, deployment, testing, and cost controls.

------------------------------------------------------------------------

# 11. TESTING REQUIREMENTS

Use pytest and a separate test database/configuration.

Minimum test cases: - Registration succeeds with valid input. -
Duplicate email is handled. - Password is stored as a hash. - Login
succeeds with correct credentials. - Login fails with incorrect
credentials. - Logout clears the authenticated session. -
Unauthenticated users cannot access private pages. - A task can be
created. - Required title validation works. - A task can be edited. - A
task can be completed and reopened. - A task can be deleted. - Search
and filters behave correctly. - Dashboard metrics match stored task
records. - Overdue calculation handles missing due dates and completed
tasks correctly. - User A cannot view, edit, complete, or delete User
B's task, including by guessing or changing an ID. - Invalid
priority/status values are rejected. - CSRF protection is active for
state-changing forms. - Error pages do not expose stack traces or
secrets.

The AI coding tool must run the tests and report actual results. If
tests fail, fix the underlying issue and rerun them. Never report tests
as passing unless they were run and passed.

------------------------------------------------------------------------

# 12. LOCAL SETUP DOCUMENTATION

The generated README and deployment docs must contain platform-specific
commands.

At minimum document: - Prerequisites and tested versions. - How to open
the project folder. - How to create a virtual environment. - How to
activate it on Windows PowerShell, Windows Command Prompt, macOS, and
Linux as applicable. - How to install dependencies. - How to create a
local `.env`. - How to initialize or migrate the database. - How to
start the development server. - The local URL to open. - How to run
tests. - How to stop the server. - Common errors and fixes.

Use commands that match the actual project files. Do not provide
contradictory commands or refer to files that do not exist.

------------------------------------------------------------------------

# 13. CLOUD DEPLOYMENT DOCUMENTATION

Before choosing services, the AI tool must check current official
provider documentation for: - Free-tier eligibility and limits. -
Supported runtime and build method. - Database connection
requirements. - Persistent storage behavior. - Inactivity/sleep
behavior. - Build/runtime hours and usage caps. - Whether a payment
method is required. - Any restrictions relevant to a student portfolio
project.

Deployment guide must include: 1. Provider selection rationale. 2.
Account setup steps, without asking for credentials in chat. 3. Database
creation and connection. 4. Environment variable configuration. 5. Build
and start commands matching the repository. 6. Migration steps. 7.
Deployment steps. 8. Post-deployment verification. 9. Troubleshooting.
10. Cost controls and service shutdown/cleanup steps.

Do not put database passwords in a public URL, source file, screenshot,
or commit. Do not expose a private database directly to the browser. The
backend should manage database access.

------------------------------------------------------------------------

# 14. README AND GITHUB REQUIREMENTS

The README must include: - Project title and summary. - Problem
statement. - Feature list. - Screenshots section with
instructions/placeholders until real screenshots exist. - Architecture
overview and diagram. - Technology stack. - Local installation steps. -
Environment variables table with descriptions but no real secret
values. - Database setup. - Test instructions. - Deployment guide
link. - Security notes. - Free-tier limitations. - Known limitations. -
Future improvements. - License section only if a license is actually
selected.

Suggested commit sequence: 1. Initial project structure. 2. Add database
models and configuration. 3. Add authentication. 4. Add task CRUD. 5.
Add dashboard and responsive styling. 6. Add tests and documentation. 7.
Deployment configuration and final fixes.

Do not fabricate GitHub repository URLs, screenshots, badges, test
coverage, user counts, uptime, or deployment links.

------------------------------------------------------------------------

# 15. RESUME AND INTERVIEW PREPARATION

Once the implementation is verified, prepare 2--3 resume bullets using
only facts supported by the project.

Example templates to fill with real facts: - "Built a responsive
task-management web application using Python, Flask, and \[database\],
implementing authentication and user-specific task operations." -
"Implemented task creation, editing, filtering, status tracking, and
data-backed dashboard metrics, with automated tests covering key
workflows." - "Deployed the application to \[verified provider\] using
environment-based configuration and documented setup, testing, and
deployment."

Only mention cloud services, CI/CD, automated deployment, security
features, or measurable performance improvements if they were actually
implemented and verified.

Prepare interview questions and answers on: - Why Flask? - How does
authentication work? - Why hash passwords? - How do you enforce task
ownership? - How is the database schema designed? - How are
configuration and secrets managed? - What happens when the database is
unavailable? - How does deployment work? - What free-tier limitations
exist? - What tests protect the application? - What would you improve
next?

------------------------------------------------------------------------

# 16. AI CODING TOOL EXECUTION INSTRUCTIONS

Treat this document as the primary specification.

## Required workflow

1.  Inspect the existing workspace before modifying it.
2.  Summarize the intended architecture and identify any assumptions.
3.  Verify current cloud provider information if web access is
    available. If not, clearly mark provider details that require manual
    verification.
4.  Create the actual folders and files in the workspace.
5.  Implement a complete, internally consistent application.
6.  Do not leave core features as TODOs, mock buttons, fake charts, or
    pseudocode.
7.  Do not generate secrets or ask the user to share secrets in the
    conversation.
8.  Install dependencies only when the user/environment permits.
9.  Run the application and automated tests where tools permit.
10. Fix errors and rerun tests.
11. Review the UI at desktop and mobile widths where browser tools
    permit.
12. Check Git status for secrets and generated files.
13. Update documentation to match the implementation.
14. Provide a final report.

## Handling ambiguity

-   Prefer the simplest maintainable design that meets the requirements.
-   Do not add unnecessary technologies.
-   If a feature conflicts with the zero-cost requirement, explain the
    tradeoff and offer a no-cost alternative.
-   If a user action or credential is required, stop at that point and
    explain exactly what the user must do.
-   Do not claim a file was created unless it exists in the workspace.
-   Do not claim a command or test was run unless it was actually run.
-   Do not claim deployment succeeded unless the deployed app was
    verified.

## Final report format

At the end, report: - Features implemented. - Files created. - Commands
to run locally. - Test commands and actual results. - Any unimplemented
items. - Any security limitations. - Cloud services chosen and current
free-tier caveats. - Exact remaining manual deployment steps. - Where to
find the README and other docs. - Suggested next steps.

------------------------------------------------------------------------

# 17. FINAL DEFINITION OF DONE

The project is considered complete when: - \[ \] The application starts
locally from documented commands. - \[ \] All core features are
implemented. - \[ \] Authentication and user-specific data access are
tested. - \[ \] Dashboard values are data-driven. - \[ \] UI is
responsive and polished. - \[ \] Automated tests have been run and
results documented. - \[ \] No secrets are committed. - \[ \] README and
documentation match the actual code. - \[ \] GitHub repository is
prepared. - \[ \] Deployment is verified, or remaining manual steps are
clearly documented. - \[ \] Free-tier constraints and possible costs are
disclosed. - \[ \] Resume bullets are accurate and interview
explanations are prepared.

**End of master specification.**

