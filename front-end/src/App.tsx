import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import ApiKeyManager from './components/ApiKeyManager';

const App: React.FC = () => {
  const [apiKey, setApiKey] = useState<string>('');
  const [showApiKeyManager, setShowApiKeyManager] = useState<boolean>(false);

  useEffect(() => {
    const savedApiKey = localStorage.getItem('apiKey');
    if (savedApiKey) {
      setApiKey(savedApiKey);
    } else {
      setShowApiKeyManager(true);
    }
  }, []);

  const handleApiKeySave = (newApiKey: string) => {
    setApiKey(newApiKey);
    localStorage.setItem('apiKey', newApiKey);
    setShowApiKeyManager(false);
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px" }}>
      <h1>Pliki Wideo</h1>
      {showApiKeyManager ? (
        <ApiKeyManager onSave={handleApiKeySave} />
      ) : (
        <>
          <div>
            API Key: {'*'.repeat(apiKey.length)}
            <button onClick={() => setShowApiKeyManager(true)}>Change API Key</button>
          </div>
          <FileUpload apiKey={apiKey} />
        </>
      )}
    </div>
  );
};

export default App;
