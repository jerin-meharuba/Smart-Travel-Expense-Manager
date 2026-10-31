import axios from "axios";

import type { Category, Expense, ExpenseFormValues, ExpenseListResponse } from "../types/expense";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1",
  headers: { "Content-Type": "application/json" },
});

function toPayload(values: ExpenseFormValues) {
  return {
    trip_id: Number(values.trip_id),
    category_id: Number(values.category_id),
    amount_original: values.amount_original,
    currency_original: values.currency_original,
    expense_date: values.expense_date,
    payment_method: values.payment_method,
  };
}

export const expenseApi = {
  async list(): Promise<ExpenseListResponse> {
    const response = await api.get<ExpenseListResponse>("/expenses", {
      params: { offset: 0, limit: 100 },
    });
    return response.data;
  },

  async listCategories(): Promise<Category[]> {
    const response = await api.get<Category[]>("/categories");
    return response.data;
  },

  async create(values: ExpenseFormValues): Promise<Expense> {
    const response = await api.post<Expense>("/expenses", toPayload(values));
    return response.data;
  },

  async update(id: number, values: ExpenseFormValues): Promise<Expense> {
    const response = await api.patch<Expense>(`/expenses/${id}`, toPayload(values));
    return response.data;
  },

  async remove(id: number): Promise<void> {
    await api.delete(`/expenses/${id}`);
  },
};
