export type User = {
  id: number;
  email: string;
  role: string;
  created_at: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
  user: User;
};
