import { FormEvent, useState } from "react";

import { authApi } from "../services/auth";
import type { User } from "../types/auth";

type AuthScreenProps = {
  onAuthenticated: (user: User) => void;
};

export function AuthScreen({ onAuthenticated }: AuthScreenProps) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    try {
      if (mode === "register") {
        await authApi.register(email, password);
      }
      const user = await authApi.login(email, password);
      onAuthenticated(user);
    } catch {
      setError(mode === "login" ? "Could not log in with those credentials." : "Could not register this account.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-panel">
        <h1>Smart Travel Expense Manager</h1>
        <p>{mode === "login" ? "Log in to manage your trips." : "Create an account to get started."}</p>
        <div className="section-tabs" role="tablist" aria-label="Authentication options">
          <button
            className={mode === "login" ? "tab-button active" : "tab-button"}
            type="button"
            onClick={() => setMode("login")}
          >
            Log in
          </button>
          <button
            className={mode === "register" ? "tab-button active" : "tab-button"}
            type="button"
            onClick={() => setMode("register")}
          >
            Register
          </button>
        </div>
        {error && <p className="error-message">{error}</p>}
        <form className="trip-form" onSubmit={submit}>
          <label>
            Email
            <input
              required
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
            />
          </label>
          <label>
            Password
            <input
              required
              minLength={8}
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
          </label>
          <button className="primary-button" disabled={isSubmitting} type="submit">
            {isSubmitting ? "Please wait..." : mode === "login" ? "Log in" : "Register"}
          </button>
        </form>
      </section>
    </main>
  );
}
