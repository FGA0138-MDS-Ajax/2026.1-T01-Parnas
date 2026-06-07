const getToken = () => localStorage.getItem('token');

export const listarSimulacoes = async (empresaId) => {
  const response = await fetch(`/api/simulations?company_id=${empresaId}`, {
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : [];
  if (!response.ok) throw new Error((data && data.erro) || 'Erro ao listar simulações.');
  return data;
};

export const salvarSimulacao = async (payload) => {
  const response = await fetch('/api/simulations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${getToken()}`,
    },
    body: JSON.stringify(payload),
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : {};
  if (!response.ok) throw new Error((data && data.erro) || 'Erro ao salvar simulação.');
  return data;
};

export const excluirSimulacao = async (id) => {
  const response = await fetch(`/api/simulations/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  if (!response.ok) {
    const text = await response.text();
    const data = text ? JSON.parse(text) : {};
    throw new Error((data && data.erro) || 'Erro ao excluir simulação.');
  }
};
