const SummaryCards = ({ items }) => (
  <div className="transacoes-totais">
    {items.map((item) => (
      <div className={`total-card ${item.className}`} key={item.label}>
        <span className="total-label">{item.label}</span>
        <span className="total-valor">{item.value}</span>
      </div>
    ))}
  </div>
);

export default SummaryCards;
