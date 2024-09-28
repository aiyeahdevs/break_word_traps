export interface Task {
  name: string;
  endpoint: string;
  title: string;
}

export const tasks: Task[] = [
  { name: "audio", endpoint: "audio", title: "Analiza Audio" },
  { name: "target-group", endpoint: "target-group", title: "Analiza Grupy Docelowej" },
  { name: "extract-jargon", endpoint: "extract-jargon", title: "Wyciąganie Żargonu" },
  { name: "simplify-jargon", endpoint: "simplify-jargon", title: "Zamiana Żargonu na zrozumiałe wyrażenia" },
  { name: "detect-foreign", endpoint: "detect-foreign", title: "Wykryj obcojęzyczne słowa" },
  { name: "detect-typos", endpoint: "detect-typos", title: "Wykryj przewyniki w transkrypcji" },
  { name: "fix-passive", endpoint: "fix-passive", title: "Wykrywanie i korekta strony biernej" },
  { name: "fix-repetitions", endpoint: "fix-repetitions", title: "Wykrywanie i korekra powtórzeń" },
  { name: "fix-topic-change", endpoint: "fix-topic-change", title: "Wykrycie i korekta zmiany tematu" },
  { name: "detect-numbers", endpoint: "detect-numbers", title: "Wykrycie Liczb w tekście" },
  { name: "generate-questions", endpoint: "generate-questions", title: "Zadaj 10 pytań do tekstu" },
  { name: "fix-nonexistent", endpoint: "fix-nonexistent", title: "Wykrycie i korekta nieistniejących słów" },
  { name: "validate-understanding", endpoint: "validate-understanding", title: "Walidacja co zrozumiał user z wypowiedzi" },
  { name: "evaluate-structure", endpoint: "evaluate-structure", title: "Oceń wstęp, rozwinięcie i zakończenie" },
  { name: "assess-target-group", endpoint: "assess-target-group", title: "Oceń grupę docelową" },
];
