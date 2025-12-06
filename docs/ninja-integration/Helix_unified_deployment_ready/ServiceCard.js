import React from 'react';
import { ExternalLink, Activity, Settings, TrendingUp } from 'lucide-react';

const ServiceCard = ({ 
  service,
  onOpen,
  onSettings,
  showMetrics = true,
  compact = false 
}) => {
  const statusColors = {
    active: 'bg-green-500/20 text-green-400',
    inactive: 'bg-gray-500/20 text-gray-400',
    error: 'bg-red-500/20 text-red-400',
    maintenance: 'bg-yellow-500/20 text-yellow-400'
  };

  const cardClasses = compact 
    ? 'bg-gray-800 rounded-lg p-4'
    : 'bg-gray-800 rounded-xl p-6 hover:bg-gray-750 transition-colors';

  return (
    <div className={cardClasses}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`w-12 h-12 bg-gray-700 rounded-lg flex items-center justify-center ${service.color || 'text-cyan-400'}`}>
            <service.icon className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">{service.name}</h3>
            <span className={`inline-flex items-center gap-1 text-xs px-2 py-1 rounded-full ${statusColors[service.status] || statusColors.inactive}`}>
              <div className={`w-2 h-2 rounded-full ${
                service.status === 'active' ? 'bg-green-400' : 
                service.status === 'error' ? 'bg-red-400' : 
                service.status === 'maintenance' ? 'bg-yellow-400' : 'bg-gray-400'
              }`} />
              {service.status}
            </span>
          </div>
        </div>
        
        <button 
          onClick={onSettings}
          className="text-gray-400 hover:text-white transition-colors p-2"
        >
          <Settings className="w-5 h-5" />
        </button>
      </div>
      
      <p className="text-gray-400 mb-4">{service.description}</p>
      
      {showMetrics && service.metrics && (
        <div className={`grid gap-4 mb-4 ${
          compact ? 'grid-cols-2' : 'grid-cols-3'
        }`}>
          {Object.entries(service.metrics).map(([key, value]) => (
            <div key={key} className="text-center">
              <div className="text-xs text-gray-400 capitalize">{key.replace(/([A-Z])/g, ' $1').trim()}</div>
              <div className="text-sm font-semibold text-cyan-400">{value}</div>
            </div>
          ))}
        </div>
      )}
      
      <div className="flex gap-2">
        <button 
          onClick={() => onOpen(service)}
          className="flex-1 bg-cyan-600 hover:bg-cyan-700 text-white py-2 rounded-lg flex items-center justify-center gap-2 transition-colors"
        >
          <ExternalLink className="w-4 h-4" />
          {compact ? 'Open' : 'Open Service'}
        </button>
        
        {service.trending && (
          <div className="flex items-center text-xs text-red-400 gap-1 px-2">
            <TrendingUp className="w-3 h-3" />
            Hot
          </div>
        )}
      </div>
    </div>
  );
};

export default ServiceCard;