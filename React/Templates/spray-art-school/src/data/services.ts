export interface Service {
  id: string;
  name: string;
  description: string;
  bullets: string[];
  schedule: string;
  rotate: number;
}

export const services: Service[] = [
  {
    id: "svc-basics",
    name: "Basics",
    description:
      "Composition, technique, and materials. Your first steps on the street, built for people who've never held a can.",
    bullets: ["Composition fundamentals", "Cap control & line work", "Choosing your materials", "Finding your style"],
    schedule: "Mon / Wed · 6–8pm",
    rotate: -2,
  },
  {
    id: "svc-sketching",
    name: "Sketching",
    description: "Fast concepts on paper before they hit a wall. Build a visual language you can repeat under pressure.",
    bullets: ["Thumbnail speed sketching", "Character construction", "Value and shadow", "Translating sketch to scale"],
    schedule: "Tue / Thu · 7–9pm",
    rotate: 2,
  },
  {
    id: "svc-muralism",
    name: "Muralism",
    description: "Working at scale, on real walls, with real permission problems. Planning, projection, and crews.",
    bullets: ["Wall prep & primer", "Scaling a sketch", "Working in a crew", "Permits & community"],
    schedule: "Sat · 10am–2pm",
    rotate: -1,
  },
  {
    id: "svc-stencils",
    name: "Stencils",
    description: "Cut, layer, repeat. Precision work for people who like their lines clean and their message loud.",
    bullets: ["Multi-layer registration", "Material choice for cuts", "Repeatable editions", "Street application"],
    schedule: "Fri · 6–8pm",
    rotate: 3,
  },
  {
    id: "svc-freedom",
    name: "Freedom",
    description: "No brief. Open studio time with critique from working artists once a week.",
    bullets: ["Open studio access", "Weekly group critique", "Portfolio building", "Show prep"],
    schedule: "Sun · anytime",
    rotate: -2,
  },
];
