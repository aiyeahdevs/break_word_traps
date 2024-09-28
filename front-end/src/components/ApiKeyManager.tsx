import React, { useState } from 'react';

interface ApiKeyManagerProps {
  onSave: (apiKey: string) => void;
}

const ApiKeyManager: React.FC<ApiKeyManagerProps> = ({ onSave }) => {
  const [apiKey, setApiKey] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(apiKey);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Enter API Key</h2>
      <input
        type="text"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        placeholder="Enter your API key"
        required
      />
      <button type="submit">Save API Key</button>
    </form>
  );
};

export default ApiKeyManager;
