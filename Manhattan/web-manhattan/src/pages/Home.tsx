import { Shield, CheckCircle, Lock, Zap } from "lucide-react";
import { Link } from "react-router-dom";
import DeviceCard from "@/components/DeviceCard";
import ComparisonTable from "@/components/ComparisonTable";
import ReferencesSidebar from "@/components/ReferencesSidebar";

const Home = () => {
  const devices = [
    {
      icon: "🔒",
      title: "Self-Encrypting Drives (SEDs)",
      method: "Cryptographic Erasure",
      nist: "SP 800-88: Purge",
      description: "Crypto-shredding via MEK destruction",
      features: [
        "Fastest, most secure method",
        "No data overwrite needed",
        "Instant completion"
      ]
    },
    {
      icon: "💾",
      title: "SATA SSDs (Non-SED)",
      method: "ATA Secure Erase (Enhanced)",
      nist: "SP 800-88: Purge",
      description: "Firmware-level command execution",
      features: [
        "Cleans hidden areas",
        "Faster than DBAN",
        "No SSD wear"
      ]
    },
    {
      icon: "⚡",
      title: "NVMe SSDs",
      method: "NVMe Sanitize",
      nist: "SP 800-88: Purge",
      description: "Controller-level sanitization",
      features: [
        "Targets all user/hidden data",
        "Firmware-level operation",
        "Fast completion"
      ]
    },
    {
      icon: "🖴",
      title: "Traditional HDDs",
      method: "ATA Secure Erase",
      nist: "SP 800-88: Purge",
      description: "Firmware-level overwrite",
      features: [
        "Cleans remapped sectors",
        "Faster than software overwrite",
        "Complete sanitization"
      ]
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="hero-gradient rounded-b-[3rem] text-white py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-extrabold mb-6 leading-tight">
            Secure Your Digital Legacy.<br />Erase Data, Empower Recycling.
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-white/90 leading-relaxed">
            Factory resets and file deletions are not enough. Get provable, NIST-compliant data sanitization with cryptographically verifiable certificates.
          </p>
          <Link to="/downloads">
            <button className="bg-white text-primary px-8 py-4 rounded-xl font-bold text-lg hover:scale-105 transition-transform shadow-2xl">
              Download Now
            </button>
          </Link>
        </div>
      </section>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Main Content */}
          <div className="flex-1 space-y-12">
            {/* The Problem Section */}
            <section className="section-card">
              <div className="flex items-start gap-4 mb-4">
                <Shield className="w-8 h-8 text-accent flex-shrink-0 mt-1" />
                <div>
                  <h2 className="text-3xl font-bold mb-4 text-foreground">The Problem</h2>
                  <div className="space-y-4 text-muted-foreground leading-relaxed">
                    <p>
                      <strong className="text-foreground">Simple factory resets and file deletions are insufficient.</strong> Studies show that data from "wiped" devices can be recovered easily, exposing sensitive personal information, credentials, and private files.
                    </p>
                    <p>
                      Fear of data leakage causes people to hoard old devices instead of recycling them, contributing to the growing e-waste crisis. This creates environmental damage and economic waste.
                    </p>
                    <p>
                      Traditional tools like DBAN are obsolete for modern SSDs, failing to reach hidden over-provisioned areas where data persists even after conventional wiping.
                    </p>
                  </div>
                </div>
              </div>
            </section>

            {/* Our Solution Section */}
            <section className="section-card">
              <div className="flex items-start gap-4 mb-4">
                <CheckCircle className="w-8 h-8 text-accent flex-shrink-0 mt-1" />
                <div>
                  <h2 className="text-3xl font-bold mb-6 text-foreground">Our Solution</h2>
                  <div className="space-y-6">
                    <p className="text-muted-foreground leading-relaxed">
                      The Manhattan Project provides <strong className="text-foreground">NIST SP 800-88 compliant data sanitization</strong> that's provably secure. Our solution uses device-specific, firmware-level techniques to ensure complete data erasure.
                    </p>

                    <div className="grid md:grid-cols-3 gap-6 my-8">
                      <div className="text-center p-6 rounded-xl bg-muted/50 border border-border">
                        <div className="w-12 h-12 bg-accent/20 text-accent rounded-full flex items-center justify-center mx-auto mb-3 font-bold text-xl">
                          1
                        </div>
                        <h3 className="font-bold mb-2 text-foreground">Download Tool</h3>
                        <p className="text-sm text-muted-foreground">Create bootable USB drive</p>
                      </div>
                      <div className="text-center p-6 rounded-xl bg-muted/50 border border-border">
                        <div className="w-12 h-12 bg-accent/20 text-accent rounded-full flex items-center justify-center mx-auto mb-3 font-bold text-xl">
                          2
                        </div>
                        <h3 className="font-bold mb-2 text-foreground">Boot Computer</h3>
                        <p className="text-sm text-muted-foreground">Start from USB drive</p>
                      </div>
                      <div className="text-center p-6 rounded-xl bg-muted/50 border border-border">
                        <div className="w-12 h-12 bg-accent/20 text-accent rounded-full flex items-center justify-center mx-auto mb-3 font-bold text-xl">
                          3
                        </div>
                        <h3 className="font-bold mb-2 text-foreground">One-Click Wipe</h3>
                        <p className="text-sm text-muted-foreground">Get verifiable certificate</p>
                      </div>
                    </div>

                    <div className="bg-accent/10 border-l-4 border-accent p-6 rounded-r-xl">
                      <div className="flex items-start gap-3">
                        <Lock className="w-6 h-6 text-accent flex-shrink-0 mt-0.5" />
                        <div>
                          <h4 className="font-bold text-foreground mb-2">Cryptographic Certificate of Sanitization</h4>
                          <p className="text-sm text-muted-foreground">
                            Every wipe generates a blockchain-backed verifiable credential proving data destruction, giving you peace of mind for recycling or resale.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* Technology Section */}
            <section className="section-card">
              <div className="flex items-start gap-4 mb-6">
                <Zap className="w-8 h-8 text-accent flex-shrink-0 mt-1" />
                <div className="flex-1">
                  <h2 className="text-3xl font-bold mb-6 text-foreground">The Technology: In-Depth</h2>

                  <div className="mb-8">
                    <h3 className="text-xl font-bold mb-4 text-foreground">Why Old Methods Are Obsolete</h3>
                    <p className="text-muted-foreground leading-relaxed mb-4">
                      Tools like DBAN were designed for HDDs and perform multiple overwrite passes, which are ineffective and harmful for SSDs. Modern solid-state drives have:
                    </p>
                    <ul className="space-y-2 text-muted-foreground ml-6">
                      <li className="flex items-start">
                        <span className="text-accent mr-2">•</span>
                        <span><strong className="text-foreground">Over-provisioned space</strong> - hidden areas inaccessible to OS-level tools</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-accent mr-2">•</span>
                        <span><strong className="text-foreground">Wear leveling</strong> - data scattered across physical locations</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-accent mr-2">•</span>
                        <span><strong className="text-foreground">Firmware-level management</strong> - requiring direct controller commands</span>
                      </li>
                    </ul>
                  </div>

                  <h3 className="text-xl font-bold mb-6 text-foreground">Device-Specific Solutions</h3>
                  <div className="grid md:grid-cols-2 gap-6 mb-8">
                    {devices.map((device, index) => (
                      <DeviceCard key={index} {...device} />
                    ))}
                  </div>

                  <h3 className="text-xl font-bold mb-4 text-foreground">Method Comparison</h3>
                  <ComparisonTable />
                </div>
              </div>
            </section>
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

export default Home;
