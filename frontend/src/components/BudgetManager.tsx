import { FormEvent, useEffect, useState } from "react";

import { budgetApi } from "../services/budgets";
import { expenseApi } from "../services/expenses";
import { tripApi } from "../services/trips";
import type { Budget, BudgetFormValues } from "../types/budget";
import type { Category } from "../types/expense";
import type { Trip } from "../types/trip";

const emptyForm: BudgetFormValues = {
  trip_id: "",
  category_id: "",
  amount: "",
  currency: "USD",
};

function formValuesFromBudget(budget: Budget): BudgetFormValues {
  return {
    trip_id: budget.trip_id ? String(budget.trip_id) : "",
    category_id: budget.category_id ? String(budget.category_id) : "",
    amount: budget.amount,
    currency: budget.currency,
  };
}

export function BudgetManager() {
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [trips, setTrips] = useState<Trip[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedBudget, setSelectedBudget] = useState<Budget | null>(null);
  const [formValues, setFormValues] = useState<BudgetFormValues>(emptyForm);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  async function loadData() {
    setIsLoading(true);
    try {
      const [budgetResponse, tripResponse, categoryResponse] = await Promise.all([
        budgetApi.list(),
        tripApi.list(),
        expenseApi.listCategories(),
      ]);
      setBudgets(budgetResponse);
      setTrips(tripResponse.items);
      setCategories(categoryResponse);
      setError("");
    } catch {
      setError("Could not load budgets. Make sure the backend is running.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadData();
  }, []);

  function selectBudget(budget: Budget) {
    setSelectedBudget(budget);
    setFormValues(formValuesFromBudget(budget));
    setError("");
  }

  function startNewBudget() {
    setSelectedBudget(null);
    setFormValues(emptyForm);
    setError("");
  }

  function updateField(field: keyof BudgetFormValues, value: string) {
    setFormValues((currentValues) => ({ ...currentValues, [field]: value }));
  }

  async function saveBudget(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!formValues.trip_id && !formValues.category_id) {
      setError("Choose a trip, a category, or both for this budget.");
      return;
    }

    setIsSaving(true);
    try {
      const savedBudget = selectedBudget
        ? await budgetApi.update(selectedBudget.id, formValues)
        : await budgetApi.create(formValues);
      setSelectedBudget(savedBudget);
      setFormValues(formValuesFromBudget(savedBudget));
      await loadData();
    } catch {
      setError("Could not save the budget. Check the amount, currency, and target.");
    } finally {
      setIsSaving(false);
    }
  }

  async function deleteSelectedBudget() {
    if (!selectedBudget || !window.confirm("Delete this budget?")) {
      return;
    }
    try {
      await budgetApi.remove(selectedBudget.id);
      startNewBudget();
      await loadData();
    } catch {
      setError("Could not delete the budget.");
    }
  }

  function tripName(tripId: number | null) {
    if (!tripId) {
      return "All trips";
    }
    return trips.find((trip) => trip.id === tripId)?.name ?? "Unknown trip";
  }

  function categoryName(categoryId: number | null) {
    if (!categoryId) {
      return "All categories";
    }
    return categories.find((category) => category.id === categoryId)?.name ?? "Unknown category";
  }

  return (
    <section className="trip-layout">
      <div className="panel">
        <div className="actions">
          <h2>Budgets</h2>
          <button className="secondary-button" type="button" onClick={startNewBudget}>
            New budget
          </button>
        </div>

        {isLoading ? (
          <p>Loading budgets...</p>
        ) : budgets.length === 0 ? (
          <p>No budgets yet. Set a budget for a trip, category, or both.</p>
        ) : (
          <div className="trip-list">
            {budgets.map((budget) => (
              <button
                className={`trip-card ${selectedBudget?.id === budget.id ? "selected" : ""}`}
                key={budget.id}
                type="button"
                onClick={() => selectBudget(budget)}
              >
                <strong>
                  {budget.amount} {budget.currency}
                </strong>
                <p>
                  {tripName(budget.trip_id)} - {categoryName(budget.category_id)}
                </p>
                <small className={budget.is_overspent ? "budget-over" : "budget-ok"}>
                  Spent {budget.actual_spending}; remaining {budget.remaining_amount}; {budget.usage_percentage}% used
                </small>
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="panel">
        <h2>{selectedBudget ? "Edit budget" : "Create budget"}</h2>
        {error && <p className="error-message">{error}</p>}
        <form className="trip-form" onSubmit={saveBudget}>
          <label>
            Trip (optional)
            <select value={formValues.trip_id} onChange={(event) => updateField("trip_id", event.target.value)}>
              <option value="">All trips</option>
              {trips.map((trip) => (
                <option key={trip.id} value={trip.id}>
                  {trip.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            Category (optional)
            <select
              value={formValues.category_id}
              onChange={(event) => updateField("category_id", event.target.value)}
            >
              <option value="">All categories</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </label>
          <div className="two-column">
            <label>
              Budget amount
              <input
                required
                min="0.01"
                step="0.01"
                type="number"
                value={formValues.amount}
                onChange={(event) => updateField("amount", event.target.value)}
              />
            </label>
            <label>
              Currency
              <input
                required
                maxLength={3}
                value={formValues.currency}
                onChange={(event) => updateField("currency", event.target.value)}
              />
            </label>
          </div>
          <p className="form-note">Spending is calculated from expenses in the same currency.</p>
          <div className="actions">
            <button className="primary-button" disabled={isSaving} type="submit">
              {isSaving ? "Saving..." : selectedBudget ? "Save changes" : "Create budget"}
            </button>
            {selectedBudget && (
              <button className="danger-button" type="button" onClick={deleteSelectedBudget}>
                Delete budget
              </button>
            )}
          </div>
        </form>
      </div>
    </section>
  );
}
