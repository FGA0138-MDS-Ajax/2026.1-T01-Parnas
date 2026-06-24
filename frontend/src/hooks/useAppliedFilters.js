import { useState } from 'react';

const useAppliedFilters = (initialFilters) => {
  const [filtros, setFiltros] = useState(initialFilters);
  const [filtrosAplicados, setFiltrosAplicados] = useState(initialFilters);

  const handleFiltroChange = (e) => {
    const { name, value } = e.target;
    setFiltros((prev) => ({ ...prev, [name]: value }));
  };

  const aplicarFiltros = () => {
    setFiltrosAplicados(filtros);
  };

  const limparFiltros = () => {
    setFiltros(initialFilters);
    setFiltrosAplicados(initialFilters);
  };

  return {
    filtros,
    filtrosAplicados,
    handleFiltroChange,
    aplicarFiltros,
    limparFiltros,
  };
};

export default useAppliedFilters;
