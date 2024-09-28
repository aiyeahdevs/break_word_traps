import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { tasks } from "../tasks";

interface FileUploaderProps {
  apiKey: string;
  onJobStart: (jobId: string) => void;
  onJobComplete: () => void;
  setResults: React.Dispatch<React.SetStateAction<Record<string, any>>>;
  setLoadingTasks: React.Dispatch<
    React.SetStateAction<Record<string, boolean>>
  >;
  setError: React.Dispatch<React.SetStateAction<string | null>>;
}

interface JobResponse {
  job_id: string;
  message: string;
}

const FileUploader: React.FC<FileUploaderProps> = ({
  apiKey,
  onJobStart,
  onJobComplete,
  setResults,
  setLoadingTasks,
  setError,
}) => {
  const [files, setFiles] = useState<File[]>([]);
  const pollInterval = 2000; // 2 seconds

  const pollJobStatus = useCallback(
    async (jobId: string) => {
      const checkStatus = async () => {
        try {
          let allCompleted = true;
          for (const task of tasks) {
            const response = await fetch(
              `http://localhost:8000/job-result/${jobId}/${task.endpoint}`
            );
            if (response.status === 200) {
              const data = await response.json();
              setResults((prevResults) => ({
                ...prevResults,
                [task.name]: data[task.name],
              }));
              setLoadingTasks((prevLoadingTasks) => ({
                ...prevLoadingTasks,
                [task.name]: false,
              }));
            } else {
              allCompleted = false;
            }
          }

          if (!allCompleted) {
            setTimeout(checkStatus, pollInterval);
          } else {
            onJobComplete();
          }
        } catch (e) {
          setError("Wystąpił błąd podczas sprawdzania statusu zadania.");
          console.error("Job status error:", e);
          onJobComplete();
        }
      };

      checkStatus();
    },
    [onJobComplete, setError, setResults, tasks]
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

    setError(null);
    setResults({});

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
      onJobStart(data.job_id);
      pollJobStatus(data.job_id);
    } catch (e) {
      setError("Wystąpił błąd podczas przesyłania pliku.");
      console.error("Upload error:", e);
      onJobComplete();
    } finally {
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
      <button onClick={handleUpload} disabled={files.length === 0}>
        Wyślij pliki
      </button>
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

export default FileUploader;
