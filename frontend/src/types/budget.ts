export type Budget = {
  id: number;
  trip_id: number | null;
  category_id: number | null;
  amount: string;
  currency: string;
  created_at: string;
  updated_at: string;
  actual_spending: string;
  remaining_amount: string;
  usage_percentage: string;
  is_overspent: boolean;
};

export type BudgetFormValues = {
  trip_id: string;
  category_id: string;
  amount: string;
  currency: string;
};
