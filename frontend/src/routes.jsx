import { BrowserRouter, Routes, Route } from 'react-router-dom';
import CadastroEmpresa from './pages/CadastroEmpresa/CadastroEmpresa';

export const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<div style={{ padding: '20px', color: 'white' }}><h1>Home temporária do CREDIFAB 🚀</h1><p>Vá para <a href="/cadastro-empresa">/cadastro-empresa</a> para ver a tela de cadastro de empresa.</p></div>} />
        <Route path="/cadastro-empresa" element={<CadastroEmpresa />} />
      </Routes>
    </BrowserRouter>
  );
};