export interface Project {
  id: string;
  title: string;
  category: string;
  year: string;
  student: string;
  placeholderLabel: string;
  rotate: number;
}

export const projects: Project[] = [
  {
    id: "proj-01",
    title: "Concrete Bloom",
    category: "Mural",
    year: "2024",
    student: "Nadia R.",
    placeholderLabel: "MURAL / WALL 04",
    rotate: -3,
  },
  {
    id: "proj-02",
    title: "Static Dogs",
    category: "Stencil series",
    year: "2024",
    student: "Theo K.",
    placeholderLabel: "STENCIL SET",
    rotate: 2,
  },
  {
    id: "proj-03",
    title: "Loudmouth",
    category: "Character piece",
    year: "2023",
    student: "Priya D.",
    placeholderLabel: "CHARACTER STUDY",
    rotate: -2,
  },
  {
    id: "proj-04",
    title: "Rust Belt Letters",
    category: "Typography",
    year: "2024",
    student: "Marcus V.",
    placeholderLabel: "LETTERFORM PIECE",
    rotate: 3,
  },
  {
    id: "proj-05",
    title: "Night Shift",
    category: "Freehand",
    year: "2023",
    student: "Lena B.",
    placeholderLabel: "FREEHAND CAN WORK",
    rotate: -1,
  },
  {
    id: "proj-06",
    title: "Paper Riot",
    category: "Zine cover",
    year: "2024",
    student: "Sam O.",
    placeholderLabel: "ZINE COVER ART",
    rotate: 2,
  },
];
