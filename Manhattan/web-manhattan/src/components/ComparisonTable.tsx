const ComparisonTable = () => {
  const rows = [
    {
      device: "Self-Encrypting Drives (SEDs)",
      method: "Cryptographic Erasure",
      speed: "Instant",
      effectiveness: "Complete",
      nist: "Purge",
      proof: "Yes - VC Certificate"
    },
    {
      device: "SATA SSDs (Non-SED)",
      method: "ATA Secure Erase (Enhanced)",
      speed: "Minutes",
      effectiveness: "Complete",
      nist: "Purge",
      proof: "Yes - VC Certificate"
    },
    {
      device: "NVMe SSDs",
      method: "NVMe Sanitize",
      speed: "Minutes",
      effectiveness: "Complete",
      nist: "Purge",
      proof: "Yes - VC Certificate"
    },
    {
      device: "Traditional HDDs",
      method: "ATA Secure Erase",
      speed: "Hours",
      effectiveness: "Complete",
      nist: "Purge",
      proof: "Yes - VC Certificate"
    }
  ];

  return (
    <div className="overflow-x-auto rounded-2xl shadow-lg">
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-accent text-accent-foreground">
            <th className="text-left p-4 font-bold">Device Type</th>
            <th className="text-left p-4 font-bold">Wiping Method</th>
            <th className="text-left p-4 font-bold">Speed</th>
            <th className="text-left p-4 font-bold">Effectiveness</th>
            <th className="text-left p-4 font-bold">NIST Compliance</th>
            <th className="text-left p-4 font-bold">Proof of Erasure</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr
              key={index}
              className={`${
                index % 2 === 0 ? "bg-card" : "bg-muted/30"
              } hover:bg-muted/50 transition-colors`}
            >
              <td className="p-4 font-semibold text-foreground">{row.device}</td>
              <td className="p-4 text-muted-foreground">{row.method}</td>
              <td className="p-4 text-muted-foreground">{row.speed}</td>
              <td className="p-4 text-muted-foreground">{row.effectiveness}</td>
              <td className="p-4">
                <span className="px-2 py-1 bg-accent/20 text-accent rounded text-sm font-semibold">
                  {row.nist}
                </span>
              </td>
              <td className="p-4 text-accent font-semibold">{row.proof}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ComparisonTable;
