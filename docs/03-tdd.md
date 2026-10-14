# Smart Travel Expense Planner --- Technical Design Document (TDD)

  Field               Details
  ------------------- ---------------------------------
  Product             Smart Travel Expense Planner
  Document            Technical Design Document (TDD)
  Version             1.0
  Status              Draft
  Related documents   `01-prd.md`, `02-srs.md`

## 1. Purpose

This document describes how to implement Smart Travel Expense Planner.
The PRD defines what the product must achieve. The SRS defines detailed
requirements and acceptance criteria. This TDD describes the proposed
architecture, database structure, API design, and security approach.

## 2. Architecture Overview

### 2.1 Architecture Decisions

  -----------------------------------------------------------------------
  Layer                   Choice                  Purpose
  ----------------------- ----------------------- -----------------------
  Frontend                React + TypeScript +    Independent browser
                          Vite                    application

  Routing                 React Router            Client-side navigation

  HTTP client             Axios                   REST API communication

  Styling                 Tailwind CSS or         UI styling
                          Bootstrap 5             

  Charts                  Recharts or Plotly.js   Dashboard
                                                  visualizations

  Backend                 FastAPI                 REST API application

  Validation              Pydantic                Request and response
                                                  schemas

  ORM                     SQLAlchemy 2.0          Database access

  ASGI server             Uvicorn                 Run FastAPI

  Migrations              Alembic                 Database schema changes

  Database                PostgreSQL on Neon      Persistent application
                                                  data
  -----------------------------------------------------------------------

The frontend and backend are separate applications. FastAPI does not
need to serve the frontend build.

### 2.2 Tech Stack

The selected technology stack is:

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

The frontend stack supports an independently deployed browser
application. The backend stack supports documented REST APIs, schema
validation, database-backed business logic, and managed migrations.

### 2.3 High-Level Architecture

``` mermaid
flowchart LR
    User[User's Browser] --> UI[React + TypeScript]
    UI --> Axios[Axios API Client]
    Axios -->|HTTPS / JSON| API[FastAPI /api/v1]
    API --> Auth[Authentication and Permissions]
    API --> Schemas[Pydantic Schemas]
    Auth --> Services[Application Services]
    Schemas --> Services
    Services --> ORM[SQLAlchemy 2.0]
    ORM --> DB[(PostgreSQL on Neon)]
    API --> Docs[Swagger UI /docs]
    API --> Migrations[Alembic migrations]
```

### 2.4 Request Flow

1.  A user interacts with the React frontend.
2.  A frontend service sends a request through Axios.
3.  FastAPI receives the request under `/api/v1`.
4.  Authentication and authorization dependencies validate access.
5.  Pydantic validates request data.
6.  The service applies business rules and uses SQLAlchemy.
7.  PostgreSQL stores or retrieves the data.
8.  FastAPI returns a JSON response and suitable HTTP status.
9.  The frontend updates the page or displays loading, error, or empty
    states.

## 3. Repository Structure

A suggested monorepo layout is:

``` text
smart-travel-expense-planner/
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   └── services/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   ├── trips/
│   │   │   ├── travelers/
│   │   │   ├── expenses/
│   │   │   ├── budgets/
│   │   │   └── dashboard/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── types/
│   │   └── main.tsx
│   ├── .env.example
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── api.py
│   │   │       └── endpoints/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── alembic/
│   ├── alembic.ini
│   ├── .env.example
│   └── pyproject.toml
└── README.md
```

Keep API calls in frontend service modules. Keep authorization and
business rules in the backend.

## 4. Frontend Design

### 4.1 API Client

-   Configure one shared Axios instance.
-   Read the API base URL from a Vite environment variable such as
    `VITE_API_BASE_URL`.
-   Use `/api/v1` in the configured API base URL or in a shared API
    prefix, but avoid duplicating it.
-   Centralize request and error handling.
-   Do not put secrets in frontend environment variables.

Example:

``` typescript
import axios from "axios";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});
```

Example frontend environment setting:

``` text
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 4.2 UI Organization

-   Use React Router for page navigation.
-   Group features by authentication, trips, travelers, expenses,
    budgets, and dashboard.
-   Keep API service logic separate from presentation components.
-   Use TypeScript types for API request and response data.
-   Show loading, error, and empty-data states.
-   Refresh dashboard queries when relevant filters change.

## 5. Backend Design

### 5.1 Application Layers

  Layer               Responsibility
  ------------------- ---------------------------------------------------
  API routers         Define HTTP endpoints and status codes
  Pydantic schemas    Validate requests and shape responses
  Dependencies        Provide database sessions and authenticated users
  Services            Apply business rules and coordinate operations
  SQLAlchemy models   Map Python objects to database tables
  Database session    Manage PostgreSQL connections and transactions
  Alembic             Version and apply schema migrations

### 5.2 FastAPI Application

Mount application routers under `/api/v1`. Keep Swagger UI enabled at
`/docs` for interactive API documentation.

Example:

``` python
from fastapi import FastAPI
from app.api.v1.api import api_router

app = FastAPI(title="Smart Travel Expense Planner")
app.include_router(api_router, prefix="/api/v1")
```

### 5.3 Configuration

Read secrets and environment-specific settings from backend environment
variables. Do not commit production credentials.

Example backend environment settings:

``` text
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/DBNAME
SECRET_KEY=replace-with-a-strong-random-secret
FRONTEND_ORIGIN=http://localhost:5173
```

The example values are placeholders. Configure the real Neon connection
string and secret outside source control.

## 6. Database Design

### 6.1 Data Model

``` mermaid
erDiagram
    USERS ||--o{ TRIPS : owns
    TRIPS ||--o{ TRIP_TRAVELERS : includes
    TRIPS ||--o{ EXPENSES : contains
    CATEGORIES ||--o{ EXPENSES : classifies
    USERS ||--o{ CATEGORIES : owns_or_creates
    TRIPS ||--o{ BUDGETS : has
    CATEGORIES ||--o{ BUDGETS : limits
    USERS ||--o{ BUDGETS : owns
```

The exact ownership model for shared travelers and categories should be
confirmed during implementation. Access checks must follow the
authenticated user's ownership of the parent trip or record.

### 6.2 Core Tables

The following is the proposed minimum data model. Use SQLAlchemy 2.0
models and Alembic migrations to implement it.

#### `users`

  -----------------------------------------------------------------------
  Column                  Type                    Rules / Purpose
  ----------------------- ----------------------- -----------------------
  `id`                    UUID or integer         Primary key

  `email`                 String                  Required, unique,
                                                  indexed

  `password_hash`         String                  Required; never store
                                                  plain-text passwords

  `role`                  String or enum          Required; regular user
                                                  or administrator

  `created_at`            Timestamp with time     Required
                          zone                    
  -----------------------------------------------------------------------

#### `trips`

  Column              Type                       Rules / Purpose
  ------------------- -------------------------- ---------------------------------------
  `id`                UUID or integer            Primary key
  `user_id`           Same type as `users.id`    Required foreign key, indexed
  `name`              String                     Required
  `destination`       String                     Required
  `start_date`        Date                       Required
  `end_date`          Date                       Required; must not precede start date
  `status`            String or enum             Required
  `budget_amount`     Numeric                    Optional trip budget
  `budget_currency`   String                     Required when a trip budget is set
  `created_at`        Timestamp with time zone   Required
  `updated_at`        Timestamp with time zone   Required

#### `trip_travelers`

  Column         Type                       Rules / Purpose
  -------------- -------------------------- -------------------------------
  `id`           UUID or integer            Primary key
  `trip_id`      Same type as `trips.id`    Required foreign key, indexed
  `name`         String                     Required
  `email`        String                     Optional, if collected
  `created_at`   Timestamp with time zone   Required

Use a uniqueness rule only if the product defines what makes a traveler
unique within a trip.

#### `categories`

  -----------------------------------------------------------------------
  Column                  Type                    Rules / Purpose
  ----------------------- ----------------------- -----------------------
  `id`                    UUID or integer         Primary key

  `user_id`               Same type as `users.id` Optional foreign key
                                                  for user-owned
                                                  categories

  `name`                  String                  Required

  `created_at`            Timestamp with time     Required
                          zone                    
  -----------------------------------------------------------------------

If system-wide default categories are required, define their ownership
convention explicitly.

#### `expenses`

  -----------------------------------------------------------------------
  Column                  Type                    Rules / Purpose
  ----------------------- ----------------------- -----------------------
  `id`                    UUID or integer         Primary key

  `trip_id`               Same type as `trips.id` Required foreign key,
                                                  indexed

  `category_id`           Same type as            Required foreign key,
                          `categories.id`         indexed

  `amount_original`       Numeric(precision,      Required; original
                          scale)                  transaction amount

  `currency_original`     String                  Required; original
                                                  currency code

  `expense_date`          Date                    Required

  `payment_method`        String                  Required if collected
                                                  by the UI

  `amount_converted`      Numeric(precision,      Nullable; separate
                          scale)                  converted value

  `currency_converted`    String                  Nullable; target
                                                  currency

  `exchange_rate`         Numeric(precision,      Nullable; rate used for
                          scale)                  conversion

  `converted_at`          Timestamp with time     Nullable; conversion
                          zone                    timestamp

  `created_at`            Timestamp with time     Required
                          zone                    

  `updated_at`            Timestamp with time     Required
                          zone                    
  -----------------------------------------------------------------------

Never update `amount_original` or `currency_original` as a side effect
of currency conversion. Choose numeric precision and scale based on
supported currencies and calculation needs.

#### `budgets`

  -----------------------------------------------------------------------
  Column                  Type                    Rules / Purpose
  ----------------------- ----------------------- -----------------------
  `id`                    UUID or integer         Primary key

  `user_id`               Same type as `users.id` Required foreign key,
                                                  indexed

  `trip_id`               Same type as `trips.id` Nullable foreign key,
                                                  indexed

  `category_id`           Same type as            Nullable foreign key,
                          `categories.id`         indexed

  `amount`                Numeric(precision,      Required planned budget
                          scale)                  

  `currency`              String                  Required currency code

  `created_at`            Timestamp with time     Required
                          zone                    

  `updated_at`            Timestamp with time     Required
                          zone                    
  -----------------------------------------------------------------------

Define a validation rule so each budget targets the intended trip,
category, or combination. Avoid ambiguous budget records.

### 6.3 Database Rules

-   Use primary keys for every table.
-   Use foreign keys for relationships.
-   Add indexes to foreign keys and frequently filtered fields.
-   Use precise `NUMERIC` columns for financial amounts and rates.
-   Store timestamps with time zone where timestamps are needed.
-   Use database transactions for related multi-record changes.
-   Use Alembic migrations for schema changes.
-   Do not expose database credentials to the frontend.

## 7. REST API Design

All application endpoints use `/api/v1`. The paths below are a proposed
initial API contract and can be adjusted during implementation while
preserving the SRS requirements.

### 7.1 Authentication

  --------------------------------------------------------------------------------------
  Method         Path                      Purpose         Success        Common errors
  -------------- ------------------------- --------------- -------------- --------------
  `POST`         `/api/v1/auth/register`   Register user   `201`          `400`, `422`

  `POST`         `/api/v1/auth/login`      Authenticate    `200`          `401`, `422`
                                           user                           

  `POST`         `/api/v1/auth/logout`     End             `204`          `401`
                                           authenticated                  
                                           session or                     
                                           invalidate                     
                                           applicable                     
                                           token                          

  `GET`          `/api/v1/auth/me`         Return current  `200`          `401`
                                           user                           
  --------------------------------------------------------------------------------------

The exact authentication transport, such as secure cookies or bearer
tokens, must be selected before implementation. Apply appropriate CSRF
protections if cookie-based authentication is used.

### 7.2 Trips

  ---------------------------------------------------------------------------------------
  Method         Path                        Purpose        Success        Common errors
  -------------- --------------------------- -------------- -------------- --------------
  `GET`          `/api/v1/trips`             List           `200`          `401`
                                             accessible                    
                                             trips                         

  `POST`         `/api/v1/trips`             Create trip    `201`          `401`, `422`

  `GET`          `/api/v1/trips/{trip_id}`   Get one trip   `200`          `401`, `404`

  `PATCH`        `/api/v1/trips/{trip_id}`   Update trip    `200`          `401`, `404`,
                                                                           `422`

  `DELETE`       `/api/v1/trips/{trip_id}`   Delete trip    `204`          `401`, `404`
  ---------------------------------------------------------------------------------------

### 7.3 Travelers

  ---------------------------------------------------------------------------------------------------------------
  Method         Path                                                Purpose        Success        Common errors
  -------------- --------------------------------------------------- -------------- -------------- --------------
  `GET`          `/api/v1/trips/{trip_id}/travelers`                 List trip      `200`          `401`, `404`
                                                                     travelers                     

  `POST`         `/api/v1/trips/{trip_id}/travelers`                 Add traveler   `201`          `401`, `404`,
                                                                                                   `422`

  `DELETE`       `/api/v1/trips/{trip_id}/travelers/{traveler_id}`   Remove         `204`          `401`, `404`
                                                                     traveler                      
  ---------------------------------------------------------------------------------------------------------------

### 7.4 Expenses

  ---------------------------------------------------------------------------------------------------
  Method         Path                              Purpose              Success        Common errors
  -------------- --------------------------------- -------------------- -------------- --------------
  `GET`          `/api/v1/expenses`                List accessible      `200`          `401`
                                                   expenses; support                   
                                                   trip/date/category                  
                                                   filters as needed                   

  `POST`         `/api/v1/expenses`                Create expense       `201`          `401`, `404`,
                                                                                       `422`

  `GET`          `/api/v1/expenses/{expense_id}`   Get expense          `200`          `401`, `404`

  `PATCH`        `/api/v1/expenses/{expense_id}`   Update expense       `200`          `401`, `404`,
                                                                                       `422`

  `DELETE`       `/api/v1/expenses/{expense_id}`   Delete expense       `204`          `401`, `404`
  ---------------------------------------------------------------------------------------------------

### 7.5 Categories and Budgets

  -------------------------------------------------------------------------------------------
  Method         Path                            Purpose        Success        Common errors
  -------------- ------------------------------- -------------- -------------- --------------
  `GET`          `/api/v1/categories`            List available `200`          `401`
                                                 categories                    

  `POST`         `/api/v1/categories`            Create         `201`          `401`, `422`
                                                 category if                   
                                                 user-managed                  
                                                 categories are                
                                                 enabled                       

  `GET`          `/api/v1/budgets`               List           `200`          `401`
                                                 accessible                    
                                                 budgets                       

  `POST`         `/api/v1/budgets`               Create budget  `201`          `401`, `404`,
                                                                               `422`

  `PATCH`        `/api/v1/budgets/{budget_id}`   Update budget  `200`          `401`, `404`,
                                                                               `422`

  `DELETE`       `/api/v1/budgets/{budget_id}`   Delete budget  `204`          `401`, `404`
  -------------------------------------------------------------------------------------------

### 7.6 Dashboard

  ---------------------------------------------------------------------------------------------------------------
  Method         Path                                       Purpose                 Success        Common errors
  -------------- ------------------------------------------ ----------------------- -------------- --------------
  `GET`          `/api/v1/dashboard/summary`                Return summary metrics  `200`          `401`

  `GET`          `/api/v1/dashboard/spending-by-category`   Return category totals  `200`          `401`

  `GET`          `/api/v1/dashboard/spending-by-trip`       Return trip totals      `200`          `401`

  `GET`          `/api/v1/dashboard/spending-trends`        Return daily or monthly `200`          `401`
                                                            series                                 

  `GET`          `/api/v1/dashboard/budget-comparison`      Return                  `200`          `401`
                                                            planned-versus-actual                  
                                                            values                                 
  ---------------------------------------------------------------------------------------------------------------

Dashboard endpoints should accept documented date, trip, or category
filters where appropriate. All calculations must query actual authorized
database records.

### 7.7 Administrator Endpoints

Add administrator endpoints only for administrator functions required by
the product. Every such endpoint must use a backend dependency that
verifies the authenticated user's administrator role. Do not rely on
frontend route guards as the security boundary.

## 8. API Schema Examples

The examples illustrate the expected data shape. Exact schema names and
optional fields can be finalized during implementation.

### 8.1 Expense Creation Request

``` json
{
  "trip_id": "trip-id",
  "category_id": "category-id",
  "amount_original": "125.50",
  "currency_original": "USD",
  "expense_date": "2026-10-10",
  "payment_method": "card"
}
```

Represent financial values as decimal strings in JSON where appropriate
to avoid client-side floating-point precision loss. The backend must
validate the amount and currency.

### 8.2 Dashboard Summary Response

``` json
{
  "total_expenses": "1250.50",
  "base_currency": "USD",
  "total_trips": 4,
  "active_trips": 1,
  "remaining_trip_budgets": "749.50"
}
```

This is an illustrative response shape, not real project data. The API
must calculate returned values from the database and authorized records.

## 9. Security Design

-   Hash passwords with a maintained password-hashing library.
-   Keep signing secrets and database credentials in environment
    configuration.
-   Require authentication for private endpoints.
-   Enforce administrator role checks on the backend.
-   Check record ownership for trips, travelers, expenses, categories,
    and budgets.
-   Avoid revealing whether another user's private record exists.
-   Validate IDs, amounts, dates, currency codes, and relationships.
-   Configure CORS for known frontend origins.
-   Use HTTPS in deployed environments.
-   Do not log passwords, tokens, database URLs, or other secrets.
-   Apply database transactions where multiple related records must
    change together.

## 10. Error Handling

Use a consistent JSON error shape. For example:

``` json
{
  "detail": "A concise error message"
}
```

Use appropriate status codes: - `401` for missing or invalid
authentication. - `403` for an authenticated user lacking required
permissions. - `404` when a resource is missing or not accessible under
the disclosure policy. - `422` for Pydantic validation errors. - `500`
for unexpected failures, without returning stack traces or secrets to
clients.

## 11. Environment and Configuration

### 11.1 Frontend

``` text
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Vite exposes variables prefixed with `VITE_` to frontend code. Never
store private keys or server secrets in frontend environment variables.

### 11.2 Backend

``` text
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/DBNAME
SECRET_KEY=replace-with-a-strong-random-secret
FRONTEND_ORIGIN=http://localhost:5173
```

Use a PostgreSQL driver compatible with the chosen SQLAlchemy setup.
Keep `.env` files out of version control and provide only placeholder
values in `.env.example`.

## 12. Migrations and Deployment

-   Create an initial Alembic migration for the required tables and
    constraints.
-   Review generated migrations before applying them.
-   Use environment-specific database URLs.
-   Run migrations as a controlled deployment step.
-   Run frontend and backend as separate processes or services.
-   Configure production CORS origins explicitly.
-   Use HTTPS and secure secret management in production.

## 13. Testing Strategy

  -----------------------------------------------------------------------
  Area                                Tests
  ----------------------------------- -----------------------------------
  Authentication                      Registration, login, logout,
                                      invalid credentials, protected
                                      endpoints

  Authorization                       Regular-user/admin access,
                                      cross-user record isolation

  Trips                               CRUD operations and date validation

  Travelers                           Add, list, remove, and trip
                                      ownership checks

  Expenses                            CRUD, field validation, trip
                                      association, original amount
                                      preservation

  Budgets                             Create/update budgets and calculate
                                      remaining amounts

  Dashboard                           Metrics and charts' API data match
                                      database records

  API                                 Status codes, schema validation,
                                      `/docs`, `/api/v1` routing

  Database                            Foreign keys, indexes, migration
                                      upgrade and downgrade where
                                      supported

  Frontend                            API errors, loading and empty
                                      states, filter-driven chart updates
  -----------------------------------------------------------------------

## 14. Risks and Decisions to Confirm

  -----------------------------------------------------------------------
  Item                                Risk / decision
  ----------------------------------- -----------------------------------
  Authentication transport            Decide between secure cookie
                                      sessions and bearer tokens before
                                      implementation.

  Administrator capabilities          Define the exact administrator
                                      actions needed; enforce them
                                      server-side.

  Base currency                       Define where the user's base
                                      currency is stored and how totals
                                      are calculated.

  Currency conversion                 Conversion is conditional in the
                                      requirements. If implemented,
                                      preserve original values and store
                                      rate metadata.

  Traveler identity                   Confirm whether travelers are
                                      simple trip contacts or registered
                                      user accounts.

  Budget targeting                    Define whether budgets target a
                                      trip, a category, or a category
                                      within a trip.

  Database IDs                        Choose UUID or integer IDs
                                      consistently before the initial
                                      migration.
  -----------------------------------------------------------------------

## 15. Requirement Traceability

  Requirement area               PRD           SRS
  ------------------------------ ------------- ----------------
  Independent frontend/backend   Section 5.1   FR-01 to FR-03
  REST API and documentation     Section 5.2   FR-04 to FR-07
  Authentication and roles       Section 5.3   FR-08 to FR-14
  Trips and travelers            Section 5.4   FR-15 to FR-20
  Expenses and budgets           Section 5.4   FR-21 to FR-27
  Original transaction values    Section 5.5   FR-28 to FR-32
  Dashboard and analytics        Section 5.6   FR-33 to FR-39
  Database migrations            Section 7     NFR-06
