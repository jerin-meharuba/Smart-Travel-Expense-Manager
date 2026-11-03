# Vercel Deployment

This project deploys the React frontend and FastAPI backend together from the
same GitHub repository. The root `vercel.toml` defines two Vercel services:
`frontend/` is the web service and `backend/` is the FastAPI API service.

## Prerequisites

- A Vercel account connected to the GitHub repository.
- A Neon PostgreSQL database, or another managed PostgreSQL database.
- A production `DATABASE_URL` supplied by the database provider.
- A newly generated, private value for `SECRET_KEY`.

Do not add any of these values to Git, an `.env.example` file, screenshots, or
pull requests.

## Vercel Project Setup

1. Open Vercel and import `jerin-meharuba/Smart-Travel-Expense-Manager`.
2. Keep the repository root as the project root. Vercel reads `vercel.toml` to
   build the frontend and FastAPI services.
3. Add the following Production environment variables in Vercel Project
   Settings. Add the same variables to Preview only when a preview needs a
   working database.

| Variable | Production value |
| --- | --- |
| `DATABASE_URL` | Neon PostgreSQL SQLAlchemy URL using `postgresql+psycopg://` and `sslmode=require` |
| `SECRET_KEY` | A unique, long random secret used to sign JWTs |
| `FRONTEND_ORIGIN` | The exact Vercel frontend origin, for example `https://your-project.vercel.app` |
| `VITE_API_BASE_URL` | `/api/v1` |

`VITE_API_BASE_URL` is included in the frontend build, so redeploy after
changing it. The other variables are read by FastAPI at runtime.

## Database Migration

Before the first production deployment, run Alembic against Neon from a trusted
machine. Set `DATABASE_URL` only in that terminal session, then run:

```powershell
cd backend
alembic upgrade head
```

This creates the schema without relying on a serverless request to run a
migration. Confirm the migration completes before deploying the application.

## Deploy and Verify

1. Push the merged `main` branch to GitHub. Vercel creates a deployment from
   the connected repository.
2. Open the assigned HTTPS URL and register a test account.
3. Confirm the frontend can create, edit, and delete a trip, expense, and
   budget for that account.
4. Open `https://your-project.vercel.app/docs` and call `GET /health`.
5. Check Vercel deployment logs for backend errors and verify that browser API
   calls stay under `/api/v1`.
6. Sign out, reload the application, and confirm protected pages require login.

The API accepts browser requests only from `FRONTEND_ORIGIN`. Set it to the
exact deployed frontend URL instead of `*`.

## Local Development

Use the values in `backend/.env.example` and `frontend/.env.example` as local
templates. The regular local commands remain:

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

```powershell
cd frontend
npm install
npm run dev
```

For a local check that mirrors Vercel routing, install the Vercel CLI, link the
project, and run `vercel dev` from the repository root. Do not commit the
generated `.vercel` directory.
