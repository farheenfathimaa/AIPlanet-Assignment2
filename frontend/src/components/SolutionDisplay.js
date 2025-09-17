import React, { useEffect, useRef } from 'react';
import 'katex/dist/katex.min.css';
import katex from 'katex';

const SolutionDisplay = ({ solution }) => {
  const solutionRef = useRef(null);

  useEffect(() => {
    if (solutionRef.current && solution) {
      solutionRef.current.innerHTML = solution.solution;
      window.renderMathInElement(solutionRef.current, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false },
        ],
        throwOnError: false,
      });
    }
  }, [solution]);

  return (
    <div className="solution-container">
      <h3>Solution</h3>
      <div ref={solutionRef}></div>
      <p><em>Source: {solution.source}</em></p>
    </div>
  );
};

export default SolutionDisplay;