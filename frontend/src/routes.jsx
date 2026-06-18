import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import useAuth from './hooks/useAuth';
import Login from './pages/Login/Login';
import CadastroEmpresa from './pages/CadastroEmpresa/CadastroEmpresa';
import { EsqueciSenha } from './pages/EsqueciSenha/EsqueciSenha';
import { RedefinirSenha } from './pages/RedefinirSenha/RedefinirSenha';
import Categorias from './pages/Categorias/Categorias';
import Register from './pages/Register/Register';
import LayoutBase from './components/Layout/LayoutBase';
import Dashboard from './pages/Dashboard/Dashboard';
import Transacoes from './pages/Transacoes/Transacoes';
import Contas from './pages/Contas/Contas';
import Configuracoes from './pages/Configuracoes/Configuracoes';
import Documentos from "./pages/Documentos/Documentos";
import Simulacoes from './pages/Simulacoes/Simulacoes';
import Relatorios from './pages/Relatorios/Relatorios';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

export const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rotas Públicas */}
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/esqueci-senha" element={<EsqueciSenha />} />
        <Route path="/redefinir-senha" element={<RedefinirSenha />} />

        {/* Rotas Privadas */}
        <Route
          element={
            <ProtectedRoute>
              <LayoutBase />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/cadastro-empresa" element={<CadastroEmpresa />} />
          <Route path="/categorias" element={<Categorias />} />
          <Route path="/transacoes" element={<Transacoes />} />
          <Route path="/contas" element={<Contas />} />
          <Route path="/simulacoes" element={<Simulacoes />} />
          <Route path="/relatorios" element={<Relatorios />} />
          <Route path="/configuracoes" element={<Configuracoes />} />
          <Route path="/documentos" element={<Documentos />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};
