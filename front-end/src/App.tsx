import React, { useState } from "react";
import FileUpload from "./components/FileUpload";

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileUpload = (uploadedFile: File) => {
    setFile(uploadedFile);
    console.log("File uploaded:", uploadedFile.name);
    // Here you can add logic to process the file or send it to a server
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px" }}>
      <h1>File Upload Dropzone</h1>
      <FileUpload onFileUpload={handleFileUpload} />
      {file && <p style={{ marginTop: "20px" }}>File selected: {file.name}</p>}
    </div>
  );
};

export default App;
