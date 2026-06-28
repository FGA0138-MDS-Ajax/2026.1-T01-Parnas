import { createContext, useCallback, useMemo, useState } from 'react';

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

  const login = useCallback((newToken, { preservarEmpresa = false } = {}) => {
    if (!preservarEmpresa) {
      localStorage.removeItem('empresaAtiva');
    }
    localStorage.setItem('token', newToken);
    setToken(newToken);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    localStorage.removeItem('empresaAtiva');
    setToken(null);
  }, []);

  const value = useMemo(
    () => ({ token, login, logout, isAuthenticated: !!token }),
    [token, login, logout],
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
