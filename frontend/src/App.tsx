import { FormEvent, useEffect, useState } from "react";
import { AuthScreen } from "./components/AuthScreen";
import { ExpenseManager } from "./components/ExpenseManager";
import { ProfilePanel } from "./components/ProfilePanel";
import { authApi } from "./services/auth";
import { clearAccessToken, hasAccessToken } from "./services/api";
import type { User } from "./types/auth";
import type { Trip, TripFormValues } from "./types/trip";
import { tripApi } from "./services/trips";

const emptyForm: TripFormValues = {
  name: "",
  destination: "",
  start_date: "",
  end_date: "",
  status: "planned",
  budget_amount: "",
  budget_currency: "USD",
};

function formValuesFromTrip(trip: Trip): TripFormValues {
  return {
    name: trip.name,
    destination: trip.destination,
    start_date: trip.start_date,
    end_date: trip.end_date,
    status: trip.status,
    budget_amount: trip.budget_amount ?? "",
    budget_currency: trip.budget_currency ?? "USD",
  };
}

function App() {
  const [activeSection, setActiveSection] = useState<"trips" | "expenses" | "profile">("trips");
  const [currentUser, setCurrentUser] = useState<User | null | undefined>(undefined);
  const [trips, setTrips] = useState<Trip[]>([]);
  const [selectedTrip, setSelectedTrip] = useState<Trip | null>(null);
  const [formValues, setFormValues] = useState<TripFormValues>(emptyForm);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  async function loadTrips() {
    setIsLoading(true);
    try {
      const response = await tripApi.list();
      setTrips(response.items);
      setError("");
    } catch {
      setError("Could not load trips. Make sure the backend is running.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    async function restoreSession() {
      if (!hasAccessToken()) {
        setCurrentUser(null);
        return;
      }

      try {
        setCurrentUser(await authApi.me());
      } catch {
        clearAccessToken();
        setCurrentUser(null);
      }
    }

    void restoreSession();
  }, []);

  useEffect(() => {
    if (currentUser) {
      void loadTrips();
    }
  }, [currentUser]);

  function selectTrip(trip: Trip) {
    setSelectedTrip(trip);
    setFormValues(formValuesFromTrip(trip));
    setError("");
  }

  function startNewTrip() {
    setSelectedTrip(null);
    setFormValues(emptyForm);
    setError("");
  }

  async function saveTrip(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSaving(true);
    try {
      const savedTrip = selectedTrip
        ? await tripApi.update(selectedTrip.id, formValues)
        : await tripApi.create(formValues);

      setSelectedTrip(savedTrip);
      setFormValues(formValuesFromTrip(savedTrip));
      await loadTrips();
    } catch {
      setError("Could not save the trip. Check all required fields and dates.");
    } finally {
      setIsSaving(false);
    }
  }

  async function deleteSelectedTrip() {
    if (!selectedTrip || !window.confirm(`Delete ${selectedTrip.name}?`)) {
      return;
    }

    try {
      await tripApi.remove(selectedTrip.id);
      startNewTrip();
      await loadTrips();
    } catch {
      setError("Could not delete the trip.");
    }
  }

  function updateField(field: keyof TripFormValues, value: string) {
    setFormValues((currentValues) => ({ ...currentValues, [field]: value }));
  }

  async function logout() {
    try {
      await authApi.logout();
    } catch {
      // The token is removed locally even when it has already expired.
      clearAccessToken();
    } finally {
      setCurrentUser(null);
      setTrips([]);
      startNewTrip();
    }
  }

  if (currentUser === undefined) {
    return <main className="auth-shell">Loading account...</main>;
  }

  if (currentUser === null) {
    return <AuthScreen onAuthenticated={setCurrentUser} />;
  }

  return (
    <main className="app-shell">
      <header className="app-header">
        <h1>Smart Travel Expense Manager</h1>
        <p>Create trips and record their expenses.</p>
        <div className="section-tabs" role="tablist" aria-label="Application sections">
          <button
            className={activeSection === "trips" ? "tab-button active" : "tab-button"}
            type="button"
            onClick={() => setActiveSection("trips")}
          >
            Trips
          </button>
          <button
            className={activeSection === "expenses" ? "tab-button active" : "tab-button"}
            type="button"
            onClick={() => setActiveSection("expenses")}
          >
            Expenses
          </button>
          <button
            className={activeSection === "profile" ? "tab-button active" : "tab-button"}
            type="button"
            onClick={() => setActiveSection("profile")}
          >
            Profile
          </button>
        </div>
      </header>

      {error && <p className="error-message">{error}</p>}

      {activeSection === "profile" ? (
        <ProfilePanel user={currentUser} onLogout={() => void logout()} />
      ) : activeSection === "expenses" ? (
        <ExpenseManager />
      ) : (
        <section className="trip-layout">
        <div className="panel">
          <div className="actions">
            <h2>Trips</h2>
            <button className="secondary-button" type="button" onClick={startNewTrip}>
              New trip
            </button>
          </div>

          {isLoading ? (
            <p>Loading trips...</p>
          ) : trips.length === 0 ? (
            <p>No trips yet. Create your first trip.</p>
          ) : (
            <div className="trip-list">
              {trips.map((trip) => (
                <button
                  className={`trip-card ${selectedTrip?.id === trip.id ? "selected" : ""}`}
                  key={trip.id}
                  type="button"
                  onClick={() => selectTrip(trip)}
                >
                  <strong>{trip.name}</strong>
                  <p>{trip.destination}</p>
                  <small>
                    {trip.start_date} to {trip.end_date} - {trip.status}
                  </small>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="panel">
          <h2>{selectedTrip ? "Edit trip" : "Create trip"}</h2>
          <form className="trip-form" onSubmit={saveTrip}>
            <label>
              Trip name
              <input
                required
                value={formValues.name}
                onChange={(event) => updateField("name", event.target.value)}
              />
            </label>
            <label>
              Destination
              <input
                required
                value={formValues.destination}
                onChange={(event) => updateField("destination", event.target.value)}
              />
            </label>
            <div className="two-column">
              <label>
                Start date
                <input
                  required
                  type="date"
                  value={formValues.start_date}
                  onChange={(event) => updateField("start_date", event.target.value)}
                />
              </label>
              <label>
                End date
                <input
                  required
                  type="date"
                  value={formValues.end_date}
                  onChange={(event) => updateField("end_date", event.target.value)}
                />
              </label>
            </div>
            <div className="two-column">
              <label>
                Status
                <select
                  value={formValues.status}
                  onChange={(event) => updateField("status", event.target.value)}
                >
                  <option value="planned">Planned</option>
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                </select>
              </label>
              <label>
                Budget amount (optional)
                <input
                  min="0"
                  step="0.01"
                  type="number"
                  value={formValues.budget_amount}
                  onChange={(event) => updateField("budget_amount", event.target.value)}
                />
              </label>
            </div>
            <label>
              Budget currency
              <input
                maxLength={3}
                value={formValues.budget_currency}
                onChange={(event) => updateField("budget_currency", event.target.value)}
              />
            </label>
            <div className="actions">
              <button className="primary-button" disabled={isSaving} type="submit">
                {isSaving ? "Saving..." : selectedTrip ? "Save changes" : "Create trip"}
              </button>
              {selectedTrip && (
                <button className="danger-button" type="button" onClick={deleteSelectedTrip}>
                  Delete trip
                </button>
              )}
            </div>
          </form>
        </div>
        </section>
      )}
    </main>
  );
}

export default App;
