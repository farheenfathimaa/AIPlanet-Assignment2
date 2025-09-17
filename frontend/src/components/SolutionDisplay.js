import React from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import 'katex/dist/katex.min.css';
import ReactMarkdown from 'react-markdown';

const SolutionDisplay = ({ solution }) => {
  if (!solution || !solution.solution) {
    return null;
  }

  const renderers = {
    // This is the core fix: check if children is an array.
    p: ({ children }) => {
      const flatChildren = React.Children.toArray(children);
      return <p>{flatChildren}</p>;
    },
    // We can also simplify how we handle code blocks
    code: ({ children, inline, className }) => {
      const codeContent = String(children).trim();
      if (inline) {
        return <InlineMath math={codeContent} />;
      }
      if (className && className.includes('language-latex')) {
        return <BlockMath math={codeContent} />;
      }
      return <code>{codeContent}</code>;
    },
    // `ReactMarkdown` handles everything else by default
  };

  return (
    <div className="solution-container">
      <h3>Solution</h3>
      <ReactMarkdown components={renderers}>
        {solution.solution}
      </ReactMarkdown>
      <p><em>Source: {solution.source}</em></p>
    </div>
  );
};

export default SolutionDisplay;