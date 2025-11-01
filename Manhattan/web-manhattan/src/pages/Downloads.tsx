import { Download } from "lucide-react";
import ReferencesSidebar from "@/components/ReferencesSidebar";

const Downloads = () => {
  const platforms = [
    { name: "Windows", icon: "🪟", disabled: true },
    { name: "macOS", icon: "🍎", disabled: true },
    { name: "Linux", icon: "🐧", disabled: true }
  ];

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Main Content */}
          <div className="flex-1">
            <h1 className="text-4xl font-bold mb-8 text-foreground">Downloads</h1>

            <div className="section-card max-w-2xl">
              <div className="flex items-start gap-4 mb-6">
                <Download className="w-8 h-8 text-accent flex-shrink-0 mt-1" />
                <div className="flex-1">
                  <h2 className="text-2xl font-bold mb-3 text-foreground">
                    Manhattan Project Media Creation Tool
                  </h2>
                  <p className="text-muted-foreground leading-relaxed mb-6">
                    Download our media creation tool to create a bootable USB drive for NIST SP 800-88 compliant secure data wiping. The tool will guide you through creating a bootable USB that can securely sanitize any computer.
                  </p>

                  <div className="space-y-4 mb-6">
                    <h3 className="font-semibold text-foreground">System Requirements:</h3>
                    <ul className="space-y-2 text-sm text-muted-foreground ml-6">
                      <li className="flex items-start">
                        <span className="text-accent mr-2">•</span>
                        <span>USB drive with at least 4GB capacity</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-accent mr-2">•</span>
                        <span>Administrator/root privileges on your computer</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-accent mr-2">•</span>
                        <span>Active internet connection for download</span>
                      </li>
                    </ul>
                  </div>

                  <div className="border-t border-border pt-6">
                    <h3 className="font-semibold text-foreground mb-4">Select Your Platform:</h3>
                    <div className="grid gap-3">
                      {platforms.map((platform) => (
                        <button
                          key={platform.name}
                          disabled={platform.disabled}
                          className={`flex items-center justify-between p-4 rounded-lg border-2 transition-all ${
                            platform.disabled
                              ? "border-border bg-muted/30 cursor-not-allowed opacity-60"
                              : "border-accent bg-accent/10 hover:bg-accent/20 hover:scale-102"
                          }`}
                        >
                          <div className="flex items-center gap-3">
                            <span className="text-3xl">{platform.icon}</span>
                            <span className="font-semibold text-foreground text-lg">
                              {platform.name}
                            </span>
                          </div>
                          <Download className={`w-5 h-5 ${platform.disabled ? "text-muted-foreground" : "text-accent"}`} />
                        </button>
                      ))}
                    </div>

                    <div className="mt-6 p-4 bg-muted/50 rounded-lg border border-border">
                      <p className="text-sm text-muted-foreground">
                        <strong className="text-foreground">Coming soon:</strong> Links are placeholders. The Manhattan Project Media Creation Tool is under active development. Sign up for updates to be notified when it's ready.
                      </p>
                    </div>
                  </div>

                  <div className="mt-8 p-6 bg-accent/10 border-l-4 border-accent rounded-r-xl">
                    <h4 className="font-bold text-foreground mb-3">What happens after download?</h4>
                    <ol className="space-y-3 text-sm text-muted-foreground">
                      <li className="flex items-start gap-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-accent text-accent-foreground rounded-full flex items-center justify-center text-xs font-bold">1</span>
                        <span>Run the downloaded tool on your current computer</span>
                      </li>
                      <li className="flex items-start gap-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-accent text-accent-foreground rounded-full flex items-center justify-center text-xs font-bold">2</span>
                        <span>Insert a USB drive and follow the creation wizard</span>
                      </li>
                      <li className="flex items-start gap-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-accent text-accent-foreground rounded-full flex items-center justify-center text-xs font-bold">3</span>
                        <span>Boot the target computer from the USB</span>
                      </li>
                      <li className="flex items-start gap-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-accent text-accent-foreground rounded-full flex items-center justify-center text-xs font-bold">4</span>
                        <span>Follow on-screen instructions to perform secure wipe</span>
                      </li>
                      <li className="flex items-start gap-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-accent text-accent-foreground rounded-full flex items-center justify-center text-xs font-bold">5</span>
                        <span>Receive your cryptographic certificate of sanitization</span>
                      </li>
                    </ol>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:w-80">
            <ReferencesSidebar />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Downloads;
