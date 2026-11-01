export type Trip = {
  id: number;
  name: string;
  destination: string;
  start_date: string;
  end_date: string;
  status: string;
  budget_amount: string | null;
  budget_currency: string | null;
  created_at: string;
  updated_at: string;
};

export type TripFormValues = {
  name: string;
  destination: string;
  start_date: string;
  end_date: string;
  status: string;
};

export type TripListResponse = {
  items: Trip[];
  total: number;
  offset: number;
  limit: number;
};
