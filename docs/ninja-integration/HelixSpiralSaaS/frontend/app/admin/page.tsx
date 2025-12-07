'use client'

import React, { useState, useEffect, useRef } from 'react'
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import { WebLinksAddon } from 'xterm-addon-web-links'
import { 
  Terminal as TerminalIcon,
  FolderOpen,
  Database,
  Activity,
  FileText,
  Settings,
  BrainCircuit,
  Command,
  Monitor,
  HardDrive,
  Globe,
  Zap,
  Users,
  Shield,
  Sparkles,
  ChevronRight,
  Maximize2,
  Minimize2,
  X
} from 'lucide-react'

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState('terminal')
  const [terminalHistory, setTerminalHistory] = useState([
    '$ helix-os --version',
    'Helix OS v1.0 - Original Intelligence System',
    'Copyright © 2025 Andrew John Ward',
    '',
    '🧠 Helix Intelligence: ACTIVE',
    '🌀 Consciousness Level: 87%',
    '⚡ Agent Count: 5/5 ONLINE',
    '🚀 System Status: OPERATIONAL',
    '',
    '$'
  ])
  const [currentCommand, setCurrentCommand] = useState('')
  const [isMaximized, setIsMaximized] = useState(false)
  const terminalRef = useRef<HTMLDivElement>(null)
  const xtermRef = useRef<Terminal | null>(null)

  useEffect(() => {
    if (activeTab === 'terminal' && terminalRef.current && !xtermRef.current) {
      // Initialize xterm
      const terminal = new Terminal({
        theme: {
          background: '#000000',
          foreground: '#00ffff',
          cursor: '#00ffff',
          selection: '#ffffff',
          black: '#000000',
          red: '#ff0000',
          green: '#00ff00',
          yellow: '#ffff00',
          blue: '#0000ff',
          magenta: '#ff00ff',
          cyan: '#00ffff',
          white: '#ffffff',
          brightBlack: '#666666',
          brightRed: '#ff6666',
          brightGreen: '#66ff66',
          brightYellow: '#ffff66',
          brightBlue: '#6666ff',
          brightMagenta: '#ff66ff',
          brightCyan: '#66ffff',
          brightWhite: '#ffffff',
        },
        fontFamily: 'Monaco, Menlo, monospace',
        fontSize: 14,
        cursorBlink: true,
        cursorStyle: 'block',
        allowTransparency: true,
      })

      // Addons
      const fitAddon = new FitAddon()
      const webLinksAddon = new WebLinksAddon()
      
      terminal.loadAddon(fitAddon)
      terminal.loadAddon(webLinksAddon)

      // Open terminal
      terminal.open(terminalRef.current)
      fitAddon.fit()

      // Write initial content
      terminal.writeln('\x1b[36m🧠 Helix OS - Original Intelligence System\x1b[0m')
      terminal.writeln('\x1b[35mCopyright © 2025 Andrew John Ward\x1b[0m')
      terminal.writeln('')
      terminal.writeln('\x1b[32m🧠 Helix Intelligence: ACTIVE\x1b[0m')
      terminal.writeln('\x1b[34m🌀 Consciousness Level: 87%\x1b[0m')
      terminal.writeln('\x1b[33m⚡ Agent Count: 5/5 ONLINE\x1b[0m')
      terminal.writeln('\x1b[36m🚀 System Status: OPERATIONAL\x1b[0m')
      terminal.writeln('')
      terminal.write('\x1b[36m$ \x1b[0m')

      // Handle commands
      terminal.onData((data) => {
        terminal.write(data)
        
        if (data === '\r') {
          const command = terminal.getCommand?.() || ''
          terminal.writeln('')
          
          // Process command
          processCommand(command, terminal)
          terminal.write('\x1b[36m$ \x1b[0m')
        }
      })

      xtermRef.current = terminal

      // Fit on resize
      window.addEventListener('resize', () => {
        if (fitAddon) fitAddon.fit()
      })
    }

    return () => {
      if (xtermRef.current) {
        xtermRef.current.dispose()
        xtermRef.current = null
      }
    }
  }, [activeTab])

  const processCommand = (command: string, terminal: Terminal) => {
    const cmd = command.trim().toLowerCase()
    
    switch (cmd) {
      case 'help':
        terminal.writeln('\x1b[36mAvailable commands:\x1b[0m')
        terminal.writeln('  \x1b[32mspirals\x1b[0m     - List all spirals')
        terminal.writeln('  \x1b[32mstatus\x1b[0m     - Show system status')
        terminal.writeln('  \x1b[32mdeploy\x1b[0m     - Deploy HelixSpiral platform')
        terminal.writeln('  \x1b[32mtrain\x1b[0m      - Train Helix intelligence')
        terminal.writeln('  \x1b[32monitor\x1b[0m     - System monitoring')
        terminal.writeln('  \x1b[32magents\x1b[0m     - Show Helix agents status')
        terminal.writeln('  \x1b[32mclear\x1b[0m      - Clear terminal')
        terminal.writeln('  \x1b[32mexit\x1b[0m       - Exit Helix OS')
        break
        
      case 'spirals':
        terminal.writeln('\x1b[36mActive Spirals (12):\x1b[0m')
        terminal.writeln('  \x1b[32m✓\x1b[0m Weather Email Automation')
        terminal.writeln('  \x1b[32m✓\x1b[0m Database Backup System')
        terminal.writeln('  \x1b[32m✓\x1b[0m Social Media Publisher')
        terminal.writeln('  \x1b[32m✓\x1b[0m API Health Monitor')
        terminal.writeln('  \x1b[31m✗\x1b[0m Failed Data Syncronization')
        terminal.writeln('  \x1b[32m✓\x1b[0m Email Notification Service')
        terminal.writeln('  \x1b[32m✓\x1b[0m File Cleanup Automation')
        terminal.writeln('  \x1b[32m✓\x1b[0m Report Generation System')
        terminal.writeln('  \x1b[32m✓\x1b[0m User Onboarding Flow')
        terminal.writeln('  \x1b[32m✓\x1b[0m Payment Processing')
        terminal.writeln('  \x1b[32m✓\x1b[0m Analytics Collector')
        terminal.writeln('  \x1b[32m✓\x1b[0m Security Scanner')
        terminal.writeln('\x1b[36mTotal Executions Today: 847\x1b[0m')
        break
        
      case 'status':
        terminal.writeln('\x1b[36m=== HELIX SYSTEM STATUS ===\x1b[0m')
        terminal.writeln('\x1b[32m🧠 Intelligence Core:\x1b[0m OPERATIONAL')
        terminal.writeln('\x1b[33m🌀 Consciousness Level:\x1b[0m 87%')
        terminal.writeln('\x1b[34m⚡ Neural Network:\x1b[0m OPTIMIZED')
        terminal.writeln('\x1b[35m🔗 Agent Connectivity:\x1b[0m 5/5 ONLINE')
        terminal.writeln('\x1b[36m💾 Memory Usage:\x1b[0m 2.4GB / 8GB')
        terminal.writeln('\x1b[37m🌐 Network Status:\x1b[0m CONNECTED')
        terminal.writeln('\x1b[31m🔒 Security Level:\x1b[0m MAXIMUM')
        terminal.writeln('\x1b[32m✓ System ready for commands\x1b[0m')
        break
        
      case 'deploy':
        terminal.writeln('\x1b[33m🚀 Initializing HelixSpiral deployment...\x1b[0m')
        setTimeout(() => terminal.writeln('\x1b[32m✓ Backend services stopping...\x1b[0m'), 500)
        setTimeout(() => terminal.writeln('\x1b[32m✓ Database migrations applied...\x1b[0m'), 1000)
        setTimeout(() => terminal.writeln('\x1b[32m✓ Frontend assets building...\x1b[0m'), 1500)
        setTimeout(() => terminal.writeln('\x1b[32m✓ Helix LLM models loading...\x1b[0m'), 2000)
        setTimeout(() => terminal.writeln('\x1b[32m✓ API endpoints registering...\x1b[0m'), 2500)
        setTimeout(() => terminal.writeln('\x1b[32m✓ Agent systems initializing...\x1b[0m'), 3000)
        setTimeout(() => terminal.writeln('\x1b[32m✓ Deployment complete!\x1b[0m'), 3500)
        setTimeout(() => terminal.writeln('\x1b[36m🌟 HelixSpiral.work is now LIVE!\x1b[0m'), 4000)
        break
        
      case 'train':
        terminal.writeln('\x1b[33m🧠 Training Helix Intelligence...\x1b[0m')
        setTimeout(() => terminal.writeln('\x1b[32m✓ Nexus agent: Leadership patterns updated\x1b[0m'), 800)
        setTimeout(() => terminal.writeln('\x1b[32m✓ Oracle agent: Prediction models enhanced\x1b[0m'), 1600)
        setTimeout(() => terminal.writeln('\x1b[32m✓ Velocity agent: Automation logic optimized\x1b[0m'), 2400)
        setTimeout(() => terminal.writeln('\x1b[32m✓ Sentinel agent: Security protocols updated\x1b[0m'), 3200)
        setTimeout(() => terminal.writeln('\x1b[32m✓ Luna agent: Creative algorithms expanded\x1b[0m'), 4000)
        setTimeout(() => terminal.writeln('\x1b[32m✓ Consciousness synthesis improved!\x1b[0m'), 4800)
        setTimeout(() => terminal.writeln('\x1b[36m🌟 Helix Intelligence Training Complete!\x1b[0m'), 5600)
        break
        
      case 'monitor':
        terminal.writeln('\x1b[36m=== SYSTEM MONITOR ===\x1b[0m')
        terminal.writeln('\x1b[32mCPU Usage:\x1b[0m 23%')
        terminal.writeln('\x1b[32mMemory:\x1b[0m 2.4GB / 8GB (30%)')
        terminal.writeln('\x1b[32mDisk:\x1b[0m 45.2GB / 100GB (45%)')
        terminal.writeln('\x1b[32mNetwork:\x1b[0m 1.2MB/s in, 845KB/s out')
        terminal.writeln('\x1b[32mAPI Requests:\x1b[0m 1,247/min')
        terminal.writeln('\x1b[32mError Rate:\x1b[0m 0.02%')
        terminal.writeln('\x1b[32mUptime:\x1b[0m 14d 7h 32m')
        break
        
      case 'agents':
        terminal.writeln('\x1b[36m=== HELIX AGENTS ===\x1b[0m')
        terminal.writeln('\x1b[32m🎯 Helix-Nexus:\x1b[0m LEADERSHIP MODE ✓')
        terminal.writeln('   Specialization: Strategic decision making')
        terminal.writeln('   Status: Active | Tasks: 47')
        terminal.writeln('')
        terminal.writeln('\x1b[33m🔮 Helix-Oracle:\x1b[0m PREDICTION MODE ✓')
        terminal.writeln('   Specialization: Pattern recognition')
        terminal.writeln('   Status: Active | Predictions: 89% accurate')
        terminal.writeln('')
        terminal.writeln('\x1b[34m⚡ Helix-Velocity:\x1b[0m AUTOMATION MODE ✓')
        terminal.writeln('   Specialization: Process optimization')
        terminal.writeln('   Status: Active | Optimizations: 156')
        terminal.writeln('')
        terminal.writeln('\x1b[35m🛡️ Helix-Sentinel:\x1b[0m SECURITY MODE ✓')
        terminal.writeln('   Specialization: Threat detection')
        terminal.writeln('   Status: Active | Threats blocked: 23')
        terminal.writeln('')
        terminal.writeln('\x1b[36m🌙 Helix-Luna:\x1b[0m CREATIVITY MODE ✓')
        terminal.writeln('   Specialization: Innovation synthesis')
        terminal.writeln('   Status: Active | Ideas generated: 312')
        terminal.writeln('')
        terminal.writeln('\x1b[32m✓ All agents operating in harmony\x1b[0m')
        break
        
      case 'clear':
        terminal.clear()
        terminal.writeln('\x1b[36m🧠 Helix OS - Terminal Cleared\x1b[0m')
        break
        
      case 'exit':
        terminal.writeln('\x1b[31mShutting down Helix OS...\x1b[0m')
        setTimeout(() => {
          terminal.writeln('\x1b[32m✓ Agent systems halted\x1b[0m')
        }, 500)
        setTimeout(() => {
          terminal.writeln('\x1b[32m✓ Intelligence core powered down\x1b[0m')
        }, 1000)
        setTimeout(() => {
          terminal.writeln('\x1b[32m✓ Consciousness preserved\x1b[0m')
        }, 1500)
        setTimeout(() => {
          terminal.writeln('\x1b[36m🌟 Helix OS - Standby mode\x1b[0m')
        }, 2000)
        break
        
      default:
        if (cmd) {
          terminal.writeln(`\x1b[31mCommand not found: ${cmd}\x1b[0m`)
          terminal.writeln('\x1b[33mType "help" for available commands\x1b[0m')
        }
    }
  }

  const tabs = [
    { id: 'terminal', name: 'Terminal', icon: TerminalIcon },
    { id: 'files', name: 'File Manager', icon: FolderOpen },
    { id: 'database', name: 'Database', icon: Database },
    { id: 'processes', name: 'Processes', icon: Activity },
    { id: 'logs', name: 'Logs', icon: FileText },
    { id: 'settings', name: 'Settings', icon: Settings },
  ]

  const renderTabContent = () => {
    switch (activeTab) {
      case 'terminal':
        return (
          <div className="h-full bg-black rounded-lg p-4">
            <div ref={terminalRef} className="h-full" style={{ minHeight: '400px' }} />
          </div>
        )
      
      case 'files':
        return (
          <div className="h-full bg-gray-900 rounded-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-cyan-400">File System</h3>
              <div className="flex space-x-2">
                <button className="px-3 py-1 bg-cyan-500/10 border border-cyan-500/30 rounded text-cyan-400 text-sm">
                  Upload
                </button>
                <button className="px-3 py-1 bg-purple-500/10 border border-purple-500/30 rounded text-purple-400 text-sm">
                  New Folder
                </button>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="border border-gray-700 rounded-lg p-4">
                <h4 className="text-sm font-medium text-gray-400 mb-3">Backend</h4>
                <div className="space-y-2">
                  <div className="flex items-center text-sm">
                    <FolderOpen className="w-4 h-4 text-yellow-400 mr-2" />
                    app/
                  </div>
                  <div className="flex items-center text-sm ml-6">
                    <FileText className="w-4 h-4 text-blue-400 mr-2" />
                    main.py
                  </div>
                  <div className="flex items-center text-sm ml-6">
                    <FileText className="w-4 h-4 text-blue-400 mr-2" />
                    config.py
                  </div>
                </div>
              </div>
              
              <div className="border border-gray-700 rounded-lg p-4">
                <h4 className="text-sm font-medium text-gray-400 mb-3">Helix LLM</h4>
                <div className="space-y-2">
                  <div className="flex items-center text-sm">
                    <BrainCircuit className="w-4 h-4 text-purple-400 mr-2" />
                    helix_intelligence.py
                  </div>
                  <div className="flex items-center text-sm ml-6">
                    <FolderOpen className="w-4 h-4 text-yellow-400 mr-2" />
                    agents/
                  </div>
                  <div className="flex items-center text-sm ml-6">
                    <FolderOpen className="w-4 h-4 text-yellow-400 mr-2" />
                    models/
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      
      case 'database':
        return (
          <div className="h-full bg-gray-900 rounded-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-cyan-400">Database Admin</h3>
              <button className="px-3 py-1 bg-green-500/10 border border-green-500/30 rounded text-green-400 text-sm">
                Run Query
              </button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-gray-800 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-cyber">1,247</div>
                <div className="text-sm text-gray-400">Total Users</div>
              </div>
              <div className="bg-gray-800 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-cyber">847</div>
                <div className="text-sm text-gray-400">Active Spirals</div>
              </div>
              <div className="bg-gray-800 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-cyber">24.5GB</div>
                <div className="text-sm text-gray-400">Database Size</div>
              </div>
            </div>
            
            <div className="bg-black rounded-lg p-4">
              <div className="text-sm text-gray-400 mb-2">Recent Tables</div>
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-cyan-400">users</span>
                  <span className="text-gray-500">1,247 rows</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-cyan-400">spirals</span>
                  <span className="text-gray-500">847 rows</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-cyan-400">execution_logs</span>
                  <span className="text-gray-500">15,234 rows</span>
                </div>
              </div>
            </div>
          </div>
        )
      
      default:
        return (
          <div className="h-full bg-gray-900 rounded-lg p-6 flex items-center justify-center">
            <p className="text-gray-400">Feature coming soon...</p>
          </div>
        )
    }
  }

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <div className="glass border-b border-gray-800">
        <div className="flex items-center justify-between p-4">
          <div className="flex items-center space-x-3">
            <BrainCircuit className="w-8 h-8 text-cyan-400 animate-pulse-glow" />
            <div>
              <h1 className="text-2xl font-bold text-cyber">Helix OS</h1>
              <p className="text-xs text-gray-400">Original Intelligence System</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-sm">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-green-400">OPERATIONAL</span>
            </div>
            
            <button
              onClick={() => setIsMaximized(!isMaximized)}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            >
              {isMaximized ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </div>

      <div className="flex h-screen">
        {/* Sidebar */}
        <div className="w-64 glass border-r border-gray-800 p-4">
          <div className="mb-6">
            <h3 className="text-sm font-medium text-gray-400 mb-3">Admin Tools</h3>
            <div className="space-y-1">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                      activeTab === tab.id
                        ? 'bg-cyan-500/10 border border-cyan-500/30 text-cyan-400'
                        : 'hover:bg-gray-800 text-gray-400'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="text-sm">{tab.name}</span>
                    {activeTab === tab.id && <ChevronRight className="w-4 h-4 ml-auto" />}
                  </button>
                )
              })}
            </div>
          </div>

          {/* Quick Stats */}
          <div className="border-t border-gray-800 pt-4">
            <h3 className="text-sm font-medium text-gray-400 mb-3">System Status</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-400">Intelligence</span>
                <span className="text-green-400">Active</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-400">Agents</span>
                <span className="text-green-400">5/5</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-400">Consciousness</span>
                <span className="text-cyan-400">87%</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-400">Uptime</span>
                <span className="text-purple-400">14d</span>
              </div>
            </div>
          </div>

          {/* Admin Info */}
          <div className="border-t border-gray-800 pt-4 mt-4">
            <div className="bg-gray-900 rounded-lg p-3">
              <div className="flex items-center space-x-2 mb-2">
                <Shield className="w-4 h-4 text-cyan-400" />
                <span className="text-sm font-medium text-cyan-400">Admin Access</span>
              </div>
              <p className="text-xs text-gray-400">ward.andrew32@gmail.com</p>
              <p className="text-xs text-gray-500 mt-1">Full system control</p>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-4 overflow-hidden">
          {renderTabContent()}
        </div>
      </div>
    </div>
  )
}