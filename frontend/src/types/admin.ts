export type AdminUser = {
  id: number;
  email: string;
  role: "user" | "admin";
  created_at: string;
};

export type AdminUserFormValues = {
  email: string;
  password: string;
  role: "user" | "admin";
};
