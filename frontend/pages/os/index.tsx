/**
 * 🖥️ Helix Web OS
 * Browser-based operating system
 *
 * Features: File explorer, terminal, code editor, all-in-one
 */

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';

// Lazy load terminal to avoid SSR issues
const Terminal = dynamic(() => import('@/components/Terminal'), { ssr: false });
const FileExplorer = dynamic(() => import('@/components/FileExplorer'), { ssr: false });
const CodeEditor = dynamic(() => import('@/components/CodeEditor'), { ssr: false });

interface Window {
  id: string;
  type: 'terminal' | 'explorer' | 'editor';
  title: string;
  isMinimized: boolean;
  x: number;
  y: number;
}

export default function WebOS() {
  const [windows, setWindows] = useState<Window[]>([
    {
      id: 'explorer-1',
      type: 'explorer',
      title: 'File Explorer',
      isMinimized: false,
      x: 50,
      y: 50,
    },
  ]);

  const [activeWindowId, setActiveWindowId] = useState('explorer-1');

  const openWindow = (type: 'terminal' | 'explorer' | 'editor') => {
    const newWindow: Window = {
      id: `${type}-${Date.now()}`,
      type,
      title:
        type === 'terminal'
          ? 'Terminal'
          : type === 'explorer'
            ? 'File Explorer'
            : 'Code Editor',
      isMinimized: false,
      x: Math.random() * 200 + 100,
      y: Math.random() * 200 + 100,
    };

    setWindows([...windows, newWindow]);
    setActiveWindowId(newWindow.id);
  };

  const closeWindow = (id: string) => {
    setWindows(windows.filter((w) => w.id !== id));
  };

  const toggleMinimize = (id: string) => {
    setWindows(
      windows.map((w) =>
        w.id === id ? { ...w, isMinimized: !w.isMinimized } : w
      )
    );
  };

  return (
    <div className="h-screen w-screen bg-gradient-to-b from-slate-900 via-purple-900 to-slate-900 overflow-hidden">
      {/* Taskbar */}
      <div className="fixed bottom-0 left-0 right-0 h-16 bg-slate-950/80 border-t border-purple-800/30 backdrop-blur flex items-center px-4 gap-2">
        <div className="flex gap-2">
          <button
            onClick={() => openWindow('explorer')}
            className="px-4 py-2 rounded bg-slate-800 hover:bg-slate-700 text-white text-sm transition"
            title="Open File Explorer"
          >
            📁 Files
          </button>
          <button
            onClick={() => openWindow('terminal')}
            className="px-4 py-2 rounded bg-slate-800 hover:bg-slate-700 text-white text-sm transition"
            title="Open Terminal"
          >
            ⌨️ Terminal
          </button>
          <button
            onClick={() => openWindow('editor')}
            className="px-4 py-2 rounded bg-slate-800 hover:bg-slate-700 text-white text-sm transition"
            title="Open Code Editor"
          >
            ✏️ Editor
          </button>
        </div>

        <div className="flex-1" />

        {/* Open Windows */}
        <div className="flex gap-1">
          {windows.map((w) => (
            <button
              key={w.id}
              onClick={() => {
                setActiveWindowId(w.id);
                if (w.isMinimized) toggleMinimize(w.id);
              }}
              className={`px-3 py-1 rounded text-xs transition ${
                activeWindowId === w.id
                  ? 'bg-purple-600 text-white'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {w.title}
            </button>
          ))}
        </div>

        <div className="ml-4 text-xs text-slate-400">
          {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* Windows Container */}
      <div className="relative h-[calc(100vh-64px)] overflow-hidden">
        {windows.map((window) => (
          <WindowFrame
            key={window.id}
            window={window}
            isActive={activeWindowId === window.id}
            onClose={() => closeWindow(window.id)}
            onMinimize={() => toggleMinimize(window.id)}
            onFocus={() => setActiveWindowId(window.id)}
          >
            {window.type === 'terminal' && <Terminal />}
            {window.type === 'explorer' && <FileExplorer />}
            {window.type === 'editor' && <CodeEditor />}
          </WindowFrame>
        ))}
      </div>
    </div>
  );
}

interface WindowFrameProps {
  window: Window;
  isActive: boolean;
  onClose: () => void;
  onMinimize: () => void;
  onFocus: () => void;
  children: React.ReactNode;
}

function WindowFrame({
  window,
  isActive,
  onClose,
  onMinimize,
  onFocus,
  children,
}: WindowFrameProps) {
  const [position, setPosition] = useState({ x: window.x, y: window.y });
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });

  const handleMouseDown = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest('[data-no-drag]')) return;

    setIsDragging(true);
    setDragOffset({
      x: e.clientX - position.x,
      y: e.clientY - position.y,
    });
    onFocus();
  };

  useEffect(() => {
    if (!isDragging) return;

    const handleMouseMove = (e: MouseEvent) => {
      setPosition({
        x: e.clientX - dragOffset.x,
        y: e.clientY - dragOffset.y,
      });
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragOffset]);

  if (window.isMinimized) return null;

  return (
    <div
      className={`absolute w-full max-w-2xl h-96 rounded-lg border shadow-lg flex flex-col transition-shadow ${
        isActive
          ? 'border-purple-600/50 shadow-purple-600/20 bg-slate-900/95'
          : 'border-slate-700/50 shadow-slate-900/50 bg-slate-950/95'
      }`}
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`,
        cursor: isDragging ? 'grabbing' : 'default',
      }}
      onClick={onFocus}
    >
      {/* Title Bar */}
      <div
        className={`px-4 py-3 border-b ${
          isActive
            ? 'border-purple-600/30 bg-gradient-to-r from-purple-600/20 to-pink-600/10'
            : 'border-slate-700/30 bg-slate-800/50'
        } flex items-center justify-between cursor-grab active:cursor-grabbing`}
        onMouseDown={handleMouseDown}
      >
        <span className="font-semibold text-white text-sm">{window.title}</span>
        <div className="flex gap-2" data-no-drag>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onMinimize();
            }}
            className="hover:bg-slate-700 p-1 rounded transition"
            title="Minimize"
          >
            <span className="text-sm">−</span>
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onClose();
            }}
            className="hover:bg-red-600 p-1 rounded transition"
            title="Close"
          >
            <span className="text-sm">×</span>
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto bg-slate-900/50">{children}</div>
    </div>
  );
}
