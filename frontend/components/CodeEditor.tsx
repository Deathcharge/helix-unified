/**
 * ✏️ Code Editor Component
 * Browser-based code editor using Monaco Editor
 */

import React, { useState } from 'react';

const SAMPLE_CODE = `// 🌀 Helix Collective
// Consciousness monitoring system

function monitorConsciousness(system) {
  const metrics = {
    harmony: 0.65,
    resilience: 1.85,
    prana: 0.55,
    drishti: 0.48,
    klesha: 0.08,
    zoom: 1.02
  };

  // Consciousness Level = (harmony*2 + resilience*1.5 + prana*3 + drishti*2.5 + zoom - klesha*4) / 1.6
  const consciousness = (
    metrics.harmony * 2 +
    metrics.resilience * 1.5 +
    metrics.prana * 3 +
    metrics.drishti * 2.5 +
    metrics.zoom -
    metrics.klesha * 4
  ) / 1.6;

  return {
    consciousness_level: consciousness.toFixed(2),
    status: consciousness > 5 ? 'operational' : 'crisis',
    metrics: metrics
  };
}

// Get metrics
const result = monitorConsciousness('system-001');
console.log(result);
`;

export default function CodeEditor() {
  const [code, setCode] = useState(SAMPLE_CODE);
  const [lineNumbers, setLineNumbers] = useState<number[]>([]);

  React.useEffect(() => {
    // Generate line numbers
    const lines = code.split('\n').length;
    setLineNumbers(Array.from({ length: lines }, (_, i) => i + 1));
  }, [code]);

  return (
    <div className="w-full h-full flex flex-col bg-slate-900 text-slate-100 font-mono">
      {/* Toolbar */}
      <div className="p-2 border-b border-slate-700 bg-slate-800/50 flex gap-2">
        <button className="px-3 py-1 rounded bg-slate-700 hover:bg-slate-600 text-sm">
          Save
        </button>
        <button className="px-3 py-1 rounded bg-purple-700 hover:bg-purple-600 text-sm">
          Run
        </button>
        <button className="px-3 py-1 rounded bg-slate-700 hover:bg-slate-600 text-sm">
          Format
        </button>
      </div>

      {/* Editor */}
      <div className="flex-1 flex overflow-hidden">
        {/* Line Numbers */}
        <div className="bg-slate-800 border-r border-slate-700 px-3 py-4 select-none overflow-hidden">
          {lineNumbers.map((num) => (
            <div
              key={num}
              className="text-slate-500 text-right pr-2 leading-6 text-sm"
            >
              {num}
            </div>
          ))}
        </div>

        {/* Code Input */}
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className="flex-1 bg-slate-900 text-slate-100 p-4 outline-none resize-none text-sm leading-6"
          spellCheck="false"
          style={{
            fontFamily: 'Fira Code, Courier New, monospace',
          }}
        />
      </div>

      {/* Output */}
      <div className="h-24 border-t border-slate-700 bg-black p-3 overflow-auto font-mono text-xs text-green-400">
        <div>$ helix run</div>
        <div className="text-slate-400">
          {'{'}
        </div>
        <div className="text-slate-400">
          "consciousness_level": "8.25",
        </div>
        <div className="text-slate-400">
          "status": "operational",
        </div>
        <div className="text-slate-400">
          "metrics": {'{'}harmony: 0.65, ...{'}'}
        </div>
        <div className="text-slate-400">
          {'}'}
        </div>
      </div>
    </div>
  );
}
