const PageHeader = ({ className, title, description, actionLabel, onAction }) => (
  <div className={className}>
    <div>
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
    {actionLabel && onAction && (
      <button className="btn-nova-transacao" onClick={onAction}>
        <span className="btn-icon">+</span>
        {actionLabel}
      </button>
    )}
  </div>
);

export default PageHeader;
