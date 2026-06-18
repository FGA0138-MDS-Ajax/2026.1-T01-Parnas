import axios from 'axios';

const getHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem('token')}`,
});

export const calcularComparacao = async (payload) => {
  const { data } = await axios.post('/api/comparacoes/calcular', payload, { headers: getHeaders() });
  return data;
};

export const salvarComparacao = async (payload) => {
  const { data } = await axios.post('/api/comparacoes/', payload, { headers: getHeaders() });
  return data;
};

export const listarComparacoes = async () => {
  const { data } = await axios.get('/api/comparacoes/', { headers: getHeaders() });
  return data;
};

export const deletarComparacao = async (id) => {
  const { data } = await axios.delete(`/api/comparacoes/${id}`, { headers: getHeaders() });
  return data;
};

export const exportarPDF = async (id) => {
  const response = await axios.get(`/api/comparacoes/${id}/exportar`, {
    headers: getHeaders(),
    responseType: 'blob',
  });
  const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = `comparativo_credito_${id}.pdf`;
  link.click();
  window.URL.revokeObjectURL(url);
};
