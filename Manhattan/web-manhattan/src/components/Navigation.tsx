import { Link, useLocation } from "react-router-dom";
import { Moon, Sun } from "lucide-react";
import { useEffect, useState } from "react";

const Navigation = () => {
  const location = useLocation();
  const [isDark, setIsDark] = useState(true);

  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    const prefersDark = savedTheme === "dark" || (!savedTheme && true);
    setIsDark(prefersDark);
    document.documentElement.classList.toggle("dark", prefersDark);
  }, []);

  const toggleTheme = () => {
    const newTheme = !isDark;
    setIsDark(newTheme);
    document.documentElement.classList.toggle("dark", newTheme);
    localStorage.setItem("theme", newTheme ? "dark" : "light");
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="sticky top-0 z-50 bg-card/95 backdrop-blur-sm border-b border-border shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link 
            to="/" 
            className="text-xl font-bold tracking-wider text-foreground hover:text-accent transition-colors"
          >
            THE MANHATTAN PROJECT
          </Link>

          <div className="flex items-center gap-6">
            <Link
              to="/"
              className={`font-medium transition-colors ${
                isActive("/")
                  ? "text-accent"
                  : "text-foreground hover:text-accent"
              }`}
            >
              Home
            </Link>
            <Link
              to="/downloads"
              className={`font-medium transition-colors ${
                isActive("/downloads")
                  ? "text-accent"
                  : "text-foreground hover:text-accent"
              }`}
            >
              Downloads
            </Link>
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-muted transition-colors"
              aria-label="Toggle theme"
            >
              {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
