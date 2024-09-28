import React, { useState, useEffect } from "react";
import ApiKeyManager from "./components/ApiKeyManager";
import FileUploader from "./components/FileUploader";
import ResultDisplay from "./components/ResultDisplay";
import { tasks } from "./tasks";

const App: React.FC = () => {
  const [apiKey, setApiKey] = useState<string>("");
  const [showApiKeyManager, setShowApiKeyManager] = useState<boolean>(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [results, setResults] = useState<Record<string, any>>({});
  const [loadingTasks, setLoadingTasks] = useState<Record<string, boolean>>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const savedApiKey = localStorage.getItem("apiKey");
    if (savedApiKey) {
      setApiKey(savedApiKey);
    } else {
      setShowApiKeyManager(true);
    }
  }, []);

  const handleApiKeySave = (newApiKey: string) => {
    setApiKey(newApiKey);
    localStorage.setItem("apiKey", newApiKey);
    setShowApiKeyManager(false);
  };

  const handleJobStart = (newJobId: string) => {
    setJobId(newJobId);
    tasks.forEach((task) => {
      task.completed = false;
    });
    setLoadingTasks(
      tasks.reduce((acc, task) => ({ ...acc, [task.name]: true }), {})
    );
    setResults({});
  };

  const handleJobComplete = () => {
    setLoadingTasks({});
    setJobId(null);
  };

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "20px" }}>
      <h1>Analiza Plików Wideo</h1>
      {showApiKeyManager ? (
        <ApiKeyManager onSave={handleApiKeySave} />
      ) : (
        <>
          <div style={{ marginBottom: "20px" }}>
            API Key: {"*".repeat(apiKey.length)}
            <button
              onClick={() => setShowApiKeyManager(true)}
              style={{ marginLeft: "10px" }}
            >
              Zmień klucz API
            </button>
          </div>
          <FileUploader
            apiKey={apiKey}
            onJobStart={handleJobStart}
            onJobComplete={handleJobComplete}
            setResults={setResults}
            setLoadingTasks={setLoadingTasks}
            setError={setError}
          />
          {error && (
            <div style={{ color: "red", marginTop: "10px" }}>{error}</div>
          )}
          {Object.values(loadingTasks).some(Boolean) && (
            <div>Przetwarzanie... Proszę czekać.</div>
          )}
          {jobId && <div>ID zadania: {jobId}</div>}
          {tasks.map((task) => (
            <ResultDisplay
              key={task.name}
              task={task}
              result={results[task.name]}
              isLoading={loadingTasks[task.name]}
            />
          ))}
        </>
      )}
    </div>
  );
};

export default App;
