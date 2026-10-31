import type { User } from "../types/auth";

type ProfilePanelProps = {
  user: User;
  onLogout: () => void;
};

export function ProfilePanel({ user, onLogout }: ProfilePanelProps) {
  return (
    <section className="panel profile-panel">
      <h2>Profile</h2>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Role:</strong> {user.role}</p>
      <p><strong>Member since:</strong> {new Date(user.created_at).toLocaleDateString()}</p>
      <button className="danger-button" type="button" onClick={onLogout}>
        Log out
      </button>
    </section>
  );
}
