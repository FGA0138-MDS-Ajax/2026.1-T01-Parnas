import React, { createContext, useState, useContext } from 'react';

const EmpresaContext = createContext();

export const EmpresaProvider = ({ children }) => {
  const [idEmpresaLogada, setIdEmpresaLogada] = useState(null);

  return (
    <EmpresaContext.Provider value={{ idEmpresaLogada, setIdEmpresaLogada }}>
      {children}
    </EmpresaContext.Provider>
  );
};

export const useEmpresa = () => {
  const contexto = useContext(EmpresaContext);

  if (!contexto) {
    return {
      idEmpresaLogada: localStorage.getItem('idEmpresaSimulado') || null,
      setIdEmpresaLogada: (idIdentificador) => {
        localStorage.setItem('idEmpresaSimulado', idIdentificador);
      }
    };
  }

  return contexto;
};