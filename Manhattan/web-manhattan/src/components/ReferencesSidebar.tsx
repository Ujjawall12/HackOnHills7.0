import { ExternalLink } from "lucide-react";

const references = [
  {
    title: "NIST SP 800-88 Rev. 1",
    subtitle: "Guidelines for Media Sanitization",
    url: "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r1.pdf"
  },
  {
    title: "UNEP E-Waste Report",
    subtitle: "2024",
    url: "https://www.unep.org/resources/report/global-e-waste-monitor-2024"
  },
  {
    title: "CPCB E-Waste Rules",
    subtitle: "2022",
    url: "https://cpcb.nic.in/e-waste/"
  },
  {
    title: "Stellar Data Recovery",
    subtitle: "Factory Reset Data Recovery",
    url: "https://www.stellarinfo.com/blog/recover-data-after-factory-reset/"
  },
  {
    title: "Cambridge Study",
    subtitle: "Android Data Recovery Research",
    url: "https://www.cl.cam.ac.uk/~rja14/Papers/fr_most17.pdf"
  },
  {
    title: "Blancco White Paper",
    subtitle: "SSD Data Erasure",
    url: "https://www.blancco.com/resources/ssd-overwriting-not-effective/"
  },
  {
    title: "Seagate Documentation",
    subtitle: "ATA Secure Erase",
    url: "https://www.seagate.com/support/kb/how-to-secure-erase-an-ssd-005805en/"
  },
  {
    title: "NVMe Sanitize",
    subtitle: "NVM Express Guide",
    url: "https://nvmexpress.org/resources/nvm-express-technology-features/sanitize/"
  },
  {
    title: "Hyperledger Fabric",
    subtitle: "Documentation",
    url: "https://hyperledger-fabric.readthedocs.io/"
  },
  {
    title: "W3C Verifiable Credentials",
    subtitle: "Data Model",
    url: "https://www.w3.org/TR/vc-data-model/"
  }
];

const ReferencesSidebar = () => {
  return (
    <aside className="lg:sticky lg:top-20 bg-card rounded-2xl shadow-lg p-6 h-fit">
      <h3 className="text-lg font-bold mb-4 text-foreground">References & Standards</h3>
      <div className="space-y-3">
        {references.map((ref, index) => (
          <a
            key={index}
            href={ref.url}
            target="_blank"
            rel="noopener noreferrer"
            className="block p-3 rounded-lg border border-border hover:border-accent hover:bg-muted/50 transition-all group"
          >
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-sm text-foreground group-hover:text-accent transition-colors truncate">
                  {ref.title}
                </p>
                <p className="text-xs text-muted-foreground mt-0.5">{ref.subtitle}</p>
              </div>
              <ExternalLink className="w-4 h-4 text-muted-foreground group-hover:text-accent transition-colors flex-shrink-0" />
            </div>
          </a>
        ))}
      </div>
    </aside>
  );
};

export default ReferencesSidebar;
