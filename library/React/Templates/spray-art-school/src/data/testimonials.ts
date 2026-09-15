export interface Testimonial {
  id: string;
  quote: string;
  name: string;
  course: string;
  rotate: number;
}

export const testimonials: Testimonial[] = [
  {
    id: "test-01",
    quote:
      "I came in knowing nothing about spray control. Six weeks later I did my first legal wall solo.",
    name: "Nadia R.",
    course: "Basics → Muralism",
    rotate: -2,
  },
  {
    id: "test-02",
    quote:
      "The critique nights are brutal in the best way. No one softens feedback here, and the work gets better fast.",
    name: "Theo K.",
    course: "Stencils",
    rotate: 2,
  },
  {
    id: "test-03",
    quote: "First art school that treated the street as the actual classroom instead of an afterthought.",
    name: "Priya D.",
    course: "Freedom",
    rotate: -1,
  },
];
