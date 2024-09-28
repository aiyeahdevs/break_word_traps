import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";

interface AnalysisResult {
  too_loud_percentage: number;
  too_quiet_percentage: number;
  average_db: number;
  max_db: number;
  min_db: number;
}

interface FileUploadProps {
  apiKey: string;
}

const FileUpload: React.FC<FileUploadProps> = ({ apiKey }) => {
  const [files, setFiles] = useState<File[]>([]);
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
    setResults(null);

    const formData = new FormData();
    formData.append("file", files[0]);

    try {
      const response = await fetch("http://localhost:8000/analyze_volume/", {
        method: "POST",
        headers: {
          'llmkey': apiKey
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (e) {
      setError("An error occurred while uploading the file.");
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
          <p>Wrzuć pliki MP4 tutaj ...</p>
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
      {results && (
        <div style={resultsStyles}>
          <h4>Wyniki analizy:</h4>
          <p>Procent zbyt głośnego dźwięku: {results.too_loud_percentage.toFixed(2)}%</p>
          <p>Procent zbyt cichego dźwięku: {results.too_quiet_percentage.toFixed(2)}%</p>
          <p>Średni poziom dB: {results.average_db.toFixed(2)} dB</p>
          <p>Maksymalny poziom dB: {results.max_db.toFixed(2)} dB</p>
          <p>Minimalny poziom dB: {results.min_db.toFixed(2)} dB</p>
        </div>
      )}
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
