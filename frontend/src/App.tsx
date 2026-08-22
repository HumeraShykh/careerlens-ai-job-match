import { useEffect, useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { Footer } from "./components/Footer";
import { Navbar } from "./components/Navbar";
import { loadTheme, persistTheme } from "./lib/storage";
import { AnalyzePage } from "./pages/AnalyzePage";
import { LandingPage } from "./pages/LandingPage";
import { ResultsPage } from "./pages/ResultsPage";

export default function App() {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  useEffect(() => {
    const initial = loadTheme();
    setTheme(initial);
    document.documentElement.classList.toggle("dark", initial === "dark");
  }, []);

  function toggleTheme() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    persistTheme(next);
    document.documentElement.classList.toggle("dark", next === "dark");
  }

  return (
    <div className="min-h-svh text-ink-950 dark:text-slate-100">
      <Navbar theme={theme} onToggleTheme={toggleTheme} />
      <main>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/analyze" element={<AnalyzePage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}
