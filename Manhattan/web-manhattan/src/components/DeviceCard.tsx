interface DeviceCardProps {
  icon: string;
  title: string;
  method: string;
  nist: string;
  description: string;
  features: string[];
}

const DeviceCard = ({ icon, title, method, nist, description, features }: DeviceCardProps) => {
  return (
    <div className="device-card">
      <div className="text-4xl mb-4">{icon}</div>
      <h4 className="text-xl font-bold mb-2 text-foreground">{title}</h4>
      <div className="space-y-2 mb-4">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-accent">METHOD:</span>
          <span className="text-sm text-foreground">{method}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-accent">NIST:</span>
          <span className="text-sm text-foreground">{nist}</span>
        </div>
      </div>
      <p className="text-sm text-muted-foreground mb-4">{description}</p>
      <div className="border-t border-border pt-4">
        <p className="text-xs font-semibold text-accent mb-2">KEY FEATURES:</p>
        <ul className="space-y-1">
          {features.map((feature, index) => (
            <li key={index} className="text-sm text-muted-foreground flex items-start">
              <span className="text-accent mr-2">•</span>
              {feature}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default DeviceCard;
