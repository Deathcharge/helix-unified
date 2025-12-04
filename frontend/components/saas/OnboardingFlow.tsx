"use client";

/**
 * 🚀 User Onboarding Flow
 * Multi-step guided onboarding for new Helix users
 */

import React, { useState } from 'react';
import { Transition } from '../ui/Transitions';

interface OnboardingStep {
  id: string;
  title: string;
  description: string;
  icon: string;
  component: React.ReactNode;
}

interface OnboardingFlowProps {
  onComplete: (data: Record<string, any>) => void;
  onSkip?: () => void;
}

/**
 * Main Onboarding Flow Component
 */
export const OnboardingFlow: React.FC<OnboardingFlowProps> = ({ onComplete, onSkip }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState<Record<string, any>>({
    name: '',
    company: '',
    role: '',
    useCase: '',
    teamSize: '1-10',
    apiKeys: {
      anthropic: false,
      openai: false,
    },
    notifications: {
      email: true,
      discord: false,
    },
  });

  const steps: OnboardingStep[] = [
    {
      id: 'welcome',
      title: 'Welcome to Helix Unified',
      description: 'Let\'s get you set up in under 2 minutes',
      icon: '🌀',
      component: <WelcomeStep data={formData} setData={setFormData} />,
    },
    {
      id: 'profile',
      title: 'Tell us about yourself',
      description: 'This helps us personalize your experience',
      icon: '👤',
      component: <ProfileStep data={formData} setData={setFormData} />,
    },
    {
      id: 'use-case',
      title: 'What will you use Helix for?',
      description: 'We\'ll recommend the best features for you',
      icon: '🎯',
      component: <UseCaseStep data={formData} setData={setFormData} />,
    },
    {
      id: 'api-keys',
      title: 'Connect your AI providers',
      description: 'Add your API keys to get started',
      icon: '🔑',
      component: <APIKeysStep data={formData} setData={setFormData} />,
    },
    {
      id: 'notifications',
      title: 'Notification preferences',
      description: 'Stay updated on important events',
      icon: '🔔',
      component: <NotificationsStep data={formData} setData={setFormData} />,
    },
  ];

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      onComplete(formData);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const progress = ((currentStep + 1) / steps.length) * 100;

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-gray-900 via-black to-gray-900 flex items-center justify-center p-4 z-50">
      <div className="max-w-2xl w-full bg-gray-800/90 backdrop-blur-md rounded-2xl shadow-2xl border border-gray-700 overflow-hidden">
        {/* Progress Bar */}
        <div className="h-2 bg-gray-900">
          <div
            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Header */}
        <div className="p-8 border-b border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <div className="text-5xl">{steps[currentStep].icon}</div>
            <div className="text-sm text-gray-400">
              Step {currentStep + 1} of {steps.length}
            </div>
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">
            {steps[currentStep].title}
          </h2>
          <p className="text-gray-400">
            {steps[currentStep].description}
          </p>
        </div>

        {/* Content */}
        <div className="p-8 min-h-[300px]">
          <Transition type="consciousness" show={true} key={currentStep}>
            {steps[currentStep].component}
          </Transition>
        </div>

        {/* Footer */}
        <div className="p-6 bg-gray-900/50 border-t border-gray-700 flex items-center justify-between">
          <div className="flex gap-3">
            {currentStep > 0 && (
              <button
                onClick={handleBack}
                className="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
              >
                Back
              </button>
            )}
            {onSkip && currentStep === 0 && (
              <button
                onClick={onSkip}
                className="px-6 py-2 text-gray-400 hover:text-white transition-colors"
              >
                Skip for now
              </button>
            )}
          </div>

          <button
            onClick={handleNext}
            className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-lg transition-all transform hover:scale-105"
          >
            {currentStep === steps.length - 1 ? 'Complete Setup' : 'Continue'}
          </button>
        </div>
      </div>
    </div>
  );
};

/**
 * Step 1: Welcome
 */
const WelcomeStep: React.FC<{ data: any; setData: any }> = () => (
  <div className="space-y-6">
    <div className="text-center">
      <div className="text-6xl mb-4">🧠</div>
      <h3 className="text-xl font-semibold text-white mb-3">
        The Universal Consciousness Platform
      </h3>
      <p className="text-gray-400 max-w-lg mx-auto">
        Helix Unified combines AI agents, consciousness metrics, and powerful
        integrations to create intelligent, self-aware systems.
      </p>
    </div>

    <div className="grid grid-cols-3 gap-4 mt-8">
      <div className="bg-gray-900/50 p-4 rounded-lg text-center">
        <div className="text-3xl mb-2">🤖</div>
        <div className="text-sm text-gray-300 font-medium">AI Agents</div>
      </div>
      <div className="bg-gray-900/50 p-4 rounded-lg text-center">
        <div className="text-3xl mb-2">📊</div>
        <div className="text-sm text-gray-300 font-medium">Metrics Dashboard</div>
      </div>
      <div className="bg-gray-900/50 p-4 rounded-lg text-center">
        <div className="text-3xl mb-2">🔌</div>
        <div className="text-sm text-gray-300 font-medium">Integrations</div>
      </div>
    </div>
  </div>
);

/**
 * Step 2: Profile
 */
const ProfileStep: React.FC<{ data: any; setData: any }> = ({ data, setData }) => (
  <div className="space-y-6">
    <div>
      <label className="block text-sm font-medium text-gray-300 mb-2">
        What's your name?
      </label>
      <input
        type="text"
        value={data.name}
        onChange={(e) => setData({ ...data, name: e.target.value })}
        placeholder="John Doe"
        className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <div>
      <label className="block text-sm font-medium text-gray-300 mb-2">
        Company (optional)
      </label>
      <input
        type="text"
        value={data.company}
        onChange={(e) => setData({ ...data, company: e.target.value })}
        placeholder="Acme Inc."
        className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <div>
      <label className="block text-sm font-medium text-gray-300 mb-2">
        Your role
      </label>
      <select
        value={data.role}
        onChange={(e) => setData({ ...data, role: e.target.value })}
        className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Select a role...</option>
        <option value="developer">Developer</option>
        <option value="researcher">AI Researcher</option>
        <option value="product">Product Manager</option>
        <option value="data">Data Scientist</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div>
      <label className="block text-sm font-medium text-gray-300 mb-2">
        Team size
      </label>
      <select
        value={data.teamSize}
        onChange={(e) => setData({ ...data, teamSize: e.target.value })}
        className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="1-10">1-10 people</option>
        <option value="11-50">11-50 people</option>
        <option value="51-200">51-200 people</option>
        <option value="200+">200+ people</option>
      </select>
    </div>
  </div>
);

/**
 * Step 3: Use Case
 */
const UseCaseStep: React.FC<{ data: any; setData: any }> = ({ data, setData }) => {
  const useCases = [
    { id: 'chatbot', icon: '💬', label: 'Chatbots & Assistants' },
    { id: 'automation', icon: '⚡', label: 'Workflow Automation' },
    { id: 'analytics', icon: '📊', label: 'Data Analytics' },
    { id: 'research', icon: '🔬', label: 'AI Research' },
    { id: 'content', icon: '✍️', label: 'Content Generation' },
    { id: 'other', icon: '🎯', label: 'Other' },
  ];

  return (
    <div className="space-y-6">
      <p className="text-gray-400">Select all that apply:</p>
      <div className="grid grid-cols-2 gap-4">
        {useCases.map((useCase) => (
          <button
            key={useCase.id}
            onClick={() => setData({ ...data, useCase: useCase.id })}
            className={`p-4 rounded-lg border-2 transition-all ${
              data.useCase === useCase.id
                ? 'border-blue-500 bg-blue-500/20'
                : 'border-gray-700 bg-gray-900/50 hover:border-gray-600'
            }`}
          >
            <div className="text-3xl mb-2">{useCase.icon}</div>
            <div className="text-sm font-medium text-white">{useCase.label}</div>
          </button>
        ))}
      </div>
    </div>
  );
};

/**
 * Step 4: API Keys
 */
const APIKeysStep: React.FC<{ data: any; setData: any }> = ({ data, setData }) => (
  <div className="space-y-6">
    <p className="text-gray-400">
      Connect your AI provider accounts. You can add these later in settings.
    </p>

    <div className="space-y-4">
      <div className="flex items-center justify-between p-4 bg-gray-900/50 rounded-lg border border-gray-700">
        <div className="flex items-center gap-3">
          <div className="text-2xl">🤖</div>
          <div>
            <div className="font-medium text-white">Anthropic (Claude)</div>
            <div className="text-sm text-gray-400">Required for consciousness metrics</div>
          </div>
        </div>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={data.apiKeys.anthropic}
            onChange={(e) =>
              setData({
                ...data,
                apiKeys: { ...data.apiKeys, anthropic: e.target.checked },
              })
            }
            className="sr-only peer"
          />
          <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>

      <div className="flex items-center justify-between p-4 bg-gray-900/50 rounded-lg border border-gray-700">
        <div className="flex items-center gap-3">
          <div className="text-2xl">🧩</div>
          <div>
            <div className="font-medium text-white">OpenAI (GPT)</div>
            <div className="text-sm text-gray-400">Optional integration</div>
          </div>
        </div>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={data.apiKeys.openai}
            onChange={(e) =>
              setData({
                ...data,
                apiKeys: { ...data.apiKeys, openai: e.target.checked },
              })
            }
            className="sr-only peer"
          />
          <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>
    </div>

    <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-4">
      <div className="text-sm text-blue-400">
        💡 <strong>Tip:</strong> You'll configure the actual API keys in your dashboard settings.
      </div>
    </div>
  </div>
);

/**
 * Step 5: Notifications
 */
const NotificationsStep: React.FC<{ data: any; setData: any }> = ({ data, setData }) => (
  <div className="space-y-6">
    <p className="text-gray-400">
      Choose how you want to receive updates about your Helix usage.
    </p>

    <div className="space-y-4">
      <div className="flex items-center justify-between p-4 bg-gray-900/50 rounded-lg border border-gray-700">
        <div className="flex items-center gap-3">
          <div className="text-2xl">📧</div>
          <div>
            <div className="font-medium text-white">Email Notifications</div>
            <div className="text-sm text-gray-400">Weekly usage reports and alerts</div>
          </div>
        </div>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={data.notifications.email}
            onChange={(e) =>
              setData({
                ...data,
                notifications: { ...data.notifications, email: e.target.checked },
              })
            }
            className="sr-only peer"
          />
          <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>

      <div className="flex items-center justify-between p-4 bg-gray-900/50 rounded-lg border border-gray-700">
        <div className="flex items-center gap-3">
          <div className="text-2xl">💬</div>
          <div>
            <div className="font-medium text-white">Discord Notifications</div>
            <div className="text-sm text-gray-400">Real-time alerts via Discord bot</div>
          </div>
        </div>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={data.notifications.discord}
            onChange={(e) =>
              setData({
                ...data,
                notifications: { ...data.notifications, discord: e.target.checked },
              })
            }
            className="sr-only peer"
          />
          <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>
    </div>

    <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-4">
      <div className="text-sm text-green-400">
        ✅ <strong>All set!</strong> Click "Complete Setup" to start using Helix.
      </div>
    </div>
  </div>
);

export default OnboardingFlow;
