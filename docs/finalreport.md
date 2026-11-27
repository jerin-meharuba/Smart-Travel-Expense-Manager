# Independent University, Bangladesh
## CSE309 Web Application & Internet
### Final Project Submission Report

**Submitted by:**

- **Name:** Jerin Meharuba
- **Student ID:** 2312069
- **Section:** 06
- **Team Number:** Write the team number assigned by the instructor here
- **Project Title:** Smart travel expense manager
- **Vercel URL:** https://smart-travel-expense-manager.vercel.app/
- **GitHub Repository:** https://github.com/jerin-meharuba/Smart-Travel-Expense-Manager

**Submitted To:**

- **Sayef Reyadh**
- Adjunct Lecturer
- Department of Computer Science & Engineering
- Independent University, Bangladesh

**Semester:** Autumn 2026
**Date of Submission:** 28-11-2026

---

## Table of Contents

1. Executive Summary
   - 1.1 Project overview
   - 1.2 What was built since the mid assessment
   - 1.3 Live links
2. Part A. Product Requirements (PRD)
   - A1. Problem Statement
   - A2. Users and Roles
   - A3. Goals and Success Measures
   - A4. Scope and Non-Goals
   - A5. User Stories
3. Part B. Software Requirements (SRS)
   - B1. Introduction
   - B2. Functional Requirements
   - B3. Non-Functional Requirements
   - B4. Roles and Permission Matrix
   - B5. Use Cases
   - B6. Acceptance Criteria
   - B7. Traceability Matrix
4. Part C. Technical Design (TDD)
   - C1. Technology Stack
   - C2. System Architecture
   - C3. Backend and Frontend Structure
   - C4. Data Model
   - C5. API Design
   - C6. JWT Authentication Design
   - C7. RBAC Design
   - C8. Admin Dashboard Design
   - C9. Security Design and Threats
   - C10. Deployment on Vercel
   - C11. Testing
5. Part D. Evidence: Screenshots of the Running Application
   - D1. User Side
   - D2. Security Behaviour
   - D3. Admin Dashboard
   - D4. Deployment
   - D5. Tests
6. Part E. Project Management and Conclusion
   - E1. How to Run and Test
   - E2. GitHub Work
   - E3. Limitations
   - E4. Future Work
   - E5. Sources, Libraries and Tools
7. Appendix. Test Accounts and Video Demo

---

## 1. Executive Summary

### 1.1 Project overview

Smart Travel Expense Manager is a web app for planning trips and tracking travel costs. It is made for people who travel and want to watch their spending. Users can create trips, add expenses, and set budgets. A dashboard shows charts built from the saved data. An admin can manage user accounts. The stack is React with TypeScript, FastAPI, PostgreSQL on Neon, and Vercel.

### 1.2 What was built since the mid assessment

These are the main parts I added for the final project.

- JWT login with Argon2 password hashing
- Role based access control with two roles, user and admin
- Ownership checks, so each user sees only their own data
- Admin panel to list, create, edit, and delete users
- Trips, expenses, budgets, and a dashboard with charts
- Deployment on Vercel with a Neon database

### 1.3 Live links

Test account IDs and passwords are in the PDF report Appendix only.

**Table 1: Project links**

| Item | Link |
|---|---|
| GitHub repository | https://github.com/jerin-meharuba/Smart-Travel-Expense-Manager |
| Vercel frontend | https://smart-travel-expense-manager.vercel.app/ |
| API | https://smart-travel-expense-manager.vercel.app/api/v1 |
| API docs | https://smart-travel-expense-manager.vercel.app/docs |
| Video demo | https://youtu.be/Pj3KFSSjFhM?si=trizXbJUB3A3kVN- |

---

# Part A. Product Requirements (PRD)

## A1. Problem Statement

Many people plan trips with notes, chat messages, and spreadsheets. The costs end up in many places. It is easy to forget small payments like taxis and snacks. Prices may also be in different currencies. This makes the real total hard to see.

Most people only learn they overspent after the trip is over. A trip budget is usually limited, so this matters. Students feel it the most because their money is tight.

## A2. Users and Roles

My project has no groups. So there is no group member role.

**Table 2: Users and roles**

| Role | Who they are | Main tasks | Must never be able to do |
|---|---|---|---|
| Visitor | A person without an account | Open the site, register, log in | See any trip, expense, or budget |
| User | A registered traveler | Manage own trips, expenses, and budgets. View the dashboard. | Read or change another user's data. Use admin endpoints. |
| Admin | The person who runs the system | List, create, edit, and delete users | Edit or delete their own account from the admin endpoints |

## A3. Goals and Success Measures

**Table 3: Goals and measures**

| ID | Goal | Measure |
|---|---|---|
| G1 | Users manage trips, expenses, and budgets | Create, view, edit, and delete work for each, with no error |
| G2 | Original money values stay unchanged | Amount and currency stay as entered. Yes or no. |
| G3 | The dashboard shows real data | Dashboard totals match the saved expenses |
| G4 | No user can read another user's data | A request for another user's trip returns 404 |
| G5 | Passwords are never stored as plain text | The database holds only Argon2 hashes |
| G6 | Only admins can use admin features | A normal user gets 403. No token gets 401. |

## A4. Scope and Non-Goals

### In scope

- Registration and login with JWT
- User and admin roles
- Ownership checks on every private record
- Admin user management
- Trips, expenses, and budgets
- Dashboard with filters and charts
- Database migrations with Alembic
- Deployment on Vercel

### Out of scope

I planned some of these in my early documents. I did not build them because of limited time. They are not needed for the main goal.

- Refresh tokens and a session list
- Groups and shared trips
- Traveler records for each trip
- Currency conversion
- Audit log and activity view
- Banning users
- CSV export
- Password change screen

### Assumptions and constraints

- Users have a modern browser like Chrome or Edge.
- Vercel and Neon free plans set the hosting limits.
- Each amount is saved in one currency.
- I had one semester to finish the work.

## A5. User Stories

**Table 4: User stories**

| ID | Role | Story |
|---|---|---|
| US-01 | Visitor | I want to register with my email so that I can keep my own trip data. |
| US-02 | User | I want to log in so that I can see my trips. |
| US-03 | User | I want to log out so that nobody else can use my account. |
| US-04 | User | I want to create a trip with dates so that I can plan it. |
| US-05 | User | I want to add an expense with a currency so that my record stays correct. |
| US-06 | User | I want to set a budget so that I can avoid overspending. |
| US-07 | User | I want charts on a dashboard so that I can understand my spending. |
| US-08 | User | I want to see only my own data so that my records stay private. |
| US-09 | User | I want to be blocked from admin features so that restricted actions stay safe. |
| US-10 | User | I want other people's trip IDs to show not found so that nobody can guess my data. |
| US-11 | Admin | I want to see all users so that I can review accounts. |
| US-12 | Admin | I want to create a user with a role so that I can add accounts. |
| US-13 | Admin | I want to edit or delete a user so that I can fix or remove accounts. |
| US-14 | Admin | I want to be stopped from deleting myself so that the system always keeps an admin. |

---

# Part B. Software Requirements (SRS)

## B1. Introduction

This part says exactly what the system shall do. Every requirement has an ID and can be tested. The readers are my instructor and any developer who works on the project later.

**Table: Definitions**

| Term | Meaning |
|---|---|
| JWT | A signed token that proves who the user is |
| Access token | A short-lived JWT sent with every request |
| Refresh token | A long-lived token used to get a new access token. My project does not use it. |
| RBAC | Role based access control. What you can do depends on your role. |
| Role | A label on the user. Mine are user and admin. |
| Permission | A rule about what a role may do |
| Audit log | A record of who did what. My project does not have one. |

### References

- RFC 7519, JSON Web Token
- OWASP Application Security Verification Standard (ASVS)
- FastAPI documentation
- SQLAlchemy 2.0 and Alembic documentation
- PyJWT and pwdlib documentation
- Vercel and Neon documentation

## B2. Functional Requirements

**Table 5: Authentication (FR-AUTH)**

| ID | Requirement |
|---|---|
| FR-AUTH-01 | The system shall let a visitor register with an email and a password. |
| FR-AUTH-02 | The system shall change emails to lowercase and reject emails that look wrong. |
| FR-AUTH-03 | The system shall require a password of 8 to 128 characters. |
| FR-AUTH-04 | The system shall reject an email that is already registered with status 409. |
| FR-AUTH-05 | The system shall store passwords only as Argon2 hashes. |
| FR-AUTH-06 | The system shall let a user log in and receive a JWT access token. |
| FR-AUTH-07 | The system shall sign the token with HS256 and make it expire in 60 minutes. |
| FR-AUTH-08 | The system shall show one generic error for a failed login. |
| FR-AUTH-09 | The system shall return the current user's profile at GET /auth/me. |
| FR-AUTH-10 | The system shall let a user log out. The frontend deletes the stored token. |
| FR-AUTH-11 | The system shall return 401 when the token is missing, wrong, or expired. |

**Table 6: Access control (FR-RBAC)**

| ID | Requirement |
|---|---|
| FR-RBAC-01 | The system shall give each user one role, user or admin. New sign-ups get user. |
| FR-RBAC-02 | The system shall check the role on the server for every admin endpoint. |
| FR-RBAC-03 | The system shall return 403 when a non-admin calls an admin endpoint. |
| FR-RBAC-04 | The system shall filter trips by the logged-in user's ID. |
| FR-RBAC-05 | The system shall check that an expense's trip belongs to the user. |
| FR-RBAC-06 | The system shall check that a budget belongs to the user. |
| FR-RBAC-07 | The system shall return 404 for records owned by someone else. |
| FR-RBAC-08 | The system shall stop an admin from editing or deleting their own account. |
| FR-RBAC-09 | The system shall accept only user or admin as a role value. |

**Table 7: Admin features (FR-ADM)**

| ID | Requirement |
|---|---|
| FR-ADM-01 | The system shall list all users, newest first. |
| FR-ADM-02 | The system shall let an admin create a user with an email, password, and role. |
| FR-ADM-03 | The system shall let an admin edit another user's email, password, or role. |
| FR-ADM-04 | The system shall let an admin delete another user. |
| FR-ADM-05 | The system shall let me create the first admin with a command line tool. |
| FR-ADM-06 | The system shall never return password hashes in admin responses. |
| FR-ADM-07 | The system shall reject a duplicate email with 409 in admin actions. |

**Table 8: Trips, expenses, budgets, and dashboard (FR-DOMAIN)**

| ID | Requirement |
|---|---|
| FR-TRIP-01 | The system shall let a user create, view, edit, and delete their own trips. |
| FR-TRIP-02 | The system shall reject a trip that ends before it starts, with 422. |
| FR-TRIP-03 | The system shall list trips in pages. The limit is 100 and the default is 20. |
| FR-TRIP-04 | The system shall require a currency when a trip budget amount is set. |
| FR-EXP-01 | The system shall let a user create, view, edit, and delete their own expenses. |
| FR-EXP-02 | The system shall save the original amount and currency of every expense. |
| FR-EXP-03 | The system shall filter expenses by trip, category, and date range. |
| FR-EXP-04 | The system shall offer five fixed categories: Accommodation, Activities, Food, Other, Transport. |
| FR-BUD-01 | The system shall let a user set a budget for a trip, a category, or both. |
| FR-BUD-02 | The system shall reject a budget of zero or less. |
| FR-BUD-03 | The system shall reject a second budget for the same target, with 409. |
| FR-BUD-04 | The system shall show spending, remaining amount, and usage for each budget. |
| FR-DASH-01 | The system shall show total trips, active trips, total spending, and remaining budgets. |
| FR-DASH-02 | The system shall show spending by category and by trip. |
| FR-DASH-03 | The system shall show daily and monthly spending trends. |
| FR-DASH-04 | The system shall compare each budget with the actual spending. |
| FR-DASH-05 | The system shall apply trip, category, and date filters to the dashboard. |

## B3. Non-Functional Requirements

**Table 9: Non-functional requirements**

| ID | Area | Requirement | How to check |
|---|---|---|---|
| NFR-SEC-01 | Security | Secrets stay in environment variables | The repository has only placeholder values |
| NFR-SEC-02 | Security | Login errors are generic | Wrong email and wrong password give the same message |
| NFR-SEC-03 | Security | The access token expires after 60 minutes | Read the token lifetime setting |
| NFR-SEC-04 | Security | CORS allows only the set frontend origin | Read the CORS setting in main.py |
| NFR-PERF-01 | Performance | List endpoints use pages with a limit of 100 | Send limit=101 and get 422 |
| NFR-USE-01 | Usability | The trip list shows loading and error messages | Stop the backend and open the page |
| NFR-REL-01 | Reliability | Data stays after a restart | Restart the server and check the data |
| NFR-ACC-01 | Accuracy | Money uses Numeric(12,2), not floats | Read the model files |
| NFR-MNT-01 | Maintainability | One reusable admin check | The require_admin dependency |
| NFR-MNT-02 | Maintainability | Database changes use migrations | Four Alembic files in the project |
| NFR-MNT-03 | Maintainability | Automated tests exist | Run pytest. Four tests pass. |
| NFR-DOC-01 | Documentation | API docs are public | Open the /docs page |

I did not set or measure a response time target.

## B4. Roles and Permission Matrix

**Table 10: Endpoint groups by roles**

| Endpoint group | Visitor | User | Admin |
|---|---|---|---|
| Register and login | Yes | Yes | Yes |
| Logout and my profile | No | Yes | Yes |
| Category list | Yes | Yes | Yes |
| Trips | No | Own | Own |
| Expenses | No | Own | Own |
| Budgets | No | Own | Own |
| Dashboard | No | Own | Own |
| Admin users | No | No | Yes |
| Health check and API docs | Yes | Yes | Yes |

**Table 11: Ownership rules (used instead of group permissions)**

My project has no groups, so I use ownership rules here.

| Record | Who can read and change it | How it is checked |
|---|---|---|
| Trip | Its owner | The query filters by user_id |
| Expense | The owner of its trip | The query joins the trip and filters by user_id |
| Budget | Its owner | The query filters by user_id |
| Category | Nobody can change it. All logged-in users can read it. | Categories are seeded and read only |

**Table 12: Admin rules**

| Rule | Result |
|---|---|
| Admin edits or deletes their own account in admin endpoints | Blocked with 400 |
| Admin creates another admin | Allowed |
| Admin changes the role of another admin | Allowed. There is no extra block. |
| Admin deletes another admin | Allowed. There is no extra block. |
| Admin reads another user's trips or expenses | Not possible. Normal endpoints filter by the admin's own ID. |
| Admin sees password hashes | Never. Responses leave them out. |

## B5. Use Cases

My project has no ban feature and no audit log. So I replaced those two use cases with others that match my app.

> **[Figure 1: Use case diagram with the actors Visitor, User, and Admin and the use cases below. Add the real diagram here.]**

**Table 13: Use case descriptions**

| ID | Use case and actor | Preconditions | Main flow | Alternative and error flows | Postconditions |
|---|---|---|---|---|---|
| UC-01 | Log in. Actor: User. | The account exists. | 1. The user types email and password. 2. The frontend sends POST /auth/login. 3. The server checks the Argon2 hash. 4. The server returns a token and the user. 5. The frontend saves the token. | Wrong details give 401. Bad format gives 422. After 60 minutes the token expires and calls give 401. The user logs in again. | The user can open the app. |
| UC-02 | Create an expense. Actor: User. | The user is logged in and owns a trip. | 1. The user picks a trip and a category. 2. The user types amount, currency, date, and payment method. 3. The frontend sends POST /expenses. 4. The server checks the trip owner and the category. 5. The server saves the expense. | A trip owned by someone else gives 404. A missing category gives 404. Bad data gives 422. No token gives 401. | The expense is saved with its original amount and currency. |
| UC-03 | Set a budget. Actor: User. | The user is logged in. | 1. The user picks a trip, a category, or both. 2. The user types amount and currency. 3. The frontend sends POST /budgets. 4. The server checks the target and duplicates. 5. The server returns the budget with spending. | No target gives 422. A duplicate target gives 409. A trip owned by someone else gives 404. | The budget is saved. |
| UC-04 | A denied action. Actor: User. | The user is logged in with the user role. | 1. The user calls GET /admin/users. 2. The require_admin check reads the role. 3. The server returns 403 with a message. | No token gives 401. | Nothing changes in the database. |
| UC-05 | Change a user's role. Actor: Admin. | The admin is logged in. | 1. The admin opens the admin panel. 2. The admin picks a user. 3. The admin changes the role. 4. The frontend sends PATCH /admin/users/{id}. 5. The server saves the change. | Own account gives 400. Unknown user gives 404. Duplicate email gives 409. A non-admin gets 403. | The user has the new role. |
| UC-06 | View the dashboard. Actor: User. | The user is logged in. | 1. The user opens the dashboard. 2. The user picks filters. 3. The frontend calls the dashboard endpoints. 4. The server adds up only the user's expenses. 5. The charts update. | No token gives 401. | The charts match the saved data. |

## B6. Acceptance Criteria

Ban rules do not apply, because I did not build banning.

**Table 14: Acceptance criteria**

| ID | Requirement | Given | When | Then |
|---|---|---|---|---|
| AC-01 | FR-AUTH-11 | A token older than 60 minutes | The user calls GET /trips | The server returns 401 |
| AC-02 | FR-AUTH-11 | A token with changed characters | The user calls GET /auth/me | The server returns 401 |
| AC-03 | FR-AUTH-11 | No token | The visitor calls GET /trips | The server returns 401 |
| AC-04 | FR-RBAC-07 | User B owns trip 5 | User A calls GET /trips/5 | The server returns 404 |
| AC-05 | FR-RBAC-03 | A user with the user role | The user calls GET /admin/users | The server returns 403 |
| AC-06 | FR-RBAC-08 | A logged in admin | The admin edits their own account | The server returns 400 |
| AC-07 | FR-AUTH-04 | An email already in use | A visitor registers with it | The server returns 409 |
| AC-08 | FR-EXP-02 | An expense saved as 125.50 USD | The user reads budgets and the dashboard | The expense still shows 125.50 USD |

## B7. Traceability Matrix

The screenshot numbers match Part D. A dash means there is no screenshot.

**Table 15: Requirement, endpoint or screen, test, screenshot**

| Requirement | Endpoint or screen | Test | Screenshot |
|---|---|---|---|
| FR-AUTH-01 | POST /auth/register, sign up screen | Manual | S1 |
| FR-AUTH-02 | UserRegister schema | Manual | S1 |
| FR-AUTH-03 | UserRegister schema | Manual | S1 |
| FR-AUTH-04 | create_user in auth service | Manual | S1 |
| FR-AUTH-05 | hash_password in security.py | test_provision_admin_creates_normalized_admin_with_hashed_password | - |
| FR-AUTH-06 | POST /auth/login | Manual | S1 |
| FR-AUTH-07 | create_access_token | Manual | S8 |
| FR-AUTH-08 | authenticate_user | Manual | S1 |
| FR-AUTH-09 | GET /auth/me, profile screen | Manual | S6 |
| FR-AUTH-10 | POST /auth/logout, Log out button | Manual | S6 |
| FR-AUTH-11 | get_current_user | Manual | S8 |
| FR-RBAC-01 | users.role column | Manual | S6 |
| FR-RBAC-02 | require_admin | test_administrator_is_accepted_for_admin_routes | S10 |
| FR-RBAC-03 | require_admin | test_regular_user_is_rejected_from_admin_routes | S7 |
| FR-RBAC-04 | GET /trips | Manual | S2 |
| FR-RBAC-05 | Expense service | Manual | S3 |
| FR-RBAC-06 | Budget service | Manual | S4 |
| FR-RBAC-07 | get_trip_or_404 | Manual | S9 |
| FR-RBAC-08 | Admin service | Manual | S12 |
| FR-RBAC-09 | AdminUserCreate schema | Manual | S11 |
| FR-ADM-01 | GET /admin/users, admin panel | Manual | S10 |
| FR-ADM-02 | POST /admin/users | Manual | S11 |
| FR-ADM-03 | PATCH /admin/users/{id} | Manual | S11 |
| FR-ADM-04 | DELETE /admin/users/{id} | Manual | S11 |
| FR-ADM-05 | python -m app.admin.bootstrap | test_provision_admin_creates_normalized_admin_with_hashed_password, test_provision_admin_promotes_existing_user_and_replaces_password | - |
| FR-ADM-06 | UserRead schema | Manual | S10 |
| FR-ADM-07 | Admin service | Manual | S11 |
| FR-TRIP-01 to FR-TRIP-04 | /trips endpoints, trips screen | Manual | S2 |
| FR-EXP-01 to FR-EXP-04 | /expenses and /categories endpoints, expenses screen | Manual | S3 |
| FR-BUD-01 to FR-BUD-04 | /budgets endpoints, budgets screen | Manual | S4 |
| FR-DASH-01 to FR-DASH-05 | /dashboard endpoints, dashboard screen | Manual | S5 |

---

# Part C. Technical Design (TDD)

## C1. Technology Stack

I wrote the versions as the minimum I set in package.json and requirements.txt.

**Table 16: Technology stack**

| Component | Technology | Version | Reason |
|---|---|---|---|
| Frontend | React with TypeScript | React 19, TypeScript 5.8 | Popular and easy to split into components |
| Build tool | Vite | 7 | Fast start and simple setup |
| UI styling | Plain CSS in index.css | - | No extra library to learn |
| HTTP client | Axios | 1.21 or newer | Easy shared setup for the token header |
| Charts | Recharts | 3.10 or newer | Works well with React |
| Backend | FastAPI | 0.115 or newer | Fast, simple, and makes API docs by itself |
| Server | Uvicorn | 0.30 or newer | Standard server for FastAPI |
| Database | SQLite locally, PostgreSQL on Neon | - | SQLite needs no setup. Neon is hosted. |
| ORM | SQLAlchemy | 2.0 or newer | Clear models and safe queries |
| Migrations | Alembic | 1.13 or newer | Tracks database changes |
| Database driver | psycopg | 3.2 or newer | Connects Python to PostgreSQL |
| Password hashing | pwdlib with Argon2 | 0.2 or newer | Argon2 is a strong, modern hash |
| JWT library | PyJWT | 2.10 or newer | Small and well known |
| Testing | pytest | 8 or newer | Simple test style |
| Hosting | Vercel | - | Hosts both the frontend and the API |

## C2. System Architecture

> **[Figure 2: System architecture. Show the browser, the Vercel frontend, the Vercel API, and the Neon database. Draw arrows for the requests and the Authorization header.]**

There is no refresh cookie and no audit log in my design. So those two parts are not in the diagram.

- **Arrow 1: Browser to Vercel frontend.** The user opens the site in a browser. Vercel sends the built React files.
- **Arrow 2: React app to the API.** Axios calls /api/v1 on the same domain. Vercel rewrites send these calls to the FastAPI service.
- **Arrow 3: The Authorization header.** Every private request carries the token as a Bearer header. The server reads it and finds the user.
- **Arrow 4: API to the database.** SQLAlchemy sends queries to PostgreSQL on Neon. The connection uses the DATABASE_URL setting.

## C3. Backend and Frontend Structure

**Backend folder tree**

```
backend/
  alembic/        migration files 0001 to 0004
  app/
    admin/        admin routes, service, schemas, bootstrap
    auth/         models, security, dependencies, routes
    budgets/      budget routes and service
    categories/   seeded categories
    dashboard/    chart and summary data
    expenses/     expense routes and service
    trips/        trip routes and service
    config.py     environment settings
    database.py   engine and session
    main.py       app setup and routers
  tests/          pytest files
  requirements.txt
```

**Frontend folder tree**

```
frontend/
  src/
    components/   screens and panels
    services/     Axios calls for each feature
    types/        TypeScript types
    App.tsx       main page and section tabs
    main.tsx      app start
    index.css     styles
  package.json
  vite.config.ts
```

Each backend folder follows the same pattern. The router file defines the endpoints. The service file holds the rules and database work. The schemas file checks the data. The models file maps tables. I did not add a separate repository layer.

Authentication code is in app/auth. The RBAC check is the require_admin function in auth/dependencies.py. Ownership checks live in each service file. Admin code is in app/admin.

On the frontend, components hold the screens. The services folder holds the API calls. The api.ts file sets up Axios and the token header. There is no route guard library. App.tsx shows or hides sections by user and role.

## C4. Data Model

> **[Figure 3: ER diagram. Show users, trips, expenses, categories, and budgets with their links.]**

A user owns many trips. A trip has many expenses. A category groups many expenses. A budget belongs to a user. It points to a trip, a category, or both.

The role is saved in users.role. My project has no tables for bans, sessions, refresh tokens, groups, or an activity log.

**Table 17: users**

| Column | Type | Keys and rules |
|---|---|---|
| id | Integer | Primary key |
| email | String(255) | Unique, indexed, required |
| password_hash | String(255) | Required |
| role | String(30) | Required, default user |
| created_at | DateTime with time zone | Required, default now |

**Table 18: trips**

| Column | Type | Keys and rules |
|---|---|---|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users, indexed |
| name | String(120) | Required |
| destination | String(160) | Required |
| start_date, end_date | Date | Required. End must not be before start. |
| status | String(30) | Required, default planned |
| budget_amount | Numeric(12,2) | Optional |
| budget_currency | String(3) | Needed when a budget amount is set |
| created_at, updated_at | DateTime with time zone | Required |

**Table 19: categories**

| Column | Type | Keys and rules |
|---|---|---|
| id | Integer | Primary key |
| name | String(80) | Unique, required |

**Table 20: expenses**

| Column | Type | Keys and rules |
|---|---|---|
| id | Integer | Primary key |
| trip_id | Integer | Foreign key to trips, indexed |
| category_id | Integer | Foreign key to categories, indexed |
| amount_original | Numeric(12,2) | Required |
| currency_original | String(3) | Required |
| expense_date | Date | Required |
| payment_method | String(50) | Required |
| created_at, updated_at | DateTime with time zone | Required |

**Table 21: budgets**

| Column | Type | Keys and rules |
|---|---|---|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users, indexed |
| trip_id | Integer | Optional foreign key to trips, indexed |
| category_id | Integer | Optional foreign key to categories, indexed |
| amount | Numeric(12,2) | Required. Check: amount is above 0. |
| currency | String(3) | Required |
| created_at, updated_at | DateTime with time zone | Required |

The budgets table has one more check. A budget needs a trip or a category.

## C5. API Design

All application endpoints use the prefix /api/v1. Errors use one shape: `{"detail": "message"}`. Validation errors use status 422.

**Table 22: Endpoint list**

| Method and path | Auth | Role | Body or query | Success | Errors |
|---|---|---|---|---|---|
| GET /health | No | None | None | 200 | None |
| POST /auth/register | No | None | email, password | 201 | 409, 422 |
| POST /auth/login | No | None | email, password | 200 | 401, 422 |
| POST /auth/logout | Token | Any | None | 204 | 401 |
| GET /auth/me | Token | Any | None | 200 | 401 |
| GET /admin/users | Token | Admin | None | 200 | 401, 403 |
| POST /admin/users | Token | Admin | email, password, role | 201 | 401, 403, 409, 422 |
| PATCH /admin/users/{id} | Token | Admin | email, password, role | 200 | 400, 401, 403, 404, 409, 422 |
| DELETE /admin/users/{id} | Token | Admin | None | 204 | 400, 401, 403, 404 |
| GET /categories | No | None | None | 200 | None |
| POST /trips | Token | Owner | trip fields | 201 | 401, 422 |
| GET /trips | Token | Owner | offset, limit | 200 | 401, 422 |
| GET /trips/{id} | Token | Owner | None | 200 | 401, 404 |
| PATCH /trips/{id} | Token | Owner | trip fields | 200 | 401, 404, 422 |
| DELETE /trips/{id} | Token | Owner | None | 204 | 401, 404 |
| POST /expenses | Token | Owner | expense fields | 201 | 401, 404, 422 |
| GET /expenses | Token | Owner | offset, limit, trip_id, category_id, start_date, end_date | 200 | 401, 422 |
| GET /expenses/{id} | Token | Owner | None | 200 | 401, 404 |
| PATCH /expenses/{id} | Token | Owner | expense fields | 200 | 401, 404, 422 |
| DELETE /expenses/{id} | Token | Owner | None | 204 | 401, 404 |
| GET /budgets | Token | Owner | None | 200 | 401 |
| POST /budgets | Token | Owner | trip_id, category_id, amount, currency | 201 | 401, 404, 409, 422 |
| GET /budgets/{id} | Token | Owner | None | 200 | 401, 404 |
| PATCH /budgets/{id} | Token | Owner | budget fields | 200 | 401, 404, 409, 422 |
| DELETE /budgets/{id} | Token | Owner | None | 204 | 401, 404 |
| GET /dashboard/summary | Token | Owner | trip_id, category_id, start_date, end_date | 200 | 401 |
| GET /dashboard/spending-by-category | Token | Owner | same filters | 200 | 401 |
| GET /dashboard/spending-by-trip | Token | Owner | same filters | 200 | 401 |
| GET /dashboard/spending-trends | Token | Owner | same filters and period | 200 | 401 |
| GET /dashboard/budget-comparison | Token | Owner | same filters | 200 | 401 |

The health check is at /health, without the prefix. The word Owner means the user sees only their own records.

## C6. JWT Authentication Design

> **[Figure 4: JWT sequence diagram for login, request, expiry, and logout. Add the real diagram here.]**

**How it works.** At login, the server checks the password hash. It then creates a token and sends it back. The frontend saves the token in the browser. Each later request sends the token in the Authorization header. The server checks the token and loads the user from the database.

**Expiry.** The token lives for 60 minutes. After that, the server returns 401. The user must log in again.

**Refresh and reuse.** I did not build refresh tokens. So there is no refresh step and no refresh token reuse to handle.

**Logout.** The logout endpoint only returns 204. The frontend deletes the saved token. The old token still works until it expires. This is a known limit.

**Table 23: Token claims**

| Claim | Meaning |
|---|---|
| sub | The user ID, saved as text |
| exp | The expiry time, 60 minutes after login |

The token has no role claim. The server reads the role from the database on each request. I used the HS256 algorithm. The secret comes from the SECRET_KEY environment variable.

**Why 60 minutes.** A short life limits the damage if a token is stolen. One hour is long enough for a normal session. It is short enough to be safe for a student project.

**Where the token is stored.** The token is in localStorage. The main risk is XSS, because a script on the page could read it. React escapes text by default, and that is my only defence. CSRF is not a problem here, because the token is not in a cookie.

**What the server checks.** On every request, the server checks the signature and the expiry. It then checks that the user still exists in the database. I have no ban check, because there is no ban feature.

**What the frontend does on a 401.** There is no refresh step. When the token is no longer good, the user logs in again.

## C7. RBAC Design

> **[Figure 5: Authorisation flow for one request. Show token, user, role check, ownership check, and handler.]**

**How a request is checked.** First, the server reads the token. Second, it loads the user from the database. Third, admin routes check the role. Fourth, the service filters records by the owner. Last, the handler runs. I have no group permission check, because I have no groups.

**Roles and constants.** There are two roles, user and admin. They are plain text values in users.role. The admin schemas accept only these two values.

**The reusable check.** All admin routes use one function. It is shortened below.

```python
def get_current_user(credentials=Depends(bearer_scheme), db=Depends(get_db)) -> User:
    user_id = decode_access_token(credentials.credentials) if credentials else None
    user = db.get(User, user_id) if user_id is not None else None
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Administrator access required")
    return current_user
```

**Ownership in queries.** The query itself filters by the owner. It does not load the record first and check later. Here is the trip lookup.

```python
def get_trip_or_404(db, trip_id, user):
    trip = db.scalar(select(Trip).where(Trip.id == trip_id, Trip.user_id == user.id))
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip
```

Expenses join to the trip and filter by the trip owner. Budgets filter by their own user_id. A record from another user looks the same as a missing record. So nobody can guess which IDs exist.

**Adding a new role.** I would add the new value to the role lists in the admin schemas. Then I would write a new check like require_admin. Last, I would add it to the routes that need it.

**Special rules.** An admin cannot edit or delete their own account in the admin endpoints. There are no banned users in my project.

## C8. Admin Dashboard Design

My admin area is one page. It is the Users section in the admin panel. It has a user list on one side and a create or edit form on the other side.

> **[Figure 6: Admin page and the endpoints it calls.]**

**Table 24: Admin page**

| Page | Endpoints | Filters | Actions | Audit events |
|---|---|---|---|---|
| Users | GET, POST, PATCH, DELETE on /admin/users | None | Create, edit, and delete a user | None. There is no audit log. |

The user list has no search, no filters, and no pages. I did not build bulk actions or CSV export.

## C9. Security Design and Threats

**Table 25: Threats and defences**

| Threat | Defence | File or module |
|---|---|---|
| Password database leak | Passwords are saved as Argon2 hashes | auth/security.py |
| Stolen access token | The token expires after 60 minutes. There is no way to cancel it earlier. | config.py |
| Stolen refresh token | Not applicable. There are no refresh tokens. | - |
| Brute-force login | Not covered. There is no lockout. | - |
| Privilege escalation | The role is checked on the server. The sign up form has no role field. | auth/dependencies.py, auth/schemas.py |
| Access to another user's record | Queries filter by the owner. Other records give 404. | trips, expenses, budgets services |
| Cross-site scripting | React escapes text by default. The token in localStorage is still a risk. | frontend |
| Cross-site request forgery | The token goes in a header, not in a cookie | services/api.ts |
| CORS misuse | Only the set frontend origin is allowed | main.py |
| Secrets in the repository | Secrets come from environment variables. The example file has placeholders only. | config.py, .env.example |
| SQL injection | SQLAlchemy sends safe, parameterised queries | all service files |
| Over-posting of fields | Pydantic schemas accept only the listed fields | all schemas files |

## C10. Deployment on Vercel

> **[Figure 7: Deployment layout. Show the Vercel frontend, the Vercel API, and the Neon database.]**

The vercel.json file defines two services. The backend service uses the backend folder and the FastAPI framework. The frontend service uses the frontend folder and the Vite framework.

Rewrites send these paths to the backend: /docs, /openapi.json, /redoc, /health, and /api/(.*). All other paths go to the frontend. So both services share one domain.

On Vercel, the frontend finds the API through VITE_API_BASE_URL set to /api/v1. The database is PostgreSQL on Neon. I run the Alembic migrations against the Neon database with the production DATABASE_URL.

**To redeploy.** Push the changes to the connected GitHub branch. Vercel builds both services again. You can also redeploy from the Vercel dashboard. Run new migrations first, if the database changed.

**Table 26: Environment variable names**

| Name | Used by | What it is for |
|---|---|---|
| DATABASE_URL | Backend | The database address. SQLite is used if it is not set. |
| SECRET_KEY | Backend | The secret that signs JWT tokens |
| FRONTEND_ORIGIN | Backend | The one origin that CORS allows |
| VITE_API_BASE_URL | Frontend | The API address. It is /api/v1 on Vercel. |

## C11. Testing

I use two kinds of tests. The first kind is automated pytest tests for the backend. The second kind is manual tests on the live site.

To run the automated tests, open a terminal in the backend folder. Then run `python -m pytest`. I ran it and all 4 tests passed.

**Table 27: Automated tests**

| Test name | Requirement | Result |
|---|---|---|
| test_regular_user_is_rejected_from_admin_routes | FR-RBAC-03 | Passed |
| test_administrator_is_accepted_for_admin_routes | FR-RBAC-02 | Passed |
| test_provision_admin_creates_normalized_admin_with_hashed_password | FR-ADM-05, FR-AUTH-05 | Passed |
| test_provision_admin_promotes_existing_user_and_replaces_password | FR-ADM-05 | Passed |

I have no automated tests yet for token expiry, tampering, ownership, or the admin self rules. I test them by hand on the live site.

**Table 28: Manual tests**

| Test | Requirement | Result |
|---|---|---|
| Expired token returns 401 | AC-01 | [Write Pass or Fail] |
| Changed token returns 401 | AC-02 | [Write Pass or Fail] |
| Other user's trip returns 404 | AC-04 | [Write Pass or Fail] |
| Normal user on admin endpoint returns 403 | AC-05 | [Write Pass or Fail] |
| Admin edits own account returns 400 | AC-06 | [Write Pass or Fail] |
| Duplicate email returns 409 | AC-07 | [Write Pass or Fail] |

---

# Part D. Evidence: Screenshots of the Running Application

Take every screenshot on the Vercel URL. Show the address bar and the logged-in user. Crop to the useful area. Mask passwords and tokens. Write a caption and the requirement ID under each one.

My project has no sessions list, group page, ban, activity log, or CSV export. So there are no screenshots for those.

> **Note:** The screenshots from the PDF are not included in this Markdown file. Captions are kept below. Add the image files where marked.

## D1. User Side

**[Screenshot S1]** Sign up and login page with a validation error, such as a short password. Requirements: FR-AUTH-01, FR-AUTH-03.

**[Screenshot S2]** Trips page of a logged-in user, showing only their trips.

**[Screenshot S3]** Expenses page with an expense list and the filters.

**[Screenshot S4]** Budgets page showing spending, remaining amount, and usage.

**[Screenshot S5]** Dashboard with the summary and charts.

**[Screenshot S6]** Profile page showing email and role, with the Log out button.

## D2. Security Behaviour

**[Screenshot S7]** Network tab showing 403 when a normal user calls GET /admin/users.

In future development, refresh-token support will be added using secure HttpOnly cookies. This will allow users to obtain new access tokens without logging in again. An account status check will also be implemented. This will ensure banned or deactivated users cannot access protected resources. These features are not implemented in the current version.

## D3. Admin Dashboard

**[Screenshot S10]** Admin panel with the list of users.

**[Screenshot S11]** Admin create or edit user form, with the role field.

**[Screenshot]** Message shown when the admin edits their own account.

## D4. Deployment

**[Screenshot S13]** Vercel project page with the production deployment and domain.

**[Screenshot S14]** Vercel environment variable page with names only. Hide the values.

**[Screenshot S15]** The live API docs page at /docs.

## D5. Tests

**[Screenshot S16]** Terminal showing the pytest run with 4 tests passed.

---

# Part E. Project Management and Conclusion

## E1. How to Run and Test

**What you need.** You need Python 3.11 or newer, Node.js with npm, and Git.

**Environment files.** The backend works without a file. It then uses SQLite. To change settings, copy backend/.env.example to .env. Do the same for frontend/.env.example. Never commit a .env file.

```
# backend/.env
DATABASE_URL=sqlite:///./smart_travel_expense.db
FRONTEND_ORIGIN=http://localhost:5173
SECRET_KEY=replace-with-a-strong-random-secret

# frontend/.env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

**Run the backend.**

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --reload
```

The API runs at http://localhost:8000. The API docs are at http://localhost:8000/docs.

**Create an admin.** Run `python -m app.admin.bootstrap` in the backend folder. It asks for an email and a password.

**Run the frontend.** Open a second terminal.

```bash
cd frontend
npm install
npm run dev
```

The site opens at http://localhost:5173.

**Run the tests.**

```bash
cd backend
python -m pytest
```

**Test accounts.** There are admin and user accounts. Their IDs and passwords are in the PDF report Appendix only.

## E2. GitHub Work

Fill in the real links and titles from your repository. Say which commits are yours and how the work was split over time.

**Table 29: Issues and pull requests**

| Feature | Issue | Pull request | What it delivered |
|---|---|---|---|
| Trips | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/issues/11 | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/pull/12 | Trip create, view, edit, delete |
| Expenses and categories | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/issues/6 | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/pull/13 | Expenses with original currency and fixed categories |
| JWT authentication | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/issues/7 | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/pull/14 | Register, login, logout, and profile |
| RBAC and ownership | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/issues/20 | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/pull/21 | User and admin roles, ownership checks |
| Admin users | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/issues/20 | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/pull/21 | Admin user management and the bootstrap command |
| Budgets and dashboard | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/issues/17 | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/pull/18 | Budgets and dashboard charts |
| Deployment | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/issues/10 | https://github.com/jerinmeharuba/SmartTravel-ExpenseManager/pull/22 | Vercel setup and Neon database |

## E3. Limitations

These are the things that are missing or only partly done.

- There are no refresh tokens. Logout only deletes the token in the browser. The old token works until it expires.
- The token is in localStorage, so an XSS bug could expose it.
- There is no login lockout or brute-force protection.
- There is no password change screen and no session list.
- There is no ban feature, audit log, CSV export, group feature, or traveler record.
- There is no currency conversion. A budget counts only expenses in its own currency.
- The admin area only manages users. The user list has no search, filters, or pages.
- An admin can change the role of another admin. An admin can also delete another admin.
- SECRET_KEY has a weak development default. If the variable is missing, that default is used.
- The category list is public. Categories are fixed and cannot be changed.
- I have only four automated tests. None cover trips, expenses, budgets, the dashboard, or ownership.
- The models have no cascade rule. Deleting a trip that has expenses needs a check.
- Migration 0003 allows an empty trip owner for old rows.
- The README links to deployment.md and project-documentation.md. Those files are not in the docs folder.
- My early PRD, SRS, and TDD files describe some features that I did not build. Examples are travelers and currency conversion.

## E4. Future Work

This is the order I would work in.

1. Add refresh tokens with an httpOnly cookie. This makes sessions safer and logout real.
2. Add login lockout. This stops password guessing.
3. Write more automated tests. This protects the ownership and token rules.
4. Stop admins from changing other admins, and add an audit log. This makes admin work safer.
5. Add password change and a session list. Users get more control.
6. Add search, filters, and CSV export to the admin page. This saves time for admins.
7. Add travelers and shared trips. Groups often travel together.
8. Add currency conversion with saved rates. Totals would then be easier to compare.
9. Fix the missing documentation links in the README.

## E5. Sources, Libraries and Tools

**Table 30: Sources, libraries, and tools**

| Name | Version or link | What for |
|---|---|---|
| React and React DOM | 19 | Frontend screens |
| TypeScript | 5.8 | Typed frontend code |
| Vite | 7 | Build and dev server |
| Axios | 1.21 or newer | API calls |
| Recharts | 3.10 or newer | Dashboard charts |
| FastAPI | 0.115 or newer | Backend API |
| Uvicorn | 0.30 or newer | Running the API |
| SQLAlchemy | 2.0 or newer | Database access |
| Alembic | 1.13 or newer | Migrations |
| psycopg | 3.2 or newer | PostgreSQL driver |
| PyJWT | 2.10 or newer | JWT tokens |
| pwdlib with Argon2 | 0.2 or newer | Password hashing |
| pytest | 8 or newer | Automated tests |
| Vercel | https://vercel.com | Hosting |
| Neon | https://neon.tech | PostgreSQL database |
| RFC 7519 | https://www.rfc-editor.org/rfc/rfc7519 | JWT reference |
| OWASP ASVS | https://owasp.org/www-project-application-security-verification-standard/ | Security reference |

---

# Appendix. Test Accounts and Video Demo

**Video demo:** https://youtu.be/Pj3KFSSjFhM?si=trizXbJUB3A3kVN-

**Test accounts.** Add these only in the PDF report. Never put them in the repository. Use demo data only. My project has no groups, so there is no group table.

| Role | User ID | Password |
|---|---|---|
| Admin 1 | admin@gmail.co | admin@2026 |
| Admin 2 | jerin.admin@gmail.com | admin@2026 |
| User 1 | jerin@gmail.com | 12345678 |
| User 2 | naimurrohan204@gmail.com | 12345678 |
| User 3 | jini@gmail.com | 12345678 |
