import type {
  BudgetComparison,
  CategorySpending,
  DashboardFilters,
  DashboardSummary,
  SpendingTrend,
  TripSpending,
} from "../types/dashboard";
import api from "./api";

function queryParams(filters: DashboardFilters) {
  return {
    ...(filters.trip_id ? { trip_id: Number(filters.trip_id) } : {}),
    ...(filters.category_id ? { category_id: Number(filters.category_id) } : {}),
    ...(filters.start_date ? { start_date: filters.start_date } : {}),
    ...(filters.end_date ? { end_date: filters.end_date } : {}),
  };
}

export const dashboardApi = {
  async summary(filters: DashboardFilters): Promise<DashboardSummary> {
    const response = await api.get<DashboardSummary>("/dashboard/summary", {
      params: queryParams(filters),
    });
    return response.data;
  },

  async spendingByCategory(filters: DashboardFilters): Promise<CategorySpending[]> {
    const response = await api.get<CategorySpending[]>("/dashboard/spending-by-category", {
      params: queryParams(filters),
    });
    return response.data;
  },

  async spendingByTrip(filters: DashboardFilters): Promise<TripSpending[]> {
    const response = await api.get<TripSpending[]>("/dashboard/spending-by-trip", {
      params: queryParams(filters),
    });
    return response.data;
  },

  async spendingTrends(filters: DashboardFilters): Promise<SpendingTrend[]> {
    const response = await api.get<SpendingTrend[]>("/dashboard/spending-trends", {
      params: { ...queryParams(filters), period: filters.period },
    });
    return response.data;
  },

  async budgetComparison(filters: DashboardFilters): Promise<BudgetComparison[]> {
    const response = await api.get<BudgetComparison[]>("/dashboard/budget-comparison", {
      params: queryParams(filters),
    });
    return response.data;
  },
};
