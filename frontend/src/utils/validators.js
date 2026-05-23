import { isCNPJ } from 'brazilian-values';

export const validateCNPJ = (cnpj) => {
  if (!cnpj) return false;
  const digitosPuros = String(cnpj).replace(/\D/g, '');

  return isCNPJ(digitosPuros);
};