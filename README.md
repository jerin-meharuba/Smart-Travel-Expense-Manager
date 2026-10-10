# Smart Travel Expense Manager

A full-stack travel expense management application built with React, TypeScript, FastAPI, and MySQL.

## Overview

Smart Travel Expense Manager helps users organize trips, travelers, expenses, and budgets in one place.

The application uses an independent React and TypeScript frontend and a FastAPI backend. The backend provides documented REST APIs and connects to a locally hosted MySQL database.

Original transaction amounts remain unchanged. Dashboard metrics and charts use actual database records.

## Project Goals

- Build an independent React and TypeScript frontend.
- Provide documented REST APIs through FastAPI.
- Implement secure authentication and administrator permissions.
- Allow users to manage trips, travelers, expenses, and budgets.
- Preserve original transaction amounts.
- Display dashboard metrics and charts using actual database data.
- Use a local MySQL database during development.
- Maintain a modular and maintainable project structure.

## Features

### Trip Management

- Create and manage travel trips.
- Store trip details and related information.
- Organize expenses by trip.

### Traveler Management

- Maintain traveler information.
- Associate travelers with relevant trips.
- Organize trip-related traveler records.

### Expense Management

- Create, view, update, and manage expenses.
- Store original transaction amounts without overwriting them.
- Associate expenses with trips and travelers.
- Support multi-currency expense records.

### Budget Management

- Create and manage travel budgets.
- Organize budgets around trips.
- Compare budgets with recorded expenses.

### Dashboard and Analytics

- Display expense and budget summaries.
- Calculate dashboard metrics from actual database records.
- Present expense information through charts.
- Keep displayed metrics consistent with stored data.

### Authentication and Authorization

- Provide secure user authentication.
- Enforce administrator permissions on protected operations.
- Validate permissions on the backend.
- Protect restricted API endpoints.

### REST API

- Provide backend functionality through REST endpoints.
- Document API operations using FastAPI's OpenAPI integration.
- Validate request and response data using Pydantic.
- Keep the frontend independent of backend implementation details.

## Technology Stack

### Frontend

- React
- TypeScript
- Vite
- React Router
- Axios
- Tailwind CSS or Bootstrap
- Recharts or Plotly

### Backend

- Python 3.11+
- FastAPI
- Pydantic
- SQLAlchemy 2.0
- PyMySQL
- Uvicorn
- Alembic

### Database

- MySQL Server running locally
- MySQL Workbench, optional, for database administration

### Development Tools

- Git and GitHub
- Visual Studio Code
- Python virtual environments
- Node.js and npm
- Environment variables for configuration
- Automated testing tools

## Project Structure

The following is the intended project structure. Actual files may be added as development progresses.

```text
smart-travel-expense-manager/
├── .agents/
│   └── skills/
├── .claude/
│   └── skills/
├── .vscode/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── migrations/
│   ├── tests/
│   ├── alembic.ini
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── features/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── routes/
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── docs/
│   ├── 01-prd.md
│   ├── 02-srs.md
│   └── 03-tdd.md
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
└── vercel.json
```

## Prerequisites

Install these tools before setting up the application:

- Git
- Python 3.11 or later
- Node.js and npm
- MySQL Server
- A code editor, such as Visual Studio Code

MySQL Workbench is optional but useful for inspecting databases and running SQL queries.

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd smart-travel-expense-manager
```

Replace `<repository-url>` with your actual repository URL.

### 2. Create a MySQL Database

Start your local MySQL Server.

Open MySQL Workbench or a MySQL command-line client. Run:

```sql
CREATE DATABASE smart_travel_expense
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE USER 'travel_app'@'localhost'
    IDENTIFIED BY 'replace_with_a_strong_password';

GRANT ALL PRIVILEGES
    ON smart_travel_expense.*
    TO 'travel_app'@'localhost';
```

Use a strong password for the database user. Do not use the example password in a real environment.

The application database is named `smart_travel_expense`.

### 3. Configure the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment.

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS or Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the backend dependencies:

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy pymysql alembic pydantic-settings
```

If the backend already has a `pyproject.toml` with dependencies configured, install the project dependencies instead:

```bash
pip install -e .
```

### 4. Configure Environment Variables

Create a `.env` file inside the backend directory.

Example:

```dotenv
APP_ENV=development
DATABASE_URL=mysql+pymysql://travel_app:YOUR_PASSWORD@127.0.0.1:3306/smart_travel_expense
SECRET_KEY=replace_with_a_secure_random_secret
```

Replace `YOUR_PASSWORD` with the password configured for your MySQL user.

Generate a strong secret key for authentication. Keep the `.env` file out of version control.

If your password contains special characters, URL-encode them in the database connection URL.

### 5. Configure the Frontend

Open a separate terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the dependencies:

```bash
npm install
```

Create a frontend `.env` file if one does not exist:

```dotenv
VITE_API_BASE_URL=http://localhost:8000
```

The frontend uses this value to communicate with the FastAPI backend.

Do not put database credentials or backend secret keys in frontend environment variables. Variables prefixed with `VITE_` may be exposed to browser code.

### 6. Run Database Migrations

Once SQLAlchemy models and Alembic configuration have been implemented, initialize or apply database migrations.

For an already configured Alembic project:

```bash
alembic upgrade head
```

Run this command from the directory containing `alembic.ini`, or provide the correct configuration path.

Migrations should create and update database tables. Avoid relying on manual table creation for the application schema.

### 7. Start the Backend

From the backend directory, activate the virtual environment and run:

```bash
uvicorn app.main:app --reload
```

The backend should be available at:

`http://localhost:8000`

The exact import path depends on the implemented application structure.

### 8. Start the Frontend

In a separate terminal:

```bash
cd frontend
npm run dev
```

Vite will display the local frontend URL in the terminal.

The frontend and backend run independently. Both must be running for the complete application to work locally.

## FastAPI and MySQL Configuration

Use SQLAlchemy 2.0 with the PyMySQL driver.

### Database Connection URL

```python
DATABASE_URL = (
    "mysql+pymysql://travel_app:YOUR_PASSWORD"
    "@127.0.0.1:3306/smart_travel_expense"
)
```

In the actual application, read this value from environment variables rather than hardcoding credentials.

### Database Session Setup

Example `backend/app/core/database.py`:

```python
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Load the backend `.env` file during application startup using your chosen settings configuration. For example, Pydantic Settings can load and validate environment variables.

### Database Dependency in FastAPI

Example endpoint:

```python
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db

app = FastAPI(
    title="Smart Travel Expense Manager API",
    version="1.0.0",
)


@app.get("/health/database")
def database_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}
```

This endpoint verifies that a database query can run. For production, protect or limit diagnostic endpoints as appropriate.

### Required Dependencies

The backend needs these packages for the recommended database setup:

```text
fastapi
uvicorn[standard]
sqlalchemy>=2.0
pymysql
alembic
pydantic-settings
```

Pin and maintain dependency versions through the project's dependency management configuration.

## API Documentation

FastAPI provides interactive API documentation when the backend is running.

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI schema:** `http://localhost:8000/openapi.json`

These endpoints depend on the application's documentation settings.

## Security

Follow these security practices:

- Authenticate users before granting access to protected resources.
- Enforce administrator permissions on the backend.
- Validate and authorize protected API operations.
- Store credentials and secret keys in environment variables.
- Use secure password hashing for password-based authentication.
- Avoid exposing sensitive information in logs.
- Configure CORS for approved frontend origins.
- Use HTTPS in production.
- Validate user input and handle errors safely.
- Use a dedicated database account with only the required permissions.

Frontend route protection alone is not sufficient for authorization.

## Data Integrity and Currency

Original transaction amounts must remain unchanged after they are recorded.

If currency conversion is supported, store converted values separately from original transaction values. Store currency codes and conversion details where appropriate.

Use suitable MySQL `DECIMAL` columns for monetary amounts instead of floating-point columns. Choose precision and scale based on the application's currency and calculation requirements.

Dashboard calculations should use actual database records rather than hardcoded demonstration values.

## Testing

Testing should cover:

- Authentication and authorization.
- Administrator-only operations.
- Trip and traveler management.
- Expense creation and updates.
- Original transaction amount preservation.
- Budget calculations.
- Dashboard metrics and chart data.
- REST API validation and error handling.
- MySQL persistence and database connectivity.
- Database migrations.
- Frontend and backend integration.

Use `pytest` for backend tests. Vitest and React Testing Library can be used for frontend tests when configured.

## Development Workflow

1. Create a feature branch for each task.
2. Implement changes in the relevant frontend, backend, or documentation area.
3. Add or update tests when application behavior changes.
4. Run available tests and checks.
5. Review changes before committing.
6. Open a pull request for review.
7. Merge after required checks pass.

## Deployment

The development database runs locally on the developer's computer.

For production, deploy the frontend and backend independently. A deployed backend cannot connect to a developer's `localhost` database because `localhost` refers to the machine running that backend.

A production deployment will therefore need an accessible database host and suitable network and security configuration.

Possible deployment components include:

- **Frontend:** Vercel or another frontend hosting service.
- **Backend:** A Python-compatible application hosting service.
- **Database:** A properly secured MySQL server or managed MySQL service.

Configure production environment variables and database credentials through the hosting provider. Restrict CORS to approved origins and use HTTPS.

## Project Documentation

Project documentation is intended to include:

- `docs/01-prd.md` — Product Requirements Document.
- `docs/02-srs.md` — Software Requirements Specification.
- `docs/03-tdd.md` — Technical Design Document.

These documents define the product scope, requirements, architecture, data model, API design, and implementation approach.

## Development Status

The project is intended to provide a React and TypeScript frontend, a FastAPI REST backend, secure authentication, and database-backed expense management.

The local MySQL configuration described here is the recommended development setup. Verify the actual repository files and dependencies before running setup commands.

## Contributing

Contributions should follow the repository's branch, testing, and pull request workflow.

Keep changes focused, document important decisions, add relevant tests, and never commit secrets or local configuration files.

## License

A license has not yet been specified. Add a `LICENSE` file before distributing the project under an open-source license.
