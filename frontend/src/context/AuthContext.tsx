"use client";

/**
 * Auth context - the single source of truth for "who is logged in."
 * Wraps the whole app (see layout.tsx) so any page/component can call
 * useAuth() to get the current user, token, and signup/login/logout
 * functions, without prop-drilling any of this manually.
 *
 * Token is persisted to localStorage so a page refresh doesn't log the
 * user out - this is a real browser app (not a Claude.ai artifact), so
 * localStorage is the correct, normal choice here.
 */
import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { api, ApiError } from "@/lib/api";

interface AuthUser {
  user_id: string;
  email: string;
}

interface AuthContextValue {
  user: AuthUser | null;
  token: string | null;
  loading: boolean;
  signup: (email: string, password: string) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

interface AuthResponse {
  user_id: string;
  email: string;
  access_token: string;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem("auraframe_token");
    const savedUserId = localStorage.getItem("auraframe_user_id");
    const savedEmail = localStorage.getItem("auraframe_email");

    if (savedToken && savedUserId && savedEmail) {
      setToken(savedToken);
      setUser({ user_id: savedUserId, email: savedEmail });
    }
    setLoading(false);
  }, []);

  function persistSession(data: AuthResponse) {
    localStorage.setItem("auraframe_token", data.access_token);
    localStorage.setItem("auraframe_user_id", data.user_id);
    localStorage.setItem("auraframe_email", data.email);
    setToken(data.access_token);
    setUser({ user_id: data.user_id, email: data.email });
  }

  async function signup(email: string, password: string) {
    const data = await api.post<AuthResponse>("/auth/signup", { email, password });
    persistSession(data);
  }

  async function login(email: string, password: string) {
    const data = await api.post<AuthResponse>("/auth/login", { email, password });
    persistSession(data);
  }

  function logout() {
    localStorage.removeItem("auraframe_token");
    localStorage.removeItem("auraframe_user_id");
    localStorage.removeItem("auraframe_email");
    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, signup, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}

export { ApiError };