import { AppRoutes } from './routes';
import { AuthProvider } from './context/AuthContext';
import './global.css';

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;
