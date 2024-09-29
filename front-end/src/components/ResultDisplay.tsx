import React from "react";
import { Task } from "../tasks";

interface ResultsDisplayProps {
  task: Task;
  result: any;
  isLoading: boolean;
}

const ResultDisplay: React.FC<ResultsDisplayProps> = ({
  task,
  result,
  isLoading,
}) => {
  const resultsStyles: React.CSSProperties = {
    marginTop: "20px",
    padding: "15px",
    border: "1px solid #ddd",
    borderRadius: "4px",
    backgroundColor: "#f9f9f9",
  };

  return (
    <div style={resultsStyles}>
      <h4>{task.title}</h4>
      {isLoading ? (
        <p>Ładowanie...</p>
      ) : result ? (
        task.name === "audio" ? (
          <>
            <p>
              Procent zbyt głośnego dźwięku:{" "}
              {result.too_loud_percentage.toFixed(2)}%
            </p>
            <p>
              Procent zbyt cichego dźwięku:{" "}
              {result.too_quiet_percentage.toFixed(2)}%
            </p>
            <p>Średni poziom dB: {result.average_db.toFixed(2)} dB</p>
            <p>Maksymalny poziom dB: {result.max_db.toFixed(2)} dB</p>
            <p>Minimalny poziom dB: {result.min_db.toFixed(2)} dB</p>
          </>
        ) : (
          <pre style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
            {result}
          </pre>
        )
      ) : (
        <p>Brak wyników</p>
      )}
    </div>
  );
};

export default ResultDisplay;
