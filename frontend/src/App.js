import React, { useState } from 'react';
import './App.css';
import MathInterface from './components/MathInterface';
import SolutionDisplay from './components/SolutionDisplay';
import FeedbackForm from './components/FeedbackForm';
import { askQuestion, submitFeedback } from './services/api';

function App() {
  const [question, setQuestion] = useState('');
  const [solution, setSolution] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAsk = async (q) => {
    setLoading(true);
    setSolution(null);
    setError(null);
    try {
      const response = await askQuestion(q);
      setQuestion(q);
      setSolution(response);
    } catch (err) {
      setError(err.response?.data?.detail || 'An unknown error occurred.');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (rating, comments) => {
    try {
      await submitFeedback({
        question: solution.question,
        solution: solution.solution,
        rating,
        comments,
      });
      alert('Feedback submitted!');
    } catch (err) {
      alert('Failed to submit feedback.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Math Routing Agent</h1>
        <p>Your personal AI math professor.</p>
      </header>
      <main>
        <MathInterface onAsk={handleAsk} loading={loading} />
        {loading && <p>Thinking...</p>}
        {error && <p className="error">{error}</p>}
        {solution && (
          <>
            <SolutionDisplay solution={solution} />
            <FeedbackForm onFeedback={handleFeedback} />
          </>
        )}
      </main>
    </div>
  );
}

export default App;