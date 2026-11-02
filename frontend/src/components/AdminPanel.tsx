import { FormEvent, useEffect, useState } from "react";

import { adminApi } from "../services/admin";
import type { AdminUser, AdminUserFormValues } from "../types/admin";
import type { User } from "../types/auth";

const emptyForm: AdminUserFormValues = {
  email: "",
  password: "",
  role: "user",
};

type AdminPanelProps = {
  currentUser: User;
};

function formValuesFromUser(user: AdminUser): AdminUserFormValues {
  return { email: user.email, password: "", role: user.role };
}

export function AdminPanel({ currentUser }: AdminPanelProps) {
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [selectedUser, setSelectedUser] = useState<AdminUser | null>(null);
  const [formValues, setFormValues] = useState<AdminUserFormValues>(emptyForm);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  async function loadUsers() {
    setIsLoading(true);
    try {
      setUsers(await adminApi.list());
      setError("");
    } catch {
      setError("Could not load users. Administrator access is required.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadUsers();
  }, []);

  function startNewUser() {
    setSelectedUser(null);
    setFormValues(emptyForm);
    setError("");
  }

  function selectUser(user: AdminUser) {
    if (user.id === currentUser.id) {
      setError("Your own account cannot be changed from administrator controls.");
      return;
    }
    setSelectedUser(user);
    setFormValues(formValuesFromUser(user));
    setError("");
  }

  function updateField(field: keyof AdminUserFormValues, value: string) {
    setFormValues((currentValues) => ({ ...currentValues, [field]: value }));
  }

  async function saveUser(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selectedUser && formValues.password.length < 8) {
      setError("A new user needs a password with at least 8 characters.");
      return;
    }
    if (selectedUser && formValues.password && formValues.password.length < 8) {
      setError("A replacement password needs at least 8 characters.");
      return;
    }

    setIsSaving(true);
    try {
      const savedUser = selectedUser
        ? await adminApi.update(selectedUser.id, formValues)
        : await adminApi.create(formValues);
      setSelectedUser(savedUser);
      setFormValues(formValuesFromUser(savedUser));
      await loadUsers();
    } catch {
      setError("Could not save the user. Check the email, role, and password.");
    } finally {
      setIsSaving(false);
    }
  }

  async function deleteSelectedUser() {
    if (!selectedUser || !window.confirm(`Delete ${selectedUser.email}?`)) {
      return;
    }
    try {
      await adminApi.remove(selectedUser.id);
      startNewUser();
      await loadUsers();
    } catch {
      setError("Could not delete the user.");
    }
  }

  return (
    <section className="admin-layout">
      <div className="panel">
        <div className="actions">
          <h2>Users</h2>
          <button className="secondary-button" type="button" onClick={startNewUser}>
            New user
          </button>
        </div>
        {isLoading ? (
          <p>Loading users...</p>
        ) : users.length === 0 ? (
          <p>No users found.</p>
        ) : (
          <div className="user-list">
            {users.map((user) => (
              <button
                className={`user-row ${selectedUser?.id === user.id ? "selected" : ""}`}
                disabled={user.id === currentUser.id}
                key={user.id}
                type="button"
                onClick={() => selectUser(user)}
              >
                <strong>{user.email}</strong>
                <small>{user.role} - joined {new Date(user.created_at).toLocaleDateString()}</small>
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="panel">
        <h2>{selectedUser ? "Edit user" : "Create user"}</h2>
        {error && <p className="error-message">{error}</p>}
        <form className="trip-form" onSubmit={saveUser}>
          <label>
            Email
            <input
              required
              type="email"
              value={formValues.email}
              onChange={(event) => updateField("email", event.target.value)}
            />
          </label>
          <label>
            {selectedUser ? "New password (optional)" : "Password"}
            <input
              required={!selectedUser}
              minLength={8}
              type="password"
              value={formValues.password}
              onChange={(event) => updateField("password", event.target.value)}
            />
          </label>
          <label>
            Role
            <select value={formValues.role} onChange={(event) => updateField("role", event.target.value)}>
              <option value="user">User</option>
              <option value="admin">Administrator</option>
            </select>
          </label>
          <div className="actions">
            <button className="primary-button" disabled={isSaving} type="submit">
              {isSaving ? "Saving..." : selectedUser ? "Save user" : "Create user"}
            </button>
            {selectedUser && (
              <button className="danger-button" type="button" onClick={deleteSelectedUser}>
                Delete user
              </button>
            )}
          </div>
        </form>
      </div>
    </section>
  );
}
