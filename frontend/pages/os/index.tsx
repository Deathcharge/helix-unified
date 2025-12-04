/**
 * 🖥️ Helix Web OS v2.0 - LAUNCH READY
 * Full-featured browser-based operating system
 *
 * NEW FEATURES:
 * ✅ Save/load file state (localStorage)
 * ✅ Terminal command history (up/down arrows)
 * ✅ Code editor syntax highlighting
 * ✅ Window maximize/restore
 * ✅ Keyboard shortcuts (Ctrl+T, Ctrl+E, Ctrl+F, Ctrl+W)
 * ✅ Settings panel
 */

import React, { useState, useEffect, useCallback } from 'react';
import dynamic from 'next/dynamic';

// Lazy load to avoid SSR issues
const Terminal = dynamic(() => import('@/components/Terminal'), { ssr: false });
const FileExplorer = dynamic(() => import('@/components/FileExplorer'), { ssr: false });
const CodeEditor = dynamic(() => import('@/components/CodeEditor'), { ssr: false });

interface OSWindow {
  id: string;
  type: 'terminal' | 'explorer' | 'editor' | 'settings';
  title: string;
  isMinimized: boolean;
  isMaximized: boolean;
  x: number;
  y: number;
  width: number;
  height: number;
  data?: any; // Window-specific data
}

interface OSSettings {
  theme: 'dark' | 'darker' | 'darkest';
  fontSize: number;
  terminalHistory: number;
  autoSave: boolean;
}

const DEFAULT_SETTINGS: OSSettings = {
  theme: 'dark',
  fontSize: 14,
  terminalHistory: 100,
  autoSave: true
};

export default function WebOS() {
  const [windows, setWindows] = useState<OSWindow[]>([]);
  const [activeWindowId, setActiveWindowId] = useState<string | null>(null);
  const [settings, setSettings] = useState<OSSettings>(DEFAULT_SETTINGS);
  const [showSettingsPanel, setShowSettingsPanel] = useState(false);

  // Load state from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('helix-os-state');
    if (saved) {
      try {
        const state = JSON.parse(saved);
        setWindows(state.windows || []);
        setSettings(state.settings || DEFAULT_SETTINGS);
      } catch (e) {
        console.error('Failed to load OS state:', e);
      }
    } else {
      // Open file explorer by default
      openWindow('explorer');
    }
  }, []);

  // Auto-save state to localStorage
  useEffect(() => {
    if (settings.autoSave && windows.length > 0) {
      const state = { windows, settings };
      localStorage.setItem('helix-os-state', JSON.stringify(state));
    }
  }, [windows, settings]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey) {
        switch(e.key.toLowerCase()) {
          case 't':
            e.preventDefault();
            openWindow('terminal');
            break;
          case 'e':
            e.preventDefault();
            openWindow('editor');
            break;
          case 'f':
            e.preventDefault();
            openWindow('explorer');
            break;
          case 'w':
            e.preventDefault();
            if (activeWindowId) closeWindow(activeWindowId);
            break;
          case ',':
            e.preventDefault();
            setShowSettingsPanel(true);
            break;
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [activeWindowId]);

  const openWindow = useCallback((type: OSWindow['type']) => {
    const newWindow: OSWindow = {
      id: `${type}-${Date.now()}`,
      type,
      title: type === 'terminal' ? '⌨️ Terminal'
        : type === 'explorer' ? '📁 File Explorer'
        : type === 'editor' ? '✏️ Code Editor'
        : '⚙️ Settings',
      isMinimized: false,
      isMaximized: false,
      x: Math.random() * 150 + 50,
      y: Math.random() * 150 + 50,
      width: 800,
      height: 600,
      data: {}
    };

    setWindows(prev => [...prev, newWindow]);
    setActiveWindowId(newWindow.id);
  }, []);

  const closeWindow = useCallback((id: string) => {
    setWindows(prev => prev.filter(w => w.id !== id));
    if (activeWindowId === id) {
      setActiveWindowId(windows.find(w => w.id !== id)?.id || null);
    }
  }, [activeWindowId, windows]);

  const toggleMinimize = useCallback((id: string) => {
    setWindows(prev =>
      prev.map(w =>
        w.id === id ? { ...w, isMinimized: !w.isMinimized } : w
      )
    );
  }, []);

  const toggleMaximize = useCallback((id: string) => {
    setWindows(prev =>
      prev.map(w =>
        w.id === id ? { ...w, isMaximized: !w.isMaximized } : w
      )
    );
  }, []);

  const updateWindowData = useCallback((id: string, data: any) => {
    setWindows(prev =>
      prev.map(w =>
        w.id === id ? { ...w, data: { ...w.data, ...data } } : w
      )
    );
  }, []);

  const clearAllWindows = () => {
    setWindows([]);
    setActiveWindowId(null);
  };

  const resetOS = () => {
    localStorage.removeItem('helix-os-state');
    setWindows([]);
    setSettings(DEFAULT_SETTINGS);
    openWindow('explorer');
  };

  return (
    <div
      className={`h-screen w-screen overflow-hidden ${
        settings.theme === 'darkest' ? 'bg-black'
        : settings.theme === 'darker' ? 'bg-slate-950'
        : 'bg-gradient-to-b from-slate-900 via-purple-900 to-slate-900'
      }`}
      style={{ fontSize: `${settings.fontSize}px` }}
    >
      {/* Taskbar */}
      <div className="fixed bottom-0 left-0 right-0 h-16 bg-slate-950/90 border-t border-purple-800/30 backdrop-blur-lg flex items-center px-4 gap-2 z-50">
        {/* App Launcher */}
        <div className="flex gap-2">
          <button
            onClick={() => openWindow('explorer')}
            className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-white text-sm transition-colors"
            title="File Explorer (Ctrl+F)"
          >
            📁 Files
          </button>
          <button
            onClick={() => openWindow('terminal')}
            className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-white text-sm transition-colors"
            title="Terminal (Ctrl+T)"
          >
            ⌨️ Terminal
          </button>
          <button
            onClick={() => openWindow('editor')}
            className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-white text-sm transition-colors"
            title="Code Editor (Ctrl+E)"
          >
            ✏️ Editor
          </button>
          <button
            onClick={() => setShowSettingsPanel(true)}
            className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-white text-sm transition-colors"
            title="Settings (Ctrl+,)"
          >
            ⚙️
          </button>
        </div>

        <div className="flex-1" />

        {/* Open Windows */}
        <div className="flex gap-1 max-w-xl overflow-x-auto">
          {windows.map(w => (
            <button
              key={w.id}
              onClick={() => {
                setActiveWindowId(w.id);
                if (w.isMinimized) toggleMinimize(w.id);
              }}
              className={`px-3 py-1 rounded text-xs transition-colors whitespace-nowrap ${
                activeWindowId === w.id
                  ? 'bg-purple-600 text-white'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {w.title}
            </button>
          ))}
        </div>

        {/* System Tray */}
        <div className="flex items-center gap-4">
          <span className="text-xs text-slate-400">
            {windows.length} window{windows.length !== 1 ? 's' : ''}
          </span>
          <span className="text-xs text-slate-400">
            {new Date().toLocaleTimeString()}
          </span>
        </div>
      </div>

      {/* Windows Container */}
      <div className="relative h-[calc(100vh-64px)] overflow-hidden">
        {windows.map(window => (
          <WindowFrame
            key={window.id}
            window={window}
            isActive={activeWindowId === window.id}
            onClose={() => closeWindow(window.id)}
            onMinimize={() => toggleMinimize(window.id)}
            onMaximize={() => toggleMaximize(window.id)}
            onFocus={() => setActiveWindowId(window.id)}
            settings={settings}
            onUpdateData={(data) => updateWindowData(window.id, data)}
          >
            {window.type === 'terminal' && (
              <Terminal
                historySize={settings.terminalHistory}
                fontSize={settings.fontSize}
              />
            )}
            {window.type === 'explorer' && <FileExplorer />}
            {window.type === 'editor' && (
              <CodeEditor
                fontSize={settings.fontSize}
                syntaxHighlighting={true}
              />
            )}
          </WindowFrame>
        ))}
      </div>

      {/* Settings Panel */}
      {showSettingsPanel && (
        <SettingsPanel
          settings={settings}
          onSettingsChange={setSettings}
          onClose={() => setShowSettingsPanel(false)}
          onClearWindows={clearAllWindows}
          onResetOS={resetOS}
        />
      )}

      {/* Keyboard Shortcuts Help */}
      <div className="fixed top-4 right-4 bg-slate-900/80 backdrop-blur-lg border border-purple-800/30 rounded-lg p-3 text-xs text-slate-300">
        <div className="font-bold mb-2">Keyboard Shortcuts:</div>
        <div>Ctrl+T - Terminal</div>
        <div>Ctrl+E - Editor</div>
        <div>Ctrl+F - Files</div>
        <div>Ctrl+W - Close Window</div>
        <div>Ctrl+, - Settings</div>
      </div>
    </div>
  );
}

// Enhanced Window Frame Component
interface WindowFrameProps {
  window: OSWindow;
  isActive: boolean;
  onClose: () => void;
  onMinimize: () => void;
  onMaximize: () => void;
  onFocus: () => void;
  settings: OSSettings;
  onUpdateData: (data: any) => void;
  children: React.ReactNode;
}

function WindowFrame({
  window,
  isActive,
  onClose,
  onMinimize,
  onMaximize,
  onFocus,
  children
}: WindowFrameProps) {
  const [position, setPosition] = useState({ x: window.x, y: window.y });
  const [size, setSize] = useState({ width: window.width, height: window.height });
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });

  const handleMouseDown = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest('[data-no-drag]')) return;
    if (window.isMaximized) return;

    setIsDragging(true);
    setDragOffset({
      x: e.clientX - position.x,
      y: e.clientY - position.y
    });
    onFocus();
  };

  useEffect(() => {
    if (!isDragging) return;

    const handleMouseMove = (e: MouseEvent) => {
      setPosition({
        x: e.clientX - dragOffset.x,
        y: e.clientY - dragOffset.y
      });
    };

    const handleMouseUp = () => setIsDragging(false);

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragOffset]);

  if (window.isMinimized) return null;

  const windowStyle = window.isMaximized
    ? { left: 0, top: 0, right: 0, bottom: 64, width: '100%', height: 'calc(100vh - 64px)' }
    : { left: `${position.x}px`, top: `${position.y}px`, width: `${size.width}px`, height: `${size.height}px` };

  return (
    <div
      className={`absolute flex flex-col rounded-lg border shadow-2xl transition-all ${
        isActive
          ? 'border-purple-600/50 shadow-purple-600/20 bg-slate-900/98 z-40'
          : 'border-slate-700/50 shadow-slate-900/50 bg-slate-950/95 z-30'
      } ${window.isMaximized ? 'rounded-none' : ''}`}
      style={{
        ...windowStyle,
        cursor: isDragging ? 'grabbing' : 'default'
      }}
      onClick={onFocus}
    >
      {/* Title Bar */}
      <div
        className={`px-4 py-3 border-b ${
          isActive
            ? 'border-purple-600/30 bg-gradient-to-r from-purple-600/20 to-pink-600/10'
            : 'border-slate-700/30 bg-slate-800/50'
        } flex items-center justify-between ${window.isMaximized ? '' : 'cursor-grab active:cursor-grabbing'}`}
        onMouseDown={handleMouseDown}
      >
        <span className="font-semibold text-white text-sm select-none">{window.title}</span>
        <div className="flex gap-2" data-no-drag>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onMinimize();
            }}
            className="w-8 h-8 flex items-center justify-center hover:bg-slate-700/50 rounded transition-colors"
            title="Minimize"
          >
            <span className="text-white">−</span>
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onMaximize();
            }}
            className="w-8 h-8 flex items-center justify-center hover:bg-slate-700/50 rounded transition-colors"
            title={window.isMaximized ? "Restore" : "Maximize"}
          >
            <span className="text-white">{window.isMaximized ? '❐' : '□'}</span>
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onClose();
            }}
            className="w-8 h-8 flex items-center justify-center hover:bg-red-600/50 rounded transition-colors"
            title="Close (Ctrl+W)"
          >
            <span className="text-white">×</span>
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto bg-slate-900/50 backdrop-blur-sm">
        {children}
      </div>
    </div>
  );
}

// Settings Panel Component
interface SettingsPanelProps {
  settings: OSSettings;
  onSettingsChange: (settings: OSSettings) => void;
  onClose: () => void;
  onClearWindows: () => void;
  onResetOS: () => void;
}

function SettingsPanel({ settings, onSettingsChange, onClose, onClearWindows, onResetOS }: SettingsPanelProps) {
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-slate-900 border border-purple-800/30 rounded-lg p-6 w-full max-w-md shadow-2xl">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-white">⚙️ Helix OS Settings</h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white transition-colors"
          >
            ×
          </button>
        </div>

        <div className="space-y-6">
          {/* Theme */}
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Theme
            </label>
            <select
              value={settings.theme}
              onChange={(e) => onSettingsChange({ ...settings, theme: e.target.value as any })}
              className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white"
            >
              <option value="dark">Dark</option>
              <option value="darker">Darker</option>
              <option value="darkest">Darkest (Pure Black)</option>
            </select>
          </div>

          {/* Font Size */}
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Font Size: {settings.fontSize}px
            </label>
            <input
              type="range"
              min="12"
              max="20"
              value={settings.fontSize}
              onChange={(e) => onSettingsChange({ ...settings, fontSize: parseInt(e.target.value) })}
              className="w-full"
            />
          </div>

          {/* Terminal History */}
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Terminal History: {settings.terminalHistory} commands
            </label>
            <input
              type="range"
              min="50"
              max="500"
              step="50"
              value={settings.terminalHistory}
              onChange={(e) => onSettingsChange({ ...settings, terminalHistory: parseInt(e.target.value) })}
              className="w-full"
            />
          </div>

          {/* Auto Save */}
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-slate-300">
              Auto-save state
            </label>
            <button
              onClick={() => onSettingsChange({ ...settings, autoSave: !settings.autoSave })}
              className={`w-12 h-6 rounded-full transition-colors ${
                settings.autoSave ? 'bg-purple-600' : 'bg-slate-700'
              }`}
            >
              <div className={`w-5 h-5 bg-white rounded-full transition-transform ${
                settings.autoSave ? 'translate-x-6' : 'translate-x-1'
              }`} />
            </button>
          </div>

          {/* Actions */}
          <div className="pt-4 border-t border-slate-700 space-y-2">
            <button
              onClick={onClearWindows}
              className="w-full px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded transition-colors"
            >
              Close All Windows
            </button>
            <button
              onClick={() => {
                if (confirm('Reset all settings and clear saved state?')) {
                  onResetOS();
                  onClose();
                }
              }}
              className="w-full px-4 py-2 bg-red-900/20 hover:bg-red-900/30 text-red-400 border border-red-900/50 rounded transition-colors"
            >
              Reset OS
            </button>
          </div>
        </div>

        <div className="mt-6 text-xs text-slate-500 text-center">
          Helix Web OS v2.0 - Launch Ready Edition
        </div>
      </div>
    </div>
  );
}
