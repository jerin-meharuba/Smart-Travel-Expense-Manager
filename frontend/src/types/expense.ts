export type Category = {
  id: number;
  name: string;
};

export type Expense = {
  id: number;
  trip_id: number;
  category_id: number;
  amount_original: string;
  currency_original: string;
  expense_date: string;
  payment_method: string;
  created_at: string;
  updated_at: string;
};

export type ExpenseFormValues = {
  trip_id: string;
  category_id: string;
  amount_original: string;
  currency_original: string;
  expense_date: string;
  payment_method: string;
};

export type ExpenseListResponse = {
  items: Expense[];
  total: number;
  offset: number;
  limit: number;
};
