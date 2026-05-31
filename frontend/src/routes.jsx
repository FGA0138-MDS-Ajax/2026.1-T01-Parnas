import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import useAuth from './hooks/useAuth';
import Login from './pages/Login/Login';
import CadastroEmpresa from './pages/CadastroEmpresa/CadastroEmpresa';
import { EsqueciSenha } from './pages/EsqueciSenha/EsqueciSenha';
import { RedefinirSenha } from './pages/RedefinirSenha/RedefinirSenha';
<<<<<<< Updated upstream
=======
import Register from './pages/Register/Register';
import LayoutBase from './components/Layout/LayoutBase';
import Dashboard from './pages/Dashboard/Dashboard';
import Transacoes from './pages/Transacoes/Transacoes';
>>>>>>> Stashed changes

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

export const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
       
        <Route path="/login" element={<Login />} />
        <Route path="/esqueci-senha" element={<EsqueciSenha />} />
        <Route path="/redefinir-senha" element={<RedefinirSenha />} />
          
        <Route 
          path="/cadastro-empresa" 
          element={
            <ProtectedRoute>
              <CadastroEmpresa />
            </ProtectedRoute>
<<<<<<< Updated upstream
          } 
        />
=======
          }
        >
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/cadastro-empresa" element={<CadastroEmpresa />} />
          <Route path="/transacoes" element={<Transacoes />} />
        </Route>
>>>>>>> Stashed changes
      </Routes>
    </BrowserRouter>
  );
};