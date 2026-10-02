export type EraKey = "atelier" | "memphis" | "brutalist";

export type Principle = {
  key: string;
  name: string;
  shape: string;
  eyebrow: string;
  blurb: string;
  bestFit: string;
  statement: string;
  status: string;
  accent: string;
  className: string;
};

export const eras: {
  key: EraKey;
  name: string;
  mood: string;
  descriptor: string;
}[] = [
  {
    key: "atelier",
    name: "Atelier",
    mood: "Warm and restrained",
    descriptor: "Warm light, soft surfaces, and restrained color create a calm composition.",
  },
  {
    key: "memphis",
    name: "Memphis",
    mood: "Playful signal burst",
    descriptor: "Playful shapes and vivid color give the same composition a more energetic character.",
  },
  {
    key: "brutalist",
    name: "Cyber-Brutalist",
    mood: "Stark and geometric",
    descriptor: "Sharper contrast, colder light, and hard edges create a stark geometric composition.",
  },
];

export const principles = [
  {key: "balance", name: "Balance", shape: "Weight · Equilibrium", accent: "var(--color-aura)"},
  {key: "contrast", name: "Contrast", shape: "Light · Hierarchy", accent: "var(--color-spark)"},
  {key: "rhythm", name: "Rhythm", shape: "Repetition · Cadence", accent: "#8de8ff"},
  {key: "unity", name: "Unity", shape: "Connection · Coherence", accent: "#f2d8b4"},
];
