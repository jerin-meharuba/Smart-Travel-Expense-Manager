import type { Budget, BudgetFormValues } from "../types/budget";
import api from "./api";

function toPayload(values: BudgetFormValues, includeEmptyTargets = false) {
  return {
    ...(values.trip_id
      ? { trip_id: Number(values.trip_id) }
      : includeEmptyTargets
        ? { trip_id: null }
        : {}),
    ...(values.category_id
      ? { category_id: Number(values.category_id) }
      : includeEmptyTargets
        ? { category_id: null }
        : {}),
    amount: values.amount,
    currency: values.currency,
  };
}

export const budgetApi = {
  async list(): Promise<Budget[]> {
    const response = await api.get<Budget[]>("/budgets");
    return response.data;
  },

  async create(values: BudgetFormValues): Promise<Budget> {
    const response = await api.post<Budget>("/budgets", toPayload(values));
    return response.data;
  },

  async update(id: number, values: BudgetFormValues): Promise<Budget> {
    const response = await api.patch<Budget>(`/budgets/${id}`, toPayload(values, true));
    return response.data;
  },

  async remove(id: number): Promise<void> {
    await api.delete(`/budgets/${id}`);
  },
};
