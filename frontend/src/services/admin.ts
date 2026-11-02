import type { AdminUser, AdminUserFormValues } from "../types/admin";
import api from "./api";

export const adminApi = {
  async list(): Promise<AdminUser[]> {
    const response = await api.get<AdminUser[]>("/admin/users");
    return response.data;
  },

  async create(values: AdminUserFormValues): Promise<AdminUser> {
    const response = await api.post<AdminUser>("/admin/users", values);
    return response.data;
  },

  async update(id: number, values: AdminUserFormValues): Promise<AdminUser> {
    const response = await api.patch<AdminUser>(`/admin/users/${id}`, {
      email: values.email,
      role: values.role,
      ...(values.password ? { password: values.password } : {}),
    });
    return response.data;
  },

  async remove(id: number): Promise<void> {
    await api.delete(`/admin/users/${id}`);
  },
};
