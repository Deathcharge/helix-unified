import React from 'react';
import { Heart, Zap, Users, Shield, Star, Brain, MessageCircle } from 'lucide-react';

const iconMap = {
  heart: Heart,
  zap: Zap,
  users: Users,
  shield: Shield,
  star: Star,
  brain: Brain,
  message: MessageCircle
};

const colorMap = {
  pink: 'from-pink-500 to-purple-500',
  cyan: 'from-cyan-500 to-blue-500',
  green: 'from-green-500 to-emerald-500',
  yellow: 'from-yellow-500 to-orange-500',
  purple: 'from-purple-500 to-indigo-500',
  red: 'from-red-500 to-orange-500',
  gray: 'from-gray-600 to-gray-800'
};

const AgentCard = ({ 
  agent,
  onClick,
  size = 'medium',
  showStats = true,
  interactive = true 
}) => {
  const Icon = iconMap[agent.icon] || Users;
  const colorClass = colorMap[agent.color] || colorMap.cyan;
  
  const cardClasses = interactive 
    ? 'agent-card rounded-lg card-hover cursor-pointer transition-all duration-300 hover:scale-105'
    : 'agent-card rounded-lg';

  return (
    <div 
      className={`${cardClasses} bg-gray-800 p-4`}
      onClick={interactive ? onClick : undefined}
    >
      <div className="flex items-center mb-3">
        <div className={`w-10 h-10 bg-gradient-to-r ${colorClass} rounded-full flex items-center justify-center mr-3`}>
          <Icon className="w-5 h-5 text-white" />
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-white">{agent.name}</h4>
          <p className="text-xs text-gray-400">{agent.role}</p>
        </div>
        {agent.status && (
          <span className={`text-xs px-2 py-1 rounded-full ${
            agent.status === 'active' 
              ? 'bg-green-500/20 text-green-400' 
              : 'bg-gray-500/20 text-gray-400'
          }`}>
            {agent.status}
          </span>
        )}
      </div>
      
      {showStats && agent.stats && (
        <div className="space-y-2">
          {Object.entries(agent.stats).map(([key, value]) => (
            <div key={key} className="flex items-center justify-between text-sm">
              <span className="text-gray-400 capitalize">{key.replace(/_/g, ' ')}</span>
              <span className="text-cyan-400 font-semibold">{value}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AgentCard;