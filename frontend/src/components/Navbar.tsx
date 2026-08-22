import { useState } from "react";
import { Menu, X } from "lucide-react";
import { NavLink } from "react-router-dom";
import { Logo } from "./Logo";
import { ThemeToggle } from "./ThemeToggle";

type NavbarProps = {
  theme: "light" | "dark";
  onToggleTheme: () => void;
};

export function Navbar({ theme, onToggleTheme }: NavbarProps) {
  const [open, setOpen] = useState(false);

  return (
    <header className="no-print sticky top-0 z-40 bg-white/55 backdrop-blur-xl dark:bg-[#0B1020]/70">
      <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
        <Logo compact />
        <div className="flex items-center gap-2">
          <ThemeToggle theme={theme} onToggle={onToggleTheme} />
          <NavLink
            to="/analyze"
            className="focus-ring btn-glossy hidden rounded-full px-4 py-2 text-sm font-semibold md:inline-flex"
          >
            Check resume
          </NavLink>
          <button
            type="button"
            className="focus-ring inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/80 md:hidden dark:bg-white/10"
            aria-expanded={open}
            aria-label="Open menu"
            onClick={() => setOpen((value) => !value)}
          >
            {open ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </button>
        </div>
      </div>
      {open && (
        <div className="px-4 pb-3 md:hidden">
          <NavLink
            to="/analyze"
            onClick={() => setOpen(false)}
            className="block rounded-2xl bg-white/80 px-4 py-3 text-sm font-semibold dark:bg-white/10"
          >
            Check resume
          </NavLink>
        </div>
      )}
    </header>
  );
}
