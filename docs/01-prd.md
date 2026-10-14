# Smart Travel Expense Planner --- Product Requirements Document (PRD)

  Field               Details
  ------------------- -------------------------------------
  Product             Smart Travel Expense Planner
  Document            Product Requirements Document (PRD)
  Version             1.0
  Status              Draft
  Related documents   `02-srs.md`, `03-tdd.md`

## 1. Purpose

Smart Travel Expense Planner helps users organize trips and track travel
expenses and budgets. It provides a dashboard that summarizes real data
stored in the database.

The application will use a separate React + TypeScript frontend and
FastAPI backend. The frontend will communicate with the backend through
documented REST APIs.

## 2. Product Goals

-   Run the React + TypeScript frontend independently from FastAPI.
-   Provide documented REST APIs through FastAPI.
-   Secure user authentication and administrator permissions.
-   Let users manage trips, travelers, expenses, and budgets.
-   Preserve original transaction amounts and currencies.
-   Display dashboard metrics and charts based on actual database
    records.

## 3. Scope

### 3.1 In Scope

-   Separate frontend and backend applications.
-   User registration, login, and logout.
-   Regular-user and administrator roles.
-   Trip creation and management.
-   Traveler management for trips.
-   Expense creation and management.
-   Trip and category budgets.
-   Preservation of original financial transaction values.
-   Dashboard metrics, filters, and interactive charts.
-   PostgreSQL database hosted on Neon.
-   REST API documentation at `/docs`.
-   Database migrations managed through Alembic.

### 3.2 Out of Scope

The project does not require features beyond the six goals listed in
this document. Additional integrations, export formats, or unrelated
modules are not part of this scope unless approved separately.

## 4. Users and Roles

  -----------------------------------------------------------------------
  Role                                Description
  ----------------------------------- -----------------------------------
  Regular user                        Manages their own trips, travelers,
                                      expenses, and budgets. Views
                                      dashboard data they are allowed to
                                      access.

  Administrator                       Uses administrator-only endpoints
                                      and functions. Administrator access
                                      is enforced by the backend.
  -----------------------------------------------------------------------

A user must not access another user's private records. The frontend must
not be the only layer enforcing permissions.

### 4.1 Target Users

-   Individual travelers who want to plan trips and track travel
    expenses in one place.
-   Small travel groups that need to organize shared trip costs,
    travelers, and budgets.
-   Project reviewers or administrators who need controlled access to
    user and project data.

### 4.2 User Stories

-   As a traveler, I want to create a trip with destinations and dates
    so that I can organize planned travel.
-   As a traveler, I want to add expenses with their original currency
    so that my transaction history remains accurate.
-   As a traveler, I want to compare spending against budgets so that I
    can avoid overspending during a trip.
-   As a traveler, I want dashboard charts based on saved records so
    that I can understand spending patterns.
-   As an administrator, I want administrator-only access controls so
    that restricted actions are protected by the backend.

### 4.3 Milestones

1.  Finalize project documentation and requirements.
2.  Set up the independent React + TypeScript frontend and FastAPI
    backend.
3.  Implement authentication, roles, and backend authorization checks.
4.  Build trip, traveler, expense, category, and budget management.
5.  Add database-backed dashboard metrics and charts.
6.  Review, test, and prepare the project for deployment.

## 5. Functional Requirements

### 5.1 Frontend and Backend Separation

-   The frontend uses React, TypeScript, and Vite.
-   The backend uses Python and FastAPI.
-   Each application can run independently.
-   The frontend calls backend REST APIs through Axios.
-   The backend API URL is configured through frontend environment
    variables.
-   CORS allows configured frontend origins.
-   UI components remain separate from API service logic.

### 5.2 REST API

-   Organize API endpoints with FastAPI routers.
-   Use Pydantic schemas to validate request and response data.
-   Use consistent JSON responses and HTTP status codes.
-   Use `/api/v1` as the API prefix.
-   Provide interactive Swagger UI documentation at `/docs`.

### 5.3 Authentication and Permissions

-   Support registration, login, and logout.
-   Store passwords using secure password hashing.
-   Distinguish regular users from administrators.
-   Require authentication for private endpoints.
-   Restrict administrator endpoints to administrators.
-   Return HTTP 401 for unauthenticated requests.
-   Return HTTP 403 when an authenticated user lacks required
    administrator permissions.
-   Enforce ownership checks on the backend.

### 5.4 Trip, Traveler, Expense, and Budget Management

-   Create, view, update, and delete trips.
-   Store trip names, destinations, dates, and statuses.
-   Validate trip date ranges.
-   Associate multiple travelers with a trip.
-   Create, view, update, and delete expenses.
-   Record each expense's amount, currency, date, category, and payment
    method.
-   Associate expenses with the correct trip.
-   Set trip and category budgets.
-   Calculate spending, remaining budgets, budget usage, and
    overspending.

### 5.5 Original Transaction Values

-   Store each expense's original amount and currency.
-   Never replace original values with converted values.
-   Store converted values separately when conversion is required.
-   Record the exchange rate used for a conversion.
-   Keep historical expense values stable when rates change.
-   Use precise numeric database types for financial amounts.

### 5.6 Dashboard and Analytics

The dashboard must use actual database records and FastAPI endpoints. It
must display:

-   Total expenses.
-   Total trips and active trips.
-   Spending in the user's base currency.
-   Remaining trip budgets.
-   Spending by category and trip.
-   Daily and monthly spending trends.
-   Budget-versus-actual comparisons.

Charts must update when selected filters change. The dashboard must
provide loading, error, and empty-data states.

## 6. Technology Stack

  Layer                 Technology
  --------------------- -----------------------------
  Frontend framework    React
  Frontend language     TypeScript
  Frontend tooling      Vite
  Routing               React Router
  HTTP client           Axios
  Styling               Tailwind CSS or Bootstrap 5
  Charts                Recharts or Plotly.js
  Backend language      Python 3.11+
  API framework         FastAPI
  Validation            Pydantic
  ORM                   SQLAlchemy 2.0
  ASGI server           Uvicorn
  Database migrations   Alembic
  Database              PostgreSQL on Neon

The project requirements mention "mySQL" in the supplied stack notes,
but the database section explicitly specifies PostgreSQL on Neon. This
document follows the explicit database requirement and does not add
MySQL support.

## 7. Data Requirements

The database must contain these core tables:

-   `users`
-   `trips`
-   `trip_travelers`
-   `expenses`
-   `categories`
-   `budgets`

Use primary keys, foreign keys, and suitable indexes. Alembic manages
schema changes.

## 8. Non-Functional Requirements

-   Frontend and backend must be deployable and runnable separately.
-   Private records must be protected by backend authorization checks.
-   API input must be validated.
-   Financial values must use precise numeric types.
-   API documentation must be available through Swagger UI.
-   Dashboard calculations must use actual database data.
-   Database schema changes must be managed with migrations.

## 9. Success Criteria

The project is successful when:

1.  React + TypeScript runs independently from FastAPI.
2.  FastAPI provides working, documented REST APIs.
3.  Authentication and administrator permissions work securely.
4.  Users can manage trips, travelers, expenses, and budgets.
5.  Original transaction amounts remain unchanged.
6.  Dashboard metrics and charts display actual database data.

## 10. Related Documents

-   `02-srs.md` defines detailed system requirements, permissions, and
    acceptance criteria.
-   `03-tdd.md` defines the proposed architecture, database design, API
    structure, and implementation approach.
