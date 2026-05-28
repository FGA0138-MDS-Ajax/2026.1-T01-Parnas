import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import useAuth from './hooks/useAuth';
import Login from './pages/Login/Login';
import CadastroEmpresa from './pages/CadastroEmpresa/CadastroEmpresa';
import { EsqueciSenha } from './pages/EsqueciSenha/EsqueciSenha';
import { RedefinirSenha } from './pages/RedefinirSenha/RedefinirSenha';
import Dashboard from './pages/Dashboard/Dashboard';
import LayoutBase from './components/Layout/LayoutBase';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

export const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* ROTAS PÚBLICAS */}
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/recuperacao-senha" element={<EsqueciSenha />} />
        <Route path="/redefinir-senha" element={<RedefinirSenha />} />

        {/* ROTAS PRIVADAS */}
        <Route element={<ProtectedRoute><LayoutBase /></ProtectedRoute>}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/cadastro-empresa" element={<CadastroEmpresa />} />
          <Route path="/configuracoes" element={<div>[Mock] Tela de Configurações (Sua tarefa US08)</div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};