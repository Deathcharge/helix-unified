"use client";

/**
 * 🖥️ Terminal Component
 * Real WebSocket-based terminal with backend execution
 */

import React, { useEffect, useRef } from 'react';

interface TerminalResult {
  command: string;
  output: string;
  error: string;
  exit_code: number;
  success: boolean;
  current_dir: string;
}

export default function Terminal() {
  const containerRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const [input, setInput] = React.useState('');
  const [output, setOutput] = React.useState<string[]>(['Helix Terminal v1.0', 'Connecting to backend...', '$ ']);
  const [connected, setConnected] = React.useState(false);
  const [currentDir, setCurrentDir] = React.useState('/home/helix');

  useEffect(() => {
    // Connect to WebSocket with JWT authentication
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const token = localStorage.getItem('token');

    if (!token) {
      setOutput(['❌ Not authenticated. Please log in.', '$ ']);
      return;
    }

    const wsUrl = `${protocol}//${window.location.host}/api/web-os/ws/terminal?token=${encodeURIComponent(token)}`;

    try {
      wsRef.current = new WebSocket(wsUrl);

      wsRef.current.onopen = () => {
        setConnected(true);
        setOutput(['Helix Terminal v1.0', '✅ Connected to backend', '$ ']);
      };

      wsRef.current.onmessage = (event) => {
        const result: TerminalResult = JSON.parse(event.data);

        setOutput((prev) => {
          const newOutput = [...prev];
          // Remove the last "$ " prompt
          newOutput.pop();

          // Add command
          newOutput.push(`$ ${result.command}`);

          // Add output or error
          if (result.error) {
            newOutput.push(result.error);
          }
          if (result.output) {
            newOutput.push(result.output);
          }

          // Add new prompt
          newOutput.push('$ ');
          return newOutput;
        });

        setCurrentDir(result.current_dir);
      };

      wsRef.current.onerror = (error) => {
        setOutput((prev) => [...prev, '❌ WebSocket error, falling back to REST API']);
        setConnected(false);
      };

      wsRef.current.onclose = () => {
        setConnected(false);
      };
    } catch (error) {
      setOutput((prev) => [...prev, `❌ Connection error: ${error}`]);
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const handleCommand = (cmd: string) => {
    if (!cmd.trim()) return;

    if (connected && wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      // Send via WebSocket
      wsRef.current.send(JSON.stringify({ command: cmd }));
      setInput('');
    } else {
      // Fallback to REST API
      handleCommandRest(cmd);
    }
  };

  const handleCommandRest = async (cmd: string) => {
    const newOutput = [...output];
    newOutput[newOutput.length - 1] = `$ ${cmd}`;

    try {
      const response = await fetch('/api/web-os/terminal/execute?command=' + encodeURIComponent(cmd) + '&user_id=default', {
        method: 'POST',
      });

      const result: TerminalResult = await response.json();

      if (result.error) {
        newOutput.push(result.error);
      }
      if (result.output) {
        newOutput.push(result.output);
      }

      setCurrentDir(result.current_dir);
    } catch (error) {
      newOutput.push(`❌ Error: ${error}`);
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
