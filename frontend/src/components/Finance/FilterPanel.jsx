const FilterPanel = ({ children, onClear, onApply }) => (
  <div className="transacoes-filtros">
    <div className="filtros-grid">{children}</div>
    <div className="filtros-acoes">
      <button className="btn-limpar" onClick={onClear}>Limpar filtros</button>
      <button className="btn-aplicar" onClick={onApply}>Aplicar filtros</button>
    </div>
  </div>
);

export default FilterPanel;
