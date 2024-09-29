export interface Task {
  name: string;
  endpoint: string;
  title: string;
  completed: boolean;
}

export const tasks: Task[] = [
  {
    name: "text-analysis",
    endpoint: "text-analysis",
    title: "Analiza tekstu",
    completed: false,
  },
  {
    name: "distracting movements",
    endpoint: "distracting movements",
    title: "Rozpraszające ruchy",
    completed: false,
  },
  {
    name: "audio",
    endpoint: "audio",
    title: "Analiza Audio",
    completed: false,
  },
  {
    name: "target-group",
    endpoint: "target-group",
    title: "Analiza Grupy Docelowej",
    completed: false,
  },
  {
    name: "process-jargon",
    endpoint: "process-jargon",
    title: "Wyciąganie Żargonu",
    completed: false,
  },
  {
    name: "detect-foreign",
    endpoint: "detect-foreign",
    title: "Wykryj obcojęzyczne słowa",
    completed: false,
  },
  {
    name: "detect-interruptions",
    endpoint: "detect-interruptions",
    title: "Wykryj przerywniki w transkrypcji",
    completed: false,
  },
  {
    name: "fix-passive",
    endpoint: "fix-passive",
    title: "Wykrywanie i korekta strony biernej",
    completed: false,
  },
  {
    name: "fix-repetitions",
    endpoint: "fix-repetitions",
    title: "Wykrywanie i korekra powtórzeń",
    completed: false,
  },
  {
    name: "fix-topic-change",
    endpoint: "fix-topic-change",
    title: "Wykrycie i korekta zmiany tematu",
    completed: false,
  },
  {
    name: "detect-numbers",
    endpoint: "detect-numbers",
    title: "Wykrycie Liczb w tekście",
    completed: false,
  },
  {
    name: "generate-questions",
    endpoint: "generate-questions",
    title: "Zadaj 10 pytań do tekstu",
    completed: false,
  },
  {
    name: "fix-nonexistent",
    endpoint: "fix-nonexistent",
    title: "Wykrycie i korekta nieistniejących słów",
    completed: false,
  },
  {
    name: "validate-understanding",
    endpoint: "validate-understanding",
    title: "Walidacja co zrozumiał user z wypowiedzi",
    completed: false,
  },
  {
    name: "evaluate-structure",
    endpoint: "evaluate-structure",
    title: "Oceń wstęp, rozwinięcie i zakończenie",
    completed: false,
  },
];
