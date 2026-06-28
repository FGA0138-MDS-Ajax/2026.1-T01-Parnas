import axios from 'axios';

const getHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem('token')}`,
});

export const fetchDashboard = async (companyId) => {
  const { data } = await axios.get('/api/dashboard', {
    headers: getHeaders(),
    params: { company_id: companyId },
  });
  return data;
};
