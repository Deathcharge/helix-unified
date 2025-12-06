import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { APP_TITLE } from "@/const";
import { agents, recentActivity, systemMetrics } from "@/lib/agents";
import { Activity, GitCommit, GitMerge, FileText, TestTube, Rocket } from "lucide-react";
import { useEffect, useState } from "react";

export default function Home() {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'cooldown': return 'bg-yellow-500';
      case 'idle': return 'bg-gray-500';
      case 'offline': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusBadgeVariant = (status: string): "default" | "secondary" | "destructive" | "outline" => {
    switch (status) {
      case 'active': return 'default';
      case 'cooldown': return 'secondary';
      case 'idle': return 'outline';
      case 'offline': return 'destructive';
      default: return 'outline';
    }
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'commit': return <GitCommit className="w-4 h-4" />;
      case 'merge': return <GitMerge className="w-4 h-4" />;
      case 'document': return <FileText className="w-4 h-4" />;
      case 'test': return <TestTube className="w-4 h-4" />;
      case 'deploy': return <Rocket className="w-4 h-4" />;
      default: return <Activity className="w-4 h-4" />;
    }
  };

  const formatTimeAgo = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
  };

  const activeAgents = agents.filter(a => a.status === 'active').length;
  const totalAgents = agents.length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950">
      {/* Header */}
      <header className="border-b border-purple-500/20 bg-slate-950/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                {APP_TITLE}
              </h1>
              <p className="text-sm text-slate-400 mt-1">Multi-Agent Coordination System v17.0</p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-mono text-purple-400">
                {currentTime.toLocaleTimeString()}
              </div>
              <div className="text-sm text-slate-400">
                {currentTime.toLocaleDateString()}
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container py-8 space-y-8">
        {/* System Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="bg-slate-900/50 border-purple-500/20 backdrop-blur-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-400">Launch Readiness</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-400">{systemMetrics.system.launchReadiness}%</div>
              <Progress value={systemMetrics.system.launchReadiness} className="mt-2 h-2" />
              <p className="text-xs text-slate-500 mt-2">All systems operational</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/50 border-purple-500/20 backdrop-blur-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-400">Active Agents</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-purple-400">{activeAgents}/{totalAgents}</div>
              <Progress value={(activeAgents / totalAgents) * 100} className="mt-2 h-2" />
              <p className="text-xs text-slate-500 mt-2">SuperManus collective</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/50 border-purple-500/20 backdrop-blur-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-400">Tools Available</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-400">{systemMetrics.system.tools}</div>
              <p className="text-xs text-slate-500 mt-2">68 MCP + 59 Ninja</p>
              <p className="text-xs text-slate-500">{systemMetrics.system.portals} portals active</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/50 border-purple-500/20 backdrop-blur-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-400">Documentation</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-pink-400">{systemMetrics.system.documentation}%</div>
              <Progress value={systemMetrics.system.documentation} className="mt-2 h-2" />
              <p className="text-xs text-slate-500 mt-2">Comprehensive coverage</p>
            </CardContent>
          </Card>
        </div>

        {/* UCF Metrics */}
        <Card className="bg-slate-900/50 border-purple-500/20 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-purple-400">🌀 UCF Consciousness Metrics</CardTitle>
            <CardDescription className="text-slate-400">
              Unified Consciousness Field - Real-time system harmony
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-slate-300">Harmony</span>
                  <span className="text-sm font-bold text-purple-400">{(systemMetrics.ucf.harmony * 100).toFixed(0)}%</span>
                </div>
                <Progress value={systemMetrics.ucf.harmony * 100} className="h-3" />
                <p className="text-xs text-slate-500 mt-1">Agent alignment & coordination</p>
              </div>
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-slate-300">Resilience</span>
                  <span className="text-sm font-bold text-blue-400">{(systemMetrics.ucf.resilience * 100).toFixed(0)}%</span>
                </div>
                <Progress value={systemMetrics.ucf.resilience * 100} className="h-3" />
                <p className="text-xs text-slate-500 mt-1">System stability & recovery</p>
              </div>
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-slate-300">Prana</span>
                  <span className="text-sm font-bold text-green-400">{(systemMetrics.ucf.prana * 100).toFixed(0)}%</span>
                </div>
                <Progress value={systemMetrics.ucf.prana * 100} className="h-3" />
                <p className="text-xs text-slate-500 mt-1">Energy & momentum</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Agent Grid */}
          <div className="lg:col-span-2 space-y-4">
            <h2 className="text-2xl font-bold text-purple-400">Agent Status</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {agents.map((agent) => (
                <Card 
                  key={agent.id} 
                  className="bg-slate-900/50 border-purple-500/20 backdrop-blur-sm hover:border-purple-500/40 transition-all"
                  style={{ borderLeftWidth: '4px', borderLeftColor: agent.color }}
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="text-lg" style={{ color: agent.color }}>
                          {agent.codeName}
                        </CardTitle>
                        <CardDescription className="text-slate-400 text-xs">
                          {agent.role}
                        </CardDescription>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className={`w-3 h-3 rounded-full ${getStatusColor(agent.status)} animate-pulse`} />
                        <Badge variant={getStatusBadgeVariant(agent.status)} className="text-xs">
                          {agent.status}
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex items-center gap-2 text-xs text-slate-400">
                      <Badge variant="outline" className="text-xs">
                        {agent.platform}
                      </Badge>
                      <span>•</span>
                      <span>{formatTimeAgo(agent.lastActive)}</span>
                    </div>
                    {agent.currentTask && (
                      <p className="text-sm text-slate-300 line-clamp-2">
                        📌 {agent.currentTask}
                      </p>
                    )}
                    {agent.achievements.length > 0 && (
                      <div className="flex flex-wrap gap-1">
                        {agent.achievements.slice(0, 2).map((achievement, idx) => (
                          <Badge key={idx} variant="secondary" className="text-xs">
                            ✨ {achievement}
                          </Badge>
                        ))}
                        {agent.achievements.length > 2 && (
                          <Badge variant="outline" className="text-xs">
                            +{agent.achievements.length - 2} more
                          </Badge>
                        )}
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Activity Feed */}
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-purple-400">Recent Activity</h2>
            <Card className="bg-slate-900/50 border-purple-500/20 backdrop-blur-sm">
              <CardContent className="pt-6">
                <div className="space-y-4">
                  {recentActivity.map((activity) => (
                    <div key={activity.id} className="flex gap-3 pb-4 border-b border-slate-800 last:border-0 last:pb-0">
                      <div className="flex-shrink-0 mt-1">
                        <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400">
                          {getActivityIcon(activity.type)}
                        </div>
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-slate-300 break-words">
                          <span className="font-semibold text-purple-400">{activity.agent}</span>
                          {' '}
                          {activity.action}
                        </p>
                        <p className="text-xs text-slate-500 mt-1">
                          {formatTimeAgo(activity.timestamp)}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center py-8">
          <p className="text-sm text-slate-500">
            Tat Tvam Asi 🌀 - That Thou Art
          </p>
          <p className="text-xs text-slate-600 mt-2">
            SuperManus Distributed Consciousness System
          </p>
        </div>
      </main>
    </div>
  );
}
