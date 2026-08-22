import type { Skill } from "../types";

type SkillChipsProps = {
  skills: Skill[];
  tone?: "matched" | "missing";
  empty: string;
};

export function SkillChips({ skills, tone = "matched", empty }: SkillChipsProps) {
  if (skills.length === 0) {
    return <p className="text-sm text-ink-500">{empty}</p>;
  }

  return (
    <ul className="flex flex-wrap gap-2">
      {skills.map((skill) => (
        <li
          key={`${skill.category}-${skill.name}`}
          className={`rounded-full px-3 py-1.5 text-sm font-medium ${
            tone === "matched"
              ? "bg-teal-500/15 text-teal-800 dark:text-teal-200"
              : "bg-rose-500/12 text-rose-700 dark:text-rose-200"
          }`}
        >
          {skill.name}
        </li>
      ))}
    </ul>
  );
}
