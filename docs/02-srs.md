# Smart Travel Expense Planner --- Software Requirements Specification (SRS)

  Field               Details
  ------------------- -------------------------------------------
  Product             Smart Travel Expense Planner
  Document            Software Requirements Specification (SRS)
  Version             1.0
  Status              Draft
  Related documents   `01-prd.md`, `03-tdd.md`

## 1. Introduction

### 1.1 Purpose

This document defines the functional and non-functional requirements for
Smart Travel Expense Planner. It converts the product goals into
requirements that can be implemented and tested.

### 1.2 Scope

The system contains a React + TypeScript frontend, a FastAPI backend,
and a PostgreSQL database hosted on Neon. The frontend and backend run
independently and communicate through REST APIs.

### 1.3 Requirement Language

-   **Must** means the requirement is mandatory.
-   **Should** means the requirement is expected unless a reason is
    documented.
-   Requirement identifiers use `FR-xx` for functional requirements and
    `NFR-xx` for non-functional requirements.

## 2. System Overview

### 2.1 User Roles

  -----------------------------------------------------------------------
  Role                                Permissions
  ----------------------------------- -----------------------------------
  Regular user                        Register, log in, and manage only
                                      records they own or are authorized
                                      to access.

  Administrator                       Access administrator-only endpoints
                                      and functions.
  -----------------------------------------------------------------------

The backend must validate authentication, role, and record ownership.
Hiding frontend controls is not sufficient authorization.

### 2.2 System Components

-   React + TypeScript frontend built with Vite.
-   FastAPI backend with versioned REST endpoints.
-   PostgreSQL database hosted on Neon.
-   SQLAlchemy 2.0 for database access.
-   Alembic for database migrations.
-   Swagger UI for API documentation.

## 3. Functional Requirements

### 3.1 Frontend and Backend Separation

**FR-01 --- Independent applications**

The frontend and backend must run as separate applications.

**Acceptance criteria** - The frontend can start without being hosted by
FastAPI. - The backend can start without serving the frontend. - The
frontend communicates with the backend over HTTP REST APIs.

**FR-02 --- API client configuration**

The frontend must use Axios for API requests and read the backend URL
from an environment variable.

**Acceptance criteria** - API service logic is separate from UI
components. - Changing the configured backend URL does not require
editing individual components.

**FR-03 --- CORS configuration**

The backend must allow configured frontend origins through CORS
settings.

**Acceptance criteria** - Requests from an allowed frontend origin can
reach the API. - Origins are configured explicitly rather than allowing
arbitrary origins by default.

### 3.2 REST API and Validation

**FR-04 --- Versioned API**

The backend must expose application endpoints under `/api/v1`.

**FR-05 --- Request validation**

The backend must use Pydantic schemas to validate request data.

**Acceptance criteria** - Invalid request data receives an appropriate
client-error status. - Invalid input does not create or modify database
records.

**FR-06 --- API documentation**

FastAPI must provide interactive Swagger UI documentation at `/docs`.

**Acceptance criteria** - Implemented endpoints appear in the generated
API documentation. - Request fields, response schemas, and relevant
status codes are documented.

**FR-07 --- Consistent responses**

The API must return JSON responses and suitable HTTP status codes.

### 3.3 Authentication and Authorization

**FR-08 --- Registration**

A visitor must be able to create a user account using valid registration
data.

**FR-09 --- Login and logout**

Users must be able to log in and log out. Private API access must
require valid authentication.

**FR-10 --- Password storage**

Passwords must be stored using a secure password-hashing method.
Plain-text passwords must not be stored.

**FR-11 --- Role enforcement**

The system must distinguish regular users and administrators.
Administrator-only endpoints must reject non-administrator users.

**FR-12 --- Authentication error**

Unauthenticated requests to protected endpoints must return HTTP 401.

**FR-13 --- Authorization error**

An authenticated user without the required administrator permission must
receive HTTP 403.

**FR-14 --- Record ownership**

Users must not read, update, or delete another user's private records by
changing an identifier in a request.

**Acceptance criteria for FR-08--FR-14** - Valid users can
authenticate. - Invalid credentials do not grant access. - Protected
endpoints reject unauthenticated requests. - Regular users cannot use
administrator-only endpoints. - Ownership checks are performed by the
backend.

### 3.4 Trip Management

**FR-15 --- Trip CRUD**

Authorized users must be able to create, view, update, and delete their
trips.

**FR-16 --- Trip fields**

A trip must support a name, destination, start date, end date, and
status.

**FR-17 --- Trip date validation**

The system must reject invalid date ranges where the end date is earlier
than the start date.

**FR-18 --- Trip budgets**

Users must be able to assign a budget to a trip.

### 3.5 Traveler Management

**FR-19 --- Multiple travelers**

A trip must support multiple traveler records.

**FR-20 --- Traveler operations**

Authorized users must be able to add, view, and remove travelers
associated with a trip.

**Acceptance criteria** - A traveler is associated with the correct
trip. - Users cannot manage travelers belonging to trips they cannot
access.

### 3.6 Expense Management

**FR-21 --- Expense CRUD**

Authorized users must be able to create, view, update, and delete
expenses.

**FR-22 --- Expense fields**

An expense must record amount, currency, date, category, payment method,
and associated trip.

**FR-23 --- Expense ownership**

The backend must verify access to the expense and its associated trip
before allowing access or modification.

**FR-24 --- Original amount preservation**

The original amount and currency must remain stored separately from any
converted values.

### 3.7 Budget Management

**FR-25 --- Budget configuration**

Users must be able to set budgets for trips and expense categories.

**FR-26 --- Budget calculations**

The system must calculate actual spending, remaining budget, and budget
usage from stored expenses.

**FR-27 --- Budget comparison**

The system must compare actual spending with planned budgets and
indicate overspending.

### 3.8 Financial Data Integrity

**FR-28 --- Preserve source transaction**

The system must not overwrite the original expense amount or currency
during calculations.

**FR-29 --- Separate converted values**

If currency conversion is implemented, converted amounts must be stored
separately from original values.

**FR-30 --- Conversion rate record**

If a converted amount is stored, the exchange rate used for that
conversion must also be recorded.

**FR-31 --- Historical stability**

Updating a currency rate must not silently alter previously stored
original amounts or historical converted transaction records.

**FR-32 --- Numeric precision**

Financial amounts and exchange rates must use suitable precise database
numeric types rather than binary floating-point storage for transaction
amounts.

### 3.9 Dashboard and Analytics

**FR-33 --- Database-backed metrics**

Dashboard metrics must be calculated from actual database records
through FastAPI endpoints.

**FR-34 --- Summary metrics**

The dashboard must show total expenses, total trips, active trips,
base-currency spending, and remaining trip budgets.

**FR-35 --- Spending breakdowns**

The dashboard must show spending by category and by trip.

**FR-36 --- Spending trends**

The dashboard must show daily and monthly spending trends.

**FR-37 --- Budget comparison**

The dashboard must compare planned budgets with actual spending.

**FR-38 --- Interactive charts**

Charts must use Recharts or Plotly.js and update when selected filters
change.

**FR-39 --- Dashboard states**

The frontend must show loading, error, and empty-data states.

## 4. Non-Functional Requirements

**NFR-01 --- Separation**

Frontend and backend must be independently runnable applications.

**NFR-02 --- Security**

The backend must enforce authentication, role permissions, and record
ownership.

**NFR-03 --- Validation**

Incoming API data must be validated before database changes are made.

**NFR-04 --- Financial accuracy**

Financial values must use precise numeric database types, and original
transaction values must remain unchanged.

**NFR-05 --- Documentation**

The API must provide interactive documentation at `/docs`.

**NFR-06 --- Database change management**

Database schema changes must be managed using Alembic migrations.

**NFR-07 --- Dashboard data source**

Dashboard figures and charts must reflect actual database data rather
than hard-coded sample values.

## 5. Data Requirements

The required database tables are:

  Table              Purpose
  ------------------ -------------------------------------------------------
  `users`            User accounts, authentication data, and role
  `trips`            Trip details and ownership
  `trip_travelers`   Travelers associated with trips
  `expenses`         Expense transaction data and original currency values
  `categories`       Expense categories
  `budgets`          Trip and category budget values

Tables must use primary keys, foreign keys, and suitable indexes. Exact
columns and constraints are specified in `03-tdd.md`.

## 6. HTTP Status Code Requirements

  -----------------------------------------------------------------------
  Status                              Required use
  ----------------------------------- -----------------------------------
  `200 OK`                            Successful read or update response
                                      when a response body is returned

  `201 Created`                       Successful resource creation

  `204 No Content`                    Successful operation with no
                                      response body, when appropriate

  `400 Bad Request`                   Invalid operation or request that
                                      cannot be processed

  `401 Unauthorized`                  Missing or invalid authentication

  `403 Forbidden`                     Authenticated user lacks required
                                      permission

  `404 Not Found`                     Resource does not exist or is not
                                      accessible under the application's
                                      disclosure policy

  `422 Unprocessable Entity`          Request data fails schema
                                      validation

  `500 Internal Server Error`         Unexpected server failure without
                                      exposing secrets
  -----------------------------------------------------------------------

## 7. Acceptance Checklist

-   [ ] React + TypeScript frontend runs independently.
-   [ ] FastAPI backend runs independently.
-   [ ] Frontend uses Axios and an environment-configured API URL.
-   [ ] REST endpoints use `/api/v1`.
-   [ ] Swagger UI is available at `/docs`.
-   [ ] Registration, login, and logout work.
-   [ ] Passwords are securely hashed.
-   [ ] Administrator permissions and record ownership are checked on
    the backend.
-   [ ] Trips, travelers, expenses, and budgets can be managed.
-   [ ] Original transaction amounts and currencies remain unchanged.
-   [ ] Dashboard metrics and charts use actual database records.
-   [ ] Alembic migrations manage schema changes.

## 8. Related Documents

-   `01-prd.md` describes product goals and scope.
-   `03-tdd.md` describes architecture, data models, and API design.
