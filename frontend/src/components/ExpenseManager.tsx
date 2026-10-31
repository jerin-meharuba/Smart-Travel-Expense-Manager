import { FormEvent, useEffect, useState } from "react";

import { expenseApi } from "../services/expenses";
import { tripApi } from "../services/trips";
import type { Category, Expense, ExpenseFormValues } from "../types/expense";
import type { Trip } from "../types/trip";

const emptyForm: ExpenseFormValues = {
  trip_id: "",
  category_id: "",
  amount_original: "",
  currency_original: "USD",
  expense_date: "",
  payment_method: "card",
};

function formValuesFromExpense(expense: Expense): ExpenseFormValues {
  return {
    trip_id: String(expense.trip_id),
    category_id: String(expense.category_id),
    amount_original: expense.amount_original,
    currency_original: expense.currency_original,
    expense_date: expense.expense_date,
    payment_method: expense.payment_method,
  };
}

export function ExpenseManager() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [trips, setTrips] = useState<Trip[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedExpense, setSelectedExpense] = useState<Expense | null>(null);
  const [formValues, setFormValues] = useState<ExpenseFormValues>(emptyForm);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  async function loadData() {
    setIsLoading(true);
    try {
      const [expenseResponse, tripResponse, categoryResponse] = await Promise.all([
        expenseApi.list(),
        tripApi.list(),
        expenseApi.listCategories(),
      ]);
      setExpenses(expenseResponse.items);
      setTrips(tripResponse.items);
      setCategories(categoryResponse);
      setError("");
    } catch {
      setError("Could not load expenses. Make sure the backend is running.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadData();
  }, []);

  function selectExpense(expense: Expense) {
    setSelectedExpense(expense);
    setFormValues(formValuesFromExpense(expense));
    setError("");
  }

  function startNewExpense() {
    setSelectedExpense(null);
    setFormValues(emptyForm);
    setError("");
  }

  async function saveExpense(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSaving(true);
    try {
      const savedExpense = selectedExpense
        ? await expenseApi.update(selectedExpense.id, formValues)
        : await expenseApi.create(formValues);

      setSelectedExpense(savedExpense);
      setFormValues(formValuesFromExpense(savedExpense));
      await loadData();
    } catch {
      setError("Could not save the expense. Check the selected trip and fields.");
    } finally {
      setIsSaving(false);
    }
  }

  async function deleteSelectedExpense() {
    if (!selectedExpense || !window.confirm("Delete this expense?")) {
      return;
    }

    try {
      await expenseApi.remove(selectedExpense.id);
      startNewExpense();
      await loadData();
    } catch {
      setError("Could not delete the expense.");
    }
  }

  function updateField(field: keyof ExpenseFormValues, value: string) {
    setFormValues((currentValues) => ({ ...currentValues, [field]: value }));
  }

  function tripName(tripId: number) {
    return trips.find((trip) => trip.id === tripId)?.name ?? "Unknown trip";
  }

  function categoryName(categoryId: number) {
    return categories.find((category) => category.id === categoryId)?.name ?? "Unknown category";
  }

  return (
    <section className="trip-layout">
      <div className="panel">
        <div className="actions">
          <h2>Expenses</h2>
          <button className="secondary-button" type="button" onClick={startNewExpense}>
            New expense
          </button>
        </div>

        {isLoading ? (
          <p>Loading expenses...</p>
        ) : expenses.length === 0 ? (
          <p>No expenses yet. Create an expense for one of your trips.</p>
        ) : (
          <div className="trip-list">
            {expenses.map((expense) => (
              <button
                className={`trip-card ${selectedExpense?.id === expense.id ? "selected" : ""}`}
                key={expense.id}
                type="button"
                onClick={() => selectExpense(expense)}
              >
                <strong>
                  {expense.amount_original} {expense.currency_original}
                </strong>
                <p>{tripName(expense.trip_id)}</p>
                <small>
                  {categoryName(expense.category_id)} - {expense.expense_date}
                </small>
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="panel">
        <h2>{selectedExpense ? "Edit expense" : "Create expense"}</h2>
        {trips.length === 0 ? (
          <p>Create a trip before adding an expense.</p>
        ) : (
          <form className="trip-form" onSubmit={saveExpense}>
            <label>
              Trip
              <select
                required
                value={formValues.trip_id}
                onChange={(event) => updateField("trip_id", event.target.value)}
              >
                <option value="">Select a trip</option>
                {trips.map((trip) => (
                  <option key={trip.id} value={trip.id}>
                    {trip.name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Category
              <select
                required
                value={formValues.category_id}
                onChange={(event) => updateField("category_id", event.target.value)}
              >
                <option value="">Select a category</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </label>
            <div className="two-column">
              <label>
                Amount
                <input
                  required
                  min="0.01"
                  step="0.01"
                  type="number"
                  value={formValues.amount_original}
                  onChange={(event) => updateField("amount_original", event.target.value)}
                />
              </label>
              <label>
                Currency
                <input
                  required
                  maxLength={3}
                  value={formValues.currency_original}
                  onChange={(event) => updateField("currency_original", event.target.value)}
                />
              </label>
            </div>
            <div className="two-column">
              <label>
                Expense date
                <input
                  required
                  type="date"
                  value={formValues.expense_date}
                  onChange={(event) => updateField("expense_date", event.target.value)}
                />
              </label>
              <label>
                Payment method
                <select
                  value={formValues.payment_method}
                  onChange={(event) => updateField("payment_method", event.target.value)}
                >
                  <option value="card">Card</option>
                  <option value="cash">Cash</option>
                  <option value="bank transfer">Bank transfer</option>
                </select>
              </label>
            </div>
            <div className="actions">
              <button className="primary-button" disabled={isSaving} type="submit">
                {isSaving ? "Saving..." : selectedExpense ? "Save changes" : "Create expense"}
              </button>
              {selectedExpense && (
                <button className="danger-button" type="button" onClick={deleteSelectedExpense}>
                  Delete expense
                </button>
              )}
            </div>
          </form>
        )}
      </div>
    </section>
  );
}
