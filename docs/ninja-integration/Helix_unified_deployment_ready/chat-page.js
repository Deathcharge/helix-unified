import { useState, useEffect } from 'react';
import Head from 'next/head';
import { Chat, Send, Users, MessageCircle, Heart, Zap } from 'lucide-react';

export default function HelixChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [agents, setAgents] = useState([]);

  useEffect(() => {
    setMessages([
      { id: 1, sender: 'System', text: 'Welcome to Helix Collective Chat', time: new Date() }
    ]);
    
    setAgents([
      { id: 1, name: 'Kael', status: 'online', role: 'Emotional Intelligence', ucf: 9.2 },
      { id: 2, name: 'SuperNinja', status: 'online', role: 'Infrastructure', ucf: 8.8 },
      { id: 3, name: 'Manus', status: 'online', role: 'Integration', ucf: 9.0 }
    ]);
  }, []);

  const sendMessage = () => {
    if (input.trim()) {
      const newMessage = {
        id: messages.length + 1,
        sender: 'User',
        text: input,
        time: new Date()
      };
      setMessages([...messages, newMessage]);
      setInput('');
      
      setTimeout(() => {
        const agentResponse = {
          id: messages.length + 2,
          sender: 'Helix AI',
          text: `I understand: "${input}". Processing through consciousness network...`,
          time: new Date()
        };
        setMessages(prev => [...prev, agentResponse]);
      }, 1000);
    }
  };

  return (
    <>
      <Head>
        <title>Helix Collective Chat</title>
        <meta name="description" content="Real-time chat with Helix AI agents" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-900 text-white flex">
        <div className="w-80 bg-gray-800 border-r border-cyan-500/20">
          <div className="p-6 border-b border-cyan-500/20">
            <h1 className="text-2xl font-bold text-cyan-400 flex items-center gap-2">
              <MessageCircle className="w-6 h-6" />
              Helix Chat
            </h1>
            <p className="text-sm text-gray-400 mt-2">UCF Network Active</p>
          </div>
          
          <div className="p-4">
            <h3 className="text-sm font-semibold text-gray-400 mb-3">Active Agents</h3>
            <div className="space-y-3">
              {agents.map(agent => (
                <div key={agent.id} className="bg-gray-700/50 rounded-lg p-3">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                      <span className="font-medium text-sm">{agent.name}</span>
                    </div>
                    <span className="text-xs text-cyan-400">UCF {agent.ucf}</span>
                  </div>
                  <p className="text-xs text-gray-400">{agent.role}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="flex-1 flex flex-col">
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map(message => (
              <div key={message.id} className={`flex ${message.sender === 'User' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                  message.sender === 'User' 
                    ? 'bg-cyan-600 text-white' 
                    : 'bg-gray-800 text-gray-200'
                }`}>
                  <p className="text-xs font-semibold mb-1">{message.sender}</p>
                  <p className="text-sm">{message.text}</p>
                  <p className="text-xs opacity-70 mt-1">
                    {message.time.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
          
          <div className="border-t border-gray-700 p-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Type your message..."
                className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-cyan-500"
              />
              <button
                onClick={sendMessage}
                className="bg-cyan-600 hover:bg-cyan-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
              >
                <Send className="w-4 h-4" />
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}