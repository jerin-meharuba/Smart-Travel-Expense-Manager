export type CurrencyAmount = {
  currency: string;
  amount: string;
};

export type DashboardSummary = {
  total_trips: number;
  active_trips: number;
  total_expenses_by_currency: CurrencyAmount[];
  remaining_budgets_by_currency: CurrencyAmount[];
};

export type CategorySpending = {
  category_id: number;
  category_name: string;
  currency: string;
  amount: string;
};

export type TripSpending = {
  trip_id: number;
  trip_name: string;
  currency: string;
  amount: string;
};

export type SpendingTrend = {
  period: string;
  currency: string;
  amount: string;
};

export type BudgetComparison = {
  budget_id: number;
  trip_id: number | null;
  category_id: number | null;
  amount: string;
  currency: string;
  actual_spending: string;
  remaining_amount: string;
  usage_percentage: string;
  is_overspent: boolean;
};

export type DashboardFilters = {
  trip_id: string;
  category_id: string;
  start_date: string;
  end_date: string;
  period: "daily" | "monthly";
};
