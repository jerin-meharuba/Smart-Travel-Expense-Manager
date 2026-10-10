# Smart Travel Expense Manager

A simple web application for managing travel expenses, trips, and budgets. This project is developed as part of a university Web Development course.

## About the Project

Smart Travel Expense Manager helps users organize their travel information and track expenses. Users can manage trips, record expenses, and monitor their budgets through a simple web interface.

The project uses React and TypeScript for the frontend, FastAPI for the backend, and MySQL for the database.

## Features

- Manage travel trips.
- Manage traveler information.
- Add, view, update, and delete expenses.
- Create and manage travel budgets.
- View expense summaries on a dashboard.
- User authentication and administrator permissions.
- Store travel and expense information in MySQL.

## Technology Stack

**Frontend**
- React
- TypeScript
- Vite
- Axios
- Tailwind CSS or Bootstrap

**Backend**
- Python
- FastAPI
- SQLAlchemy
- Uvicorn

**Database**
- MySQL Server (local)

**Tools**
- Visual Studio Code
- Git and GitHub
- MySQL Workbench (optional)

## Project Structure

```text
smart-travel-expense-manager/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── schemas/
│   │   └── routes/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/
├── README.md
├── LICENSE
└── .gitignore
```

This is the planned structure. Some folders and files may be added during development.

## Requirements

Install the following before running the project:

- Python 3.11 or later
- Node.js and npm
- MySQL Server
- Git

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd smart-travel-expense-manager
```

Replace `<repository-url>` with your GitHub repository URL.

### 2. Set Up the MySQL Database

Start MySQL and run the following SQL commands:

```sql
CREATE DATABASE smart_travel_expense;

CREATE USER 'travel_app'@'localhost'
IDENTIFIED BY 'your_password';

GRANT ALL PRIVILEGES
ON smart_travel_expense.*
TO 'travel_app'@'localhost';
```

Use your own database password.

### 3. Run the Backend

Open a terminal and navigate to the backend folder:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

**Windows:**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy pymysql
```

Configure the MySQL connection string using an environment variable:

```text
mysql+pymysql://travel_app:YOUR_PASSWORD@127.0.0.1:3306/smart_travel_expense
```

Replace `YOUR_PASSWORD` with your actual database password. The backend must read this value from its environment configuration.

Start the API after the backend application has been implemented:

```bash
uvicorn app.main:app --reload
```

The API will normally run at `http://localhost:8000`.

### 4. Run the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in your terminal.

## API Documentation

When the FastAPI backend is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

These pages show the API endpoints implemented in the backend.

## Database

MySQL stores the application's trips, travelers, expenses, and budgets.

The database runs locally during development. Keep your database password and other secrets out of GitHub.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
