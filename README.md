# Smart Travel Expense Manager

Smart Travel Expense Manager is a university web application for planning
trips, recording expenses, assigning categories, and monitoring travel budgets.
Registered users can manage their own travel data, while administrators can
manage user accounts.

## Technology Stack

| Area | Technology |
| --- | --- |
| Frontend | React, TypeScript, Vite, Axios, Recharts |
| Backend | Python, FastAPI, SQLAlchemy 2.0, Alembic |
| Database | SQLite for local development, PostgreSQL/Neon for production |
| Authentication | JWT bearer tokens with Argon2 password hashing |
| Hosting | Vercel services for the React frontend and FastAPI API |

## Features

- User registration, login, and profile access.
- Trip, expense, and budget management.
- Seeded, read-only expense categories.
- Dashboard summaries and category spending data.
  

## Project Structure

```text
Smart-Travel-Expense-Manager/
|-- backend/
|   |-- alembic/
|   |-- app/
|   |   |-- auth/
|   |   |-- admin/
|   |   |-- trips/
|   |   |-- expenses/
|   |   |-- budgets/
|   |   |-- categories/
|   |   |-- dashboard/
|   |   `-- main.py
|   `-- requirements.txt
|-- frontend/
|   |-- src/
|   `-- package.json
|-- docs/
|-- vercel.json
`-- README.md
```

## Run Locally

### Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --reload
```

The local API is available at `http://localhost:8000`, with Swagger UI at
`http://localhost:8000/docs` and the health check at
`http://localhost:8000/health`.

Copy `backend/.env.example` to a local `.env` file only if you need to override
the SQLite fallback. Never commit a `.env` file.

### Frontend

In a separate terminal, run:

```powershell
cd frontend
npm install
npm run dev
```

Vite displays the local frontend URL, usually `http://localhost:5173`.
Copy `frontend/.env.example` to a local `.env` file when changing the API base
URL.

## Deployment

The application is configured for Vercel with React and FastAPI deployed as
services from this repository. Production uses PostgreSQL through Neon or
another managed PostgreSQL provider.

Follow the full environment-variable, migration, deployment, and verification
checklist in [docs/deployment.md](docs/deployment.md). Do not place database
URLs, JWT secrets, or Vercel values in the repository.

## Documentation

- [Full Project Documentation](docs/project-documentation.md)
- [Product Requirements Document](docs/01-prd.md)
- [Software Requirements Specification](docs/02-srs.md)
- [Technical Design Document](docs/03-tdd.md)
- [Deployment Guide](docs/deployment.md)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
