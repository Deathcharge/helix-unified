/**
 * 📁 File Explorer Component
 * Browser-based file explorer
 */

import React, { useState } from 'react';

interface FileEntry {
  name: string;
  type: 'file' | 'folder';
  path: string;
  size?: number;
}

const mockFiles: Record<string, FileEntry[]> = {
  '/': [
    { name: 'backend', type: 'folder', path: '/backend' },
    { name: 'frontend', type: 'folder', path: '/frontend' },
    { name: 'docs', type: 'folder', path: '/docs' },
    { name: 'README.md', type: 'file', path: '/README.md', size: 5240 },
    { name: 'package.json', type: 'file', path: '/package.json', size: 1200 },
  ],
  '/backend': [
    { name: 'saas', type: 'folder', path: '/backend/saas' },
    { name: 'app.py', type: 'file', path: '/backend/app.py', size: 3200 },
    { name: 'main.py', type: 'file', path: '/backend/main.py', size: 2100 },
  ],
  '/backend/saas': [
    { name: 'stripe_service.py', type: 'file', path: '/backend/saas/stripe_service.py', size: 4200 },
    { name: 'auth_service.py', type: 'file', path: '/backend/saas/auth_service.py', size: 3800 },
    { name: 'dashboard_api.py', type: 'file', path: '/backend/saas/dashboard_api.py', size: 2900 },
  ],
  '/frontend': [
    { name: 'pages', type: 'folder', path: '/frontend/pages' },
    { name: 'components', type: 'folder', path: '/frontend/components' },
    { name: 'package.json', type: 'file', path: '/frontend/package.json', size: 890 },
  ],
};

export default function FileExplorer() {
  const [currentPath, setCurrentPath] = useState('/');
  const [selectedFile, setSelectedFile] = useState<FileEntry | null>(null);

  const files = mockFiles[currentPath] || [];

  const handleDoubleClick = (entry: FileEntry) => {
    if (entry.type === 'folder') {
      setCurrentPath(entry.path);
      setSelectedFile(null);
    } else {
      setSelectedFile(entry);
    }
  };

  const handleBack = () => {
    if (currentPath !== '/') {
      const parent = currentPath.split('/').slice(0, -1).join('/') || '/';
      setCurrentPath(parent);
      setSelectedFile(null);
    }
  };

  const formatSize = (bytes?: number) => {
    if (!bytes) return '-';
    if (bytes < 1024) return `${bytes}B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
  };

  return (
    <div className="w-full h-full flex flex-col bg-slate-900 text-slate-100">
      {/* Address Bar */}
      <div className="p-3 border-b border-slate-700 bg-slate-800/50 space-y-2">
        <div className="flex gap-2">
          <button
            onClick={handleBack}
            disabled={currentPath === '/'}
            className="px-3 py-1 rounded bg-slate-700 hover:bg-slate-600 disabled:opacity-50 text-sm"
          >
            ← Back
          </button>
          <div className="flex-1 px-3 py-1 rounded bg-slate-800 border border-slate-700 font-mono text-sm">
            {currentPath}
          </div>
        </div>
      </div>

      {/* File List */}
      <div className="flex-1 overflow-auto">
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
      </div>

      {/* Status Bar */}
      <div className="p-2 border-t border-slate-700 bg-slate-800/50 text-xs text-slate-400 flex justify-between">
        <span>{files.length} items</span>
        {selectedFile && <span>{selectedFile.name}</span>}
      </div>
    </div>
  );
}
