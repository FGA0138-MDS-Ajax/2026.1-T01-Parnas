import { useEffect } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";
import useAuth from "./hooks/useAuth";
import api from "./services/api";
import Login from "./pages/Login/Login";
import CadastroEmpresa from "./pages/CadastroEmpresa/CadastroEmpresa";
import { EsqueciSenha } from "./pages/EsqueciSenha/EsqueciSenha";
import { RedefinirSenha } from "./pages/RedefinirSenha/RedefinirSenha";
import Categorias from "./pages/Categorias/Categorias";
import Register from "./pages/Register/Register";
import LayoutBase from "./components/Layout/LayoutBase";
import Dashboard from "./pages/Dashboard/Dashboard";
import Transacoes from "./pages/Transacoes/Transacoes";
import Configuracoes from "./pages/Configuracoes/Configuracoes";
import Documentos from "./pages/Documentos/Documentos";
import Contas from './pages/Contas/Contas';
import EditarPerfil from "./pages/EditarPerfil/EditarPerfil";

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

const AxiosInterceptorWrapper = ({ children }) => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  useEffect(() => {
    const interceptor = api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          console.warn(
            "Sessão inválida ou conta desativada detectada pelo interceptor.",
          );

          logout();
          localStorage.removeItem("credifab_empresas_reais");
          localStorage.removeItem("idEmpresaSimulado");

          // Redireciona de forma limpa para a tela de login
          navigate("/login", { replace: true });
        }
        return Promise.reject(error);
      },
    );
    return () => api.interceptors.response.eject(interceptor);
  }, [navigate, logout]);

  return children;
};

export const AppRoutes = () => {
  return (
    <BrowserRouter>
      <AxiosInterceptorWrapper>
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
            <Route path="/configuracoes" element={<Configuracoes />} />
            <Route path="/contas" element={<Contas />} />
            <Route path="/documentos" element={<Documentos />} />
            <Route path="/editar-perfil" element={<EditarPerfil />} />
          </Route>
        </Routes>
      </AxiosInterceptorWrapper>
    </BrowserRouter>
  );
};
