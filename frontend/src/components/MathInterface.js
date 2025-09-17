import React, { useState } from 'react';

const MathInterface = ({ onAsk, loading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onAsk(query);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a math question..."
        disabled={loading}
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Solving...' : 'Ask'}
      </button>
    </form>
  );
};

export default MathInterface;