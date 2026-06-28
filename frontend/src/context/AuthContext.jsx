import { createContext, useCallback, useMemo, useState } from 'react';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('token'));

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
