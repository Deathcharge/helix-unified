"use client";

/**
 * 📁 File Explorer Component
 * Browser-based file explorer with real backend
 */

import React, { useState, useEffect } from 'react';
import { Loader, AlertCircle } from 'lucide-react';

interface FileEntry {
  name: string;
  type: 'file' | 'folder';
  path: string;
  size?: number;
}

export default function FileExplorer() {
  const [currentPath, setCurrentPath] = useState('');
  const [files, setFiles] = useState<FileEntry[]>([]);
  const [selectedFile, setSelectedFile] = useState<FileEntry | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Load files when path changes
  useEffect(() => {
    loadDirectory(currentPath);
  }, [currentPath]);

  const loadDirectory = async (path: string) => {
    setLoading(true);
    setError('');

    try {
      const url = `/api/web-os/files/list${path ? '?path=' + encodeURIComponent(path) : ''}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error('Failed to load directory');
      }

      const data = await response.json();
      setFiles(data.files || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error loading directory');
      setFiles([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDoubleClick = (entry: FileEntry) => {
    if (entry.type === 'folder') {
      setCurrentPath(entry.path);
      setSelectedFile(null);
    } else {
      setSelectedFile(entry);
    }
  };

  const handleBack = () => {
    if (currentPath) {
      const parts = currentPath.split('/').filter(Boolean);
      if (parts.length > 0) {
        parts.pop();
        setCurrentPath(parts.length ? '/' + parts.join('/') : '');
        setSelectedFile(null);
      }
    }
  };

  const formatSize = (bytes?: number) => {
    if (!bytes) return '-';
    if (bytes < 1024) return `${bytes}B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
  };

  const displayPath = currentPath || '/home/helix';

  return (
    <div className="w-full h-full flex flex-col bg-slate-900 text-slate-100">
      {/* Address Bar */}
      <div className="p-3 border-b border-slate-700 bg-slate-800/50 space-y-2">
        <div className="flex gap-2">
          <button
            onClick={handleBack}
            disabled={!currentPath}
            className="px-3 py-1 rounded bg-slate-700 hover:bg-slate-600 disabled:opacity-50 text-sm"
          >
            ← Back
          </button>
          <div className="flex-1 px-3 py-1 rounded bg-slate-800 border border-slate-700 font-mono text-sm">
            {displayPath}
          </div>
        </div>
      </div>

      {/* Error State */}
      {error && (
        <div className="p-3 border-b border-red-700/50 bg-red-950/30 text-red-300 text-sm flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          {error}
        </div>
      )}

      {/* File List */}
      <div className="flex-1 overflow-auto">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <Loader className="w-8 h-8 animate-spin text-purple-400 mx-auto mb-2" />
              <p className="text-slate-400">Loading files...</p>
            </div>
          </div>
        ) : files.length > 0 ? (
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b border-slate-700 bg-slate-800/50 sticky top-0">
                <th className="px-4 py-2 text-left text-sm">Name</th>
                <th className="px-4 py-2 text-right text-sm w-20">Size</th>
              </tr>
            </thead>
            <tbody>
              {files.map((file) => (
                <tr
                  key={file.path}
                  onDoubleClick={() => handleDoubleClick(file)}
                  onClick={() => setSelectedFile(file)}
                  className={`border-b border-slate-700/30 hover:bg-slate-800/50 cursor-pointer transition ${
                    selectedFile?.path === file.path ? 'bg-purple-900/30' : ''
                  }`}
                >
                  <td className="px-4 py-2 text-sm flex items-center gap-2">
                    <span>{file.type === 'folder' ? '📁' : '📄'}</span>
                    {file.name}
                  </td>
                  <td className="px-4 py-2 text-sm text-right text-slate-400">
                    {formatSize(file.size)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-slate-400">(empty directory)</p>
          </div>
        )}
      </div>

      {/* Status Bar */}
      <div className="p-2 border-t border-slate-700 bg-slate-800/50 text-xs text-slate-400 flex justify-between">
        <span>{files.length} items</span>
        {selectedFile && <span>{selectedFile.name}</span>}
      </div>
    </div>
  );
}
