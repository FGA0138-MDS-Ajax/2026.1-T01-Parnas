import { createContext, useState } from "react";

export const AuthContext = createContext(null);

const USER_EMAIL_KEY = "auth_user_email";

const clearCompanyState = () => {
  const cachedKeys = Object.keys(localStorage).filter(
    (key) =>
      key.startsWith("credifab_empresas_") ||
      key.startsWith("empresa_ativa_") ||
      key === "empresa_ativa" ||
      key === "idEmpresaSimulado",
  );
  cachedKeys.forEach((key) => localStorage.removeItem(key));
};

const readStoredToken = () => {
  const directToken = localStorage.getItem("token");
  if (directToken) return directToken;

  const fallbackToken = localStorage.getItem("access_token");
  return fallbackToken || null;
};

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => readStoredToken());

  const login = (newToken, userEmail = null) => {
    clearCompanyState();
    if (userEmail) {
      localStorage.setItem(USER_EMAIL_KEY, userEmail);
    }
    localStorage.setItem("token", newToken);
    localStorage.setItem("access_token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    clearCompanyState();
    localStorage.removeItem(USER_EMAIL_KEY);
    localStorage.removeItem("token");
    localStorage.removeItem("access_token");
    setToken(null);
  };

  return (
    <AuthContext.Provider
      value={{ token, login, logout, isAuthenticated: !!token }}
    >
      {children}
    </AuthContext.Provider>
  );
};
