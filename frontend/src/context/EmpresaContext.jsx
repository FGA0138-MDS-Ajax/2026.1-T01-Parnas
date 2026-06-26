import React, { createContext, useState, useContext } from "react";

const EmpresaContext = createContext();
const USER_EMAIL_KEY = "auth_user_email";

const getEmpresaIdKey = () => {
  const email = (localStorage.getItem(USER_EMAIL_KEY) || "default")
    .trim()
    .toLowerCase();
  return `idEmpresaSimulado_${email}`;
};

export const EmpresaProvider = ({ children }) => {
  const [idEmpresaLogada, setIdEmpresaLogada] = useState(
    () => localStorage.getItem(getEmpresaIdKey()) || null,
  );

  return (
    <EmpresaContext.Provider
      value={{
        idEmpresaLogada,
        setIdEmpresaLogada: (idIdentificador) => {
          const key = getEmpresaIdKey();
          if (idIdentificador) {
            localStorage.setItem(key, String(idIdentificador));
          } else {
            localStorage.removeItem(key);
          }
          setIdEmpresaLogada(idIdentificador);
        },
      }}
    >
      {children}
    </EmpresaContext.Provider>
  );
};

export const useEmpresa = () => {
  const contexto = useContext(EmpresaContext);

  if (!contexto) {
    return {
      idEmpresaLogada: localStorage.getItem(getEmpresaIdKey()) || null,
      setIdEmpresaLogada: (idIdentificador) => {
        const key = getEmpresaIdKey();
        if (idIdentificador) {
          localStorage.setItem(key, String(idIdentificador));
        } else {
          localStorage.removeItem(key);
        }
      },
    };
  }

  return contexto;
};
