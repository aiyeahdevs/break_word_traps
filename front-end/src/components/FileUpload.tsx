import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";

interface JobResponse {
  job_id: string;
  message: string;
}

interface AnalysisResult {
  too_loud_percentage: number;
  too_quiet_percentage: number;
  average_db: number;
  max_db: number;
  min_db: number;
}

interface Task {
  name: string;
  endpoint: string;
  setResult: React.Dispatch<React.SetStateAction<any>>;
}

interface FileUploadProps {
  apiKey: string;
}

const FileUpload: React.FC<FileUploadProps> = ({ apiKey }) => {
  const pollInterval = 2000; // 2 seconds

  const [files, setFiles] = useState<File[]>([]);
  const [jobId, setJobId] = useState<string | null>(null);
  const [audioResults, setAudioResults] = useState<AnalysisResult | null>(null);
  const [textResults, setTargetGroupResult] = useState<any | null>(null);
  const [videoResults, setVideoResults] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const tasks: Task[] = [
    {
      name: "audio",
      endpoint: "audio",
      setResult: setAudioResults,
    },
    {
      name: "target-group",
      endpoint: "target-group",
      setResult: setTargetGroupResult,
    },
    // {
    //   name: 'video',
    //   endpoint: 'video',
    //   setResult: setVideoResults,
    // },
  ];

  const pollJobStatus = useCallback(
    async (jobId: string) => {
      const checkStatus = async () => {
        try {
          const results = await Promise.all(
            tasks.map(async (task) => {
              const response = await fetch(
                `http://localhost:8000/job-result/${jobId}/${task.endpoint}`
              );
              return { task, response };
            })
          );

          let allCompleted = true;
          results.forEach(({ task, response }) => {
            if (response.status === 200) {
              response.json().then((data) => task.setResult(data[task.name]));
            } else {
              allCompleted = false;
            }
          });

          if (!allCompleted) {
            setTimeout(checkStatus, pollInterval);
          } else {
            setIsLoading(false);
            setJobId(null);
          }
        } catch (e) {
          setError("Wystąpił błąd podczas sprawdzania statusu zadania.");
          console.error("Job status error:", e);
          setIsLoading(false);
          setJobId(null);
        }
      };

      checkStatus();
    },
    [tasks]
  );

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles((prevFiles) => [...prevFiles, ...acceptedFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive, fileRejections } =
    useDropzone({
      onDrop,
      accept: {
        "video/mp4": [".mp4"],
      },
    });

  const handleUpload = async () => {
    if (files.length === 0) return;

    setIsLoading(true);
    setError(null);
    //setResults(null);

    const formData = new FormData();
    formData.append("file", files[0]);

    try {
      const response = await fetch("http://localhost:8000/start-job/", {
        method: "POST",
        headers: {
          llmkey: apiKey,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: JobResponse = await response.json();
      setJobId(data.job_id);
      pollJobStatus(data.job_id);
    } catch (e) {
      setError("Wystąpił błąd podczas przesyłania pliku.");
      console.error("Upload error:", e);
    } finally {
      setIsLoading(false);
      setFiles([]);
    }
  };

  return (
    <div>
      <div {...getRootProps()} style={dropzoneStyles}>
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Upuść pliki MP4 tutaj ...</p>
        ) : (
          <p>
            Przeciągnij i upuść pliki MP4 tutaj lub kliknij, aby wybrać pliki
          </p>
        )}
      </div>
      {files.length > 0 && (
        <div>
          <h4>Wybrane pliki:</h4>
          <ul>
            {files.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </div>
      )}
      {fileRejections.length > 0 && (
        <div style={{ color: "red" }}>
          <h4>Odrzucone pliki:</h4>
          <ul>
            {fileRejections.map(({ file, errors }) => (
              <li key={file.name}>
                {file.name} - {errors.map((e) => e.message).join(", ")}
              </li>
            ))}
          </ul>
        </div>
      )}
      <button onClick={handleUpload} disabled={files.length === 0 || isLoading}>
        {isLoading ? "Wysyłanie..." : "Wyślij pliki"}
      </button>
      {error && <div style={{ color: "red", marginTop: "10px" }}>{error}</div>}
      {isLoading && <div>Przetwarzanie... Proszę czekać.</div>}
      {jobId && <div>ID zadania: {jobId}</div>}
      {tasks.map((task) => {
        const result =
          task.name === "audio"
            ? audioResults
            : task.name === "target-group"
            ? textResults
            : videoResults;
        if (!result) return null;

        return (
          <div key={task.name} style={resultsStyles}>
            <h4>
              Wyniki analizy{" "}
              {task.name === "audio"
                ? "audio"
                : task.name === "target-group"
                ? "tekstu"
                : "wideo"}
              :
            </h4>
            {task.name === "audio" && audioResults ? (
              <>
                <p>
                  Procent zbyt głośnego dźwięku:{" "}
                  {audioResults.too_loud_percentage.toFixed(2)}%
                </p>
                <p>
                  Procent zbyt cichego dźwięku:{" "}
                  {audioResults.too_quiet_percentage.toFixed(2)}%
                </p>
                <p>Średni poziom dB: {audioResults.average_db.toFixed(2)} dB</p>
                <p>Maksymalny poziom dB: {audioResults.max_db.toFixed(2)} dB</p>
                <p>Minimalny poziom dB: {audioResults.min_db.toFixed(2)} dB</p>
              </>
            ) : (
              <pre>{JSON.stringify(result, null, 2)}</pre>
            )}
          </div>
        );
      })}
    </div>
  );
};

const dropzoneStyles: React.CSSProperties = {
  border: "2px dashed #cccccc",
  borderRadius: "4px",
  padding: "20px",
  textAlign: "center",
  cursor: "pointer",
  marginBottom: "20px",
};

const resultsStyles: React.CSSProperties = {
  marginTop: "20px",
  padding: "15px",
  border: "1px solid #ddd",
  borderRadius: "4px",
  backgroundColor: "#f9f9f9",
};

export default FileUpload;
