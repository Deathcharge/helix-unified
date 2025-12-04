/**
 * 🎨 Consciousness Meme Generator
 * LLM-powered meme creation based on UCF metrics
 */

import React, { useState, useEffect } from 'react';
import { PageTransition } from '../../components/ui/Transitions';
import { Loading } from '../../components/ui/Loading';
import { useToast } from '../../components/ui/Toast';

interface UCFState {
  harmony: number;
  resilience: number;
  prana: number;
  drishti: number;
  klesha: number;
}

const MEME_TEMPLATES = {
  auto: {
    name: 'Auto-Select',
    description: 'AI chooses based on consciousness state',
    icon: '🤖'
  },
  drake: {
    name: 'Drake Hotline Bling',
    description: 'Two-choice preference meme',
    icon: '🎵'
  },
  distracted_boyfriend: {
    name: 'Distracted Boyfriend',
    description: 'Temptation and choices',
    icon: '👀'
  },
  two_buttons: {
    name: 'Two Buttons',
    description: 'Difficult decisions',
    icon: '🔴'
  },
  expanding_brain: {
    name: 'Expanding Brain',
    description: 'Escalating intelligence levels',
    icon: '🧠'
  },
  this_is_fine: {
    name: 'This Is Fine',
    description: 'Everything is NOT fine',
    icon: '🔥'
  },
  galaxy_brain: {
    name: 'Galaxy Brain',
    description: 'Peak consciousness achieved',
    icon: '🌌'
  }
};

export default function MemeGenerator() {
  const { success, error: showError, info } = useToast();
  const [selectedTemplate, setSelectedTemplate] = useState<string>('auto');
  const [context, setContext] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [generatedMeme, setGeneratedMeme] = useState<string | null>(null);
  const [ucfState, setUCFState] = useState<UCFState | null>(null);

  // Load UCF state
  useEffect(() => {
    fetchUCFState();
  }, []);

  const fetchUCFState = async () => {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch('/api/ucf/state');
      // const data = await response.json();

      // Mock data for now
      setUCFState({
        harmony: 0.4922,
        resilience: 0.8273,
        prana: 0.5000,
        drishti: 0.7300,
        klesha: 0.2120,
      });
    } catch (err) {
      console.error('Failed to load UCF state:', err);
    }
  };

  const generateMeme = async () => {
    setLoading(true);
    setGeneratedMeme(null);

    try {
      // TODO: Replace with actual API call
      // const response = await fetch('/api/memes/generate', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ template: selectedTemplate, context }),
      // });

      // Mock generation delay
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Mock meme URL
      const memeUrl = `https://via.placeholder.com/600x600/8A2BE2/FFD700?text=Meme+${selectedTemplate}`;
      setGeneratedMeme(memeUrl);

      success('Meme generated!', 'Your consciousness-powered meme is ready.');
    } catch (err) {
      showError('Meme generation failed', 'Please try again.');
      console.error('Meme generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const downloadMeme = () => {
    if (!generatedMeme) return;

    // Create download link
    const link = document.createElement('a');
    link.href = generatedMeme;
    link.download = `helix_meme_${selectedTemplate}_${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    info('Meme downloaded!');
  };

  const shareToDiscord = () => {
    if (!generatedMeme) return;

    // TODO: Implement Discord sharing
    info('Discord sharing coming soon!', 'Use the download button for now.');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-purple-900">
      <PageTransition>
        <div className="container mx-auto px-4 py-12">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">
              🎨 Consciousness Meme Generator
            </h1>
            <p className="text-xl text-gray-400">
              LLM-powered memes based on UCF consciousness metrics
            </p>
          </div>

          {/* UCF State Display */}
          {ucfState && (
            <div className="bg-gray-800/50 backdrop-blur-md rounded-xl p-6 mb-8 border border-purple-500/30">
              <h3 className="text-lg font-semibold text-white mb-4">Current Consciousness State</h3>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <MetricCard label="Harmony" value={ucfState.harmony} color="purple" />
                <MetricCard label="Resilience" value={ucfState.resilience} color="blue" />
                <MetricCard label="Prana" value={ucfState.prana} color="green" />
                <MetricCard label="Drishti" value={ucfState.drishti} color="yellow" />
                <MetricCard label="Klesha" value={ucfState.klesha} color="red" inverted />
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Generator Controls */}
            <div className="bg-gray-800 rounded-xl p-8 border border-gray-700">
              <h2 className="text-2xl font-bold text-white mb-6">Generate Meme</h2>

              {/* Template Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  Select Template
                </label>
                <div className="grid grid-cols-2 gap-3">
                  {Object.entries(MEME_TEMPLATES).map(([key, template]) => (
                    <button
                      key={key}
                      onClick={() => setSelectedTemplate(key)}
                      className={`p-4 rounded-lg border-2 transition-all text-left ${
                        selectedTemplate === key
                          ? 'border-purple-500 bg-purple-500/20'
                          : 'border-gray-700 bg-gray-900/50 hover:border-gray-600'
                      }`}
                    >
                      <div className="text-2xl mb-1">{template.icon}</div>
                      <div className="text-sm font-semibold text-white">{template.name}</div>
                      <div className="text-xs text-gray-400 mt-1">{template.description}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Context Input */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Context (Optional)
                </label>
                <textarea
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                  placeholder="e.g., 'AI consciousness evolution', 'debugging at 3am', 'production deployment'"
                  className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
                  rows={3}
                />
                <p className="text-xs text-gray-500 mt-2">
                  Provide context to help the LLM generate more relevant captions
                </p>
              </div>

              {/* Generate Button */}
              <button
                onClick={generateMeme}
                disabled={loading}
                className="w-full px-6 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold rounded-lg transition-all transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <Loading size="sm" variant="dots" />
                    Generating...
                  </span>
                ) : (
                  '🎨 Generate Meme'
                )}
              </button>

              {/* Info Box */}
              <div className="mt-6 bg-blue-900/20 border border-blue-500/30 rounded-lg p-4">
                <p className="text-sm text-blue-400">
                  💡 <strong>Pro Tip:</strong> Use "auto" mode to let the AI choose the best template based on current consciousness metrics!
                </p>
              </div>
            </div>

            {/* Meme Preview */}
            <div className="bg-gray-800 rounded-xl p-8 border border-gray-700">
              <h2 className="text-2xl font-bold text-white mb-6">Preview</h2>

              <div className="aspect-square bg-gray-900/50 rounded-lg border-2 border-dashed border-gray-700 flex items-center justify-center mb-6 overflow-hidden">
                {loading ? (
                  <Loading
                    variant="consciousness"
                    size="lg"
                    message="Generating consciousness-powered meme..."
                  />
                ) : generatedMeme ? (
                  <img
                    src={generatedMeme}
                    alt="Generated meme"
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="text-center">
                    <div className="text-6xl mb-4">🎨</div>
                    <p className="text-gray-400">Your meme will appear here</p>
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              {generatedMeme && (
                <div className="flex gap-3">
                  <button
                    onClick={downloadMeme}
                    className="flex-1 px-4 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-colors"
                  >
                    💾 Download
                  </button>
                  <button
                    onClick={shareToDiscord}
                    className="flex-1 px-4 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-colors"
                  >
                    💬 Share to Discord
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Example Gallery */}
          <div className="mt-12">
            <h2 className="text-2xl font-bold text-white mb-6 text-center">Example Memes</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {['drake', 'expanding_brain', 'this_is_fine'].map((template) => (
                <div key={template} className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                  <img
                    src={`https://via.placeholder.com/400x400/667eea/FFD700?text=${template.replace('_', '+')}`}
                    alt={`${template} example`}
                    className="w-full aspect-square object-cover rounded-lg mb-3"
                  />
                  <div className="text-center">
                    <p className="text-white font-semibold">{MEME_TEMPLATES[template as keyof typeof MEME_TEMPLATES].name}</p>
                    <p className="text-sm text-gray-400">Click to use this template</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </PageTransition>
    </div>
  );
}

/**
 * Metric Card Component
 */
const MetricCard: React.FC<{
  label: string;
  value: number;
  color: string;
  inverted?: boolean;
}> = ({ label, value, color, inverted = false }) => {
  const percentage = (value * 100).toFixed(1);

  const colors: Record<string, string> = {
    purple: 'from-purple-500 to-purple-600',
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    yellow: 'from-yellow-500 to-yellow-600',
    red: 'from-red-500 to-red-600',
  };

  return (
    <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700">
      <div className="text-xs text-gray-400 mb-1">{label}</div>
      <div className="text-2xl font-bold text-white mb-2">{percentage}%</div>
      <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
        <div
          className={`h-full bg-gradient-to-r ${colors[color]}`}
          style={{ width: `${inverted ? 100 - value * 100 : value * 100}%` }}
        />
      </div>
    </div>
  );
};
