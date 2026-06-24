import { AppRoutes } from './routes';
import { AuthProvider } from './context/AuthContext';
import { EmpresaProvider } from './context/EmpresaContext';
import './global.css';

function App() {
  return (
    <AuthProvider>
      <EmpresaProvider>
        <AppRoutes />
      </EmpresaProvider>
    </AuthProvider>
  );
}

export default App;
