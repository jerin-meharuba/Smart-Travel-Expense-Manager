import React from "react";

const dashboardItems = [
  "Track trip expenses",
  "Manage travel budgets",
  "Review spending summaries",
];

function App() {
  return (
    <main>
      <h1>Smart Travel Expense Manager</h1>
      <p>Plan trips, record expenses, and monitor travel budgets.</p>
      <ul>
        {dashboardItems.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </main>
  );
}

export default App;
