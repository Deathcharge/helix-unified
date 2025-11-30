/**
 * 🖥️ Terminal Component
 * Browser-based terminal using xterm.js
 */

import React, { useEffect, useRef } from 'react';

export default function Terminal() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [input, setInput] = React.useState('');
  const [output, setOutput] = React.useState<string[]>(['Helix Terminal v1.0', '$ ']);

  const handleCommand = (cmd: string) => {
    const newOutput = [...output];
    newOutput[newOutput.length - 1] = `$ ${cmd}`;

    // Simple mock commands
    if (cmd === 'help') {
      newOutput.push('Available commands:');
      newOutput.push('  ls - List files');
      newOutput.push('  pwd - Print working directory');
      newOutput.push('  help - Show this help');
      newOutput.push('  clear - Clear screen');
    } else if (cmd === 'clear') {
      newOutput.length = 0;
    } else if (cmd === 'ls') {
      newOutput.push('backend/  frontend/  docs/  README.md');
    } else if (cmd === 'pwd') {
      newOutput.push('/home/helix');
    } else if (cmd.startsWith('cd ')) {
      newOutput.push(`Changed directory to ${cmd.slice(3)}`);
    } else if (cmd) {
      newOutput.push(`Command not found: ${cmd}`);
    }

    newOutput.push('$ ');
    setOutput(newOutput);
    setInput('');
  };

  return (
    <div ref={containerRef} className="w-full h-full p-4 font-mono text-sm text-green-400 bg-black">
      {/* Terminal Output */}
      <div className="space-y-1 mb-4">
        {output.map((line, i) => (
          <div key={i}>{line}</div>
        ))}
      </div>

      {/* Input Line */}
      <div className="flex items-center">
        <span>$ </span>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleCommand(input);
            }
          }}
          autoFocus
          className="flex-1 bg-transparent outline-none text-green-400 ml-1"
          spellCheck="false"
        />
      </div>

      {/* Blinking Cursor */}
      <style>{`
        @keyframes blink {
          0%, 50% { opacity: 1; }
          51%, 100% { opacity: 0; }
        }
        input { animation: blink 1s infinite; }
      `}</style>
    </div>
  );
}
