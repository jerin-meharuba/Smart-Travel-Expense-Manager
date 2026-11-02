import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { dashboardApi } from "../services/dashboard";
import { expenseApi } from "../services/expenses";
import { tripApi } from "../services/trips";
import type {
  BudgetComparison,
  CategorySpending,
  DashboardFilters,
  DashboardSummary,
  SpendingTrend,
  TripSpending,
} from "../types/dashboard";
import type { Category } from "../types/expense";
import type { Trip } from "../types/trip";

const emptyFilters: DashboardFilters = {
  trip_id: "",
  category_id: "",
  start_date: "",
  end_date: "",
  period: "monthly",
};

function currencyText(items: { currency: string; amount: string }[]) {
  return items.length === 0 ? "No data" : items.map((item) => `${item.amount} ${item.currency}`).join(" | ");
}

export function DashboardPanel() {
  const [filters, setFilters] = useState<DashboardFilters>(emptyFilters);
  const [trips, setTrips] = useState<Trip[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [byCategory, setByCategory] = useState<CategorySpending[]>([]);
  const [byTrip, setByTrip] = useState<TripSpending[]>([]);
  const [trends, setTrends] = useState<SpendingTrend[]>([]);
  const [comparisons, setComparisons] = useState<BudgetComparison[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadDashboard() {
    setIsLoading(true);
    try {
      const [summaryResponse, categoryResponse, tripResponse, trendResponse, comparisonResponse] = await Promise.all([
        dashboardApi.summary(filters),
        dashboardApi.spendingByCategory(filters),
        dashboardApi.spendingByTrip(filters),
        dashboardApi.spendingTrends(filters),
        dashboardApi.budgetComparison(filters),
      ]);
      setSummary(summaryResponse);
      setByCategory(categoryResponse);
      setByTrip(tripResponse);
      setTrends(trendResponse);
      setComparisons(comparisonResponse);
      setError("");
    } catch {
      setError("Could not load dashboard data. Check the filters and backend connection.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    async function loadFilterChoices() {
      try {
        const [tripResponse, categoryResponse] = await Promise.all([tripApi.list(), expenseApi.listCategories()]);
        setTrips(tripResponse.items);
        setCategories(categoryResponse);
      } catch {
        setError("Could not load dashboard filter choices.");
      }
    }
    void loadFilterChoices();
  }, []);

  useEffect(() => {
    void loadDashboard();
  }, [filters]);

  function updateFilter(field: keyof DashboardFilters, value: string) {
    setFilters((currentFilters) => ({ ...currentFilters, [field]: value }));
  }

  function clearFilters() {
    setFilters(emptyFilters);
  }

  const categoryChartData = byCategory.map((item) => ({
    label: `${item.category_name} (${item.currency})`,
    amount: Number(item.amount),
  }));
  const tripChartData = byTrip.map((item) => ({
    label: `${item.trip_name} (${item.currency})`,
    amount: Number(item.amount),
  }));
  const trendChartData = trends.map((item) => ({
    label: `${item.period} (${item.currency})`,
    amount: Number(item.amount),
  }));
  const isEmpty = !isLoading && byCategory.length === 0 && byTrip.length === 0 && comparisons.length === 0;

  return (
    <section className="dashboard-panel">
      <div className="dashboard-heading">
        <div>
          <h2>Dashboard</h2>
          <p>All totals use the original currency stored with each expense.</p>
        </div>
        <button className="secondary-button" type="button" onClick={clearFilters}>
          Clear filters
        </button>
      </div>

      <div className="dashboard-filters" aria-label="Dashboard filters">
        <label>
          Trip
          <select value={filters.trip_id} onChange={(event) => updateFilter("trip_id", event.target.value)}>
            <option value="">All trips</option>
            {trips.map((trip) => (
              <option key={trip.id} value={trip.id}>
                {trip.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Category
          <select value={filters.category_id} onChange={(event) => updateFilter("category_id", event.target.value)}>
            <option value="">All categories</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          From
          <input type="date" value={filters.start_date} onChange={(event) => updateFilter("start_date", event.target.value)} />
        </label>
        <label>
          To
          <input type="date" value={filters.end_date} onChange={(event) => updateFilter("end_date", event.target.value)} />
        </label>
        <label>
          Trend
          <select value={filters.period} onChange={(event) => updateFilter("period", event.target.value)}>
            <option value="monthly">Monthly</option>
            <option value="daily">Daily</option>
          </select>
        </label>
      </div>

      {error && <p className="error-message">{error}</p>}
      {isLoading ? (
        <p className="dashboard-state">Loading dashboard...</p>
      ) : isEmpty ? (
        <p className="dashboard-state">No dashboard data matches these filters.</p>
      ) : (
        <>
          <div className="metric-grid">
            <article className="metric-card">
              <span>Total trips</span>
              <strong>{summary?.total_trips ?? 0}</strong>
            </article>
            <article className="metric-card">
              <span>Active trips</span>
              <strong>{summary?.active_trips ?? 0}</strong>
            </article>
            <article className="metric-card">
              <span>Expense totals</span>
              <strong>{currencyText(summary?.total_expenses_by_currency ?? [])}</strong>
            </article>
            <article className="metric-card">
              <span>Budget remaining</span>
              <strong>{currencyText(summary?.remaining_budgets_by_currency ?? [])}</strong>
            </article>
          </div>

          <div className="chart-grid">
            <ChartCard title="Spending by category" hasData={categoryChartData.length > 0}>
              <BarChart data={categoryChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="label" hide />
                <YAxis />
                <Tooltip />
                <Bar dataKey="amount" fill="#2563eb" />
              </BarChart>
            </ChartCard>
            <ChartCard title="Spending by trip" hasData={tripChartData.length > 0}>
              <BarChart data={tripChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="label" hide />
                <YAxis />
                <Tooltip />
                <Bar dataKey="amount" fill="#0891b2" />
              </BarChart>
            </ChartCard>
            <ChartCard title={`${filters.period === "daily" ? "Daily" : "Monthly"} spending trend`} hasData={trendChartData.length > 0}>
              <LineChart data={trendChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="label" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="amount" stroke="#7c3aed" strokeWidth={2} />
              </LineChart>
            </ChartCard>
          </div>

          <section className="panel comparison-panel">
            <h3>Budget versus actual</h3>
            {comparisons.length === 0 ? (
              <p>No budgets match these filters.</p>
            ) : (
              <div className="comparison-list">
                {comparisons.map((comparison) => (
                  <div className="comparison-row" key={comparison.budget_id}>
                    <div>
                      <strong>{comparison.amount} {comparison.currency}</strong>
                      <p>Spent {comparison.actual_spending}; remaining {comparison.remaining_amount}</p>
                    </div>
                    <span className={comparison.is_overspent ? "budget-over" : "budget-ok"}>
                      {comparison.is_overspent ? "Overspent" : `${comparison.usage_percentage}% used`}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </section>
        </>
      )}
    </section>
  );
}

function ChartCard({ title, hasData, children }: { title: string; hasData: boolean; children: React.ReactNode }) {
  return (
    <section className="panel chart-panel">
      <h3>{title}</h3>
      {hasData ? <ResponsiveContainer width="100%" height={260}>{children}</ResponsiveContainer> : <p>No data for this chart.</p>}
    </section>
  );
}
