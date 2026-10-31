import api, { clearAccessToken, saveAccessToken } from "./api";
import type { LoginResponse, User } from "../types/auth";

export const authApi = {
  async register(email: string, password: string): Promise<User> {
    const response = await api.post<User>("/auth/register", { email, password });
    return response.data;
  },

  async login(email: string, password: string): Promise<User> {
    const response = await api.post<LoginResponse>("/auth/login", { email, password });
    saveAccessToken(response.data.access_token);
    return response.data.user;
  },

  async me(): Promise<User> {
    const response = await api.get<User>("/auth/me");
    return response.data;
  },

  async logout(): Promise<void> {
    try {
      await api.post("/auth/logout");
    } finally {
      clearAccessToken();
    }
  },
};
