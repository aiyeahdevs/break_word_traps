import React, { useState } from "react";
import FileUpload from "./components/FileUpload";

const UPLOAD_ENDPOINT = "https://api.example.com/upload"; // Replace with your actual endpoint

const App: React.FC = () => {
  const [uploadStatus, setUploadStatus] = useState<string>("");

  const handleUpload = async (files: File[]) => {
    setUploadStatus("Uploading...");
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    try {
      const response = await fetch(UPLOAD_ENDPOINT, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        setUploadStatus("Files uploaded successfully!");
      } else {
        setUploadStatus("Upload failed. Please try again.");
      }
    } catch (error) {
      console.error("Error uploading files:", error);
      setUploadStatus("Upload failed. Please try again.");
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px" }}>
      <h1>File Upload Dropzone</h1>
      <FileUpload onUpload={handleUpload} />
      {uploadStatus && <p>{uploadStatus}</p>}
    </div>
  );
};

export default App;
