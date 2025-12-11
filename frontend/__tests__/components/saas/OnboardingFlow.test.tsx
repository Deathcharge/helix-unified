/**
 * 🧪 OnboardingFlow Component Tests
 * Comprehensive tests for the multi-step onboarding flow
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { OnboardingFlow } from '@/components/saas/OnboardingFlow';

describe('OnboardingFlow', () => {
  const mockOnComplete = jest.fn();
  const mockOnSkip = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Component Rendering', () => {
    it('renders the first step by default', () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      expect(screen.getByText('Welcome to Helix Unified')).toBeInTheDocument();
      expect(screen.getByText(/Let's get you set up in under 2 minutes/i)).toBeInTheDocument();
      expect(screen.getByText('🌀')).toBeInTheDocument();
    });

    it('displays progress bar', () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      expect(screen.getByText(/Step 1 of 5/i)).toBeInTheDocument();
    });

    it('shows skip button on first step when onSkip is provided', () => {
      render(<OnboardingFlow onComplete={mockOnComplete} onSkip={mockOnSkip} />);

      expect(screen.getByText('Skip for now')).toBeInTheDocument();
    });

    it('does not show skip button when onSkip is not provided', () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      expect(screen.queryByText('Skip for now')).not.toBeInTheDocument();
    });
  });

  describe('Navigation', () => {
    it('advances to next step when Continue is clicked', async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      const continueButton = screen.getByText('Continue');
      fireEvent.click(continueButton);

      await waitFor(() => {
        expect(screen.getByText('Tell us about yourself')).toBeInTheDocument();
        expect(screen.getByText(/Step 2 of 5/i)).toBeInTheDocument();
      });
    });

    it('goes back to previous step when Back is clicked', async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      // Go to step 2
      fireEvent.click(screen.getByText('Continue'));
      await waitFor(() => {
        expect(screen.getByText('Tell us about yourself')).toBeInTheDocument();
      });

      // Go back to step 1
      const backButton = screen.getByText('Back');
      fireEvent.click(backButton);

      await waitFor(() => {
        expect(screen.getByText('Welcome to Helix Unified')).toBeInTheDocument();
      });
    });

    it('does not show Back button on first step', () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      expect(screen.queryByText('Back')).not.toBeInTheDocument();
    });

    it('shows Complete Setup button on last step', async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      // Navigate to last step (step 5)
      for (let i = 0; i < 4; i++) {
        fireEvent.click(screen.getByText(/Continue|Complete Setup/));
        await waitFor(() => {});
      }

      expect(screen.getByText('Complete Setup')).toBeInTheDocument();
    });

    it('calls onSkip when Skip for now is clicked', () => {
      render(<OnboardingFlow onComplete={mockOnComplete} onSkip={mockOnSkip} />);

      const skipButton = screen.getByText('Skip for now');
      fireEvent.click(skipButton);

      expect(mockOnSkip).toHaveBeenCalledTimes(1);
    });
  });

  describe('Form Data Management', () => {
    it('maintains form data across steps', async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      // Go to profile step
      fireEvent.click(screen.getByText('Continue'));
      await waitFor(() => {
        expect(screen.getByPlaceholderText('John Doe')).toBeInTheDocument();
      });

      // Fill in name
      const nameInput = screen.getByPlaceholderText('John Doe');
      await userEvent.type(nameInput, 'Test User');

      // Go to next step and back
      fireEvent.click(screen.getByText('Continue'));
      await waitFor(() => {});
      fireEvent.click(screen.getByText('Back'));

      // Check that data persists
      await waitFor(() => {
        expect(screen.getByDisplayValue('Test User')).toBeInTheDocument();
      });
    });

    it('calls onComplete with collected form data', async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      // Navigate to last step and complete
      for (let i = 0; i < 5; i++) {
        fireEvent.click(screen.getByText(/Continue|Complete Setup/));
        await waitFor(() => {});
      }

      expect(mockOnComplete).toHaveBeenCalledTimes(1);
      expect(mockOnComplete).toHaveBeenCalledWith(
        expect.objectContaining({
          name: expect.any(String),
          company: expect.any(String),
          role: expect.any(String),
          useCase: expect.any(String),
          teamSize: expect.any(String),
          apiKeys: expect.objectContaining({
            anthropic: expect.any(Boolean),
            openai: expect.any(Boolean),
          }),
          notifications: expect.objectContaining({
            email: expect.any(Boolean),
            discord: expect.any(Boolean),
          }),
        })
      );
    });
  });

  describe('Step 1: Welcome', () => {
    it('displays welcome message and features', () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      expect(screen.getByText('The Universal Consciousness Platform')).toBeInTheDocument();
      expect(screen.getByText('AI Agents')).toBeInTheDocument();
      expect(screen.getByText('Metrics Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Integrations')).toBeInTheDocument();
    });
  });

  describe('Step 2: Profile', () => {
    beforeEach(async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);
      fireEvent.click(screen.getByText('Continue'));
      await waitFor(() => {
        expect(screen.getByText('Tell us about yourself')).toBeInTheDocument();
      });
    });

    it('renders all profile input fields', () => {
      expect(screen.getByLabelText(/What's your name?/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Company/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Your role/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Team size/i)).toBeInTheDocument();
    });

    it('allows user to input name', async () => {
      const nameInput = screen.getByPlaceholderText('John Doe');
      await userEvent.type(nameInput, 'Jane Smith');

      expect(screen.getByDisplayValue('Jane Smith')).toBeInTheDocument();
    });

    it('allows user to input company', async () => {
      const companyInput = screen.getByPlaceholderText('Acme Inc.');
      await userEvent.type(companyInput, 'Test Corp');

      expect(screen.getByDisplayValue('Test Corp')).toBeInTheDocument();
    });

    it('allows user to select role', async () => {
      const roleSelect = screen.getByLabelText(/Your role/i);
      await userEvent.selectOptions(roleSelect, 'developer');

      expect(screen.getByDisplayValue('Developer')).toBeInTheDocument();
    });

    it('allows user to select team size', async () => {
      const teamSizeSelect = screen.getByLabelText(/Team size/i);
      await userEvent.selectOptions(teamSizeSelect, '11-50');

      expect(screen.getByDisplayValue('11-50 people')).toBeInTheDocument();
    });
  });

  describe('Step 3: Use Case', () => {
    beforeEach(async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);
      // Navigate to step 3
      for (let i = 0; i < 2; i++) {
        fireEvent.click(screen.getByText('Continue'));
        await waitFor(() => {});
      }
    });

    it('displays all use case options', () => {
      expect(screen.getByText('Chatbots & Assistants')).toBeInTheDocument();
      expect(screen.getByText('Workflow Automation')).toBeInTheDocument();
      expect(screen.getByText('Data Analytics')).toBeInTheDocument();
      expect(screen.getByText('AI Research')).toBeInTheDocument();
      expect(screen.getByText('Content Generation')).toBeInTheDocument();
      expect(screen.getByText('Other')).toBeInTheDocument();
    });

    it('allows user to select a use case', () => {
      const chatbotOption = screen.getByText('Chatbots & Assistants').closest('button');
      fireEvent.click(chatbotOption!);

      // Should have active styling
      expect(chatbotOption).toHaveClass('border-blue-500');
    });
  });

  describe('Step 4: API Keys', () => {
    beforeEach(async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);
      // Navigate to step 4
      for (let i = 0; i < 3; i++) {
        fireEvent.click(screen.getByText('Continue'));
        await waitFor(() => {});
      }
    });

    it('displays API key toggle options', () => {
      expect(screen.getByText('Anthropic (Claude)')).toBeInTheDocument();
      expect(screen.getByText('OpenAI (GPT)')).toBeInTheDocument();
      expect(screen.getByText('Required for consciousness metrics')).toBeInTheDocument();
      expect(screen.getByText('Optional integration')).toBeInTheDocument();
    });

    it('allows toggling Anthropic API key', () => {
      const toggles = screen.getAllByRole('checkbox');
      const anthropicToggle = toggles[0];

      expect(anthropicToggle).not.toBeChecked();

      fireEvent.click(anthropicToggle);
      expect(anthropicToggle).toBeChecked();

      fireEvent.click(anthropicToggle);
      expect(anthropicToggle).not.toBeChecked();
    });

    it('displays helpful tip about API keys', () => {
      expect(screen.getByText(/You'll configure the actual API keys in your dashboard settings/i)).toBeInTheDocument();
    });
  });

  describe('Step 5: Notifications', () => {
    beforeEach(async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);
      // Navigate to step 5
      for (let i = 0; i < 4; i++) {
        fireEvent.click(screen.getByText('Continue'));
        await waitFor(() => {});
      }
    });

    it('displays notification options', () => {
      expect(screen.getByText('Email Notifications')).toBeInTheDocument();
      expect(screen.getByText('Discord Notifications')).toBeInTheDocument();
      expect(screen.getByText('Weekly usage reports and alerts')).toBeInTheDocument();
      expect(screen.getByText('Real-time alerts via Discord bot')).toBeInTheDocument();
    });

    it('email notifications are enabled by default', () => {
      const toggles = screen.getAllByRole('checkbox');
      const emailToggle = toggles[0];

      expect(emailToggle).toBeChecked();
    });

    it('allows toggling notification preferences', () => {
      const toggles = screen.getAllByRole('checkbox');
      const discordToggle = toggles[1];

      expect(discordToggle).not.toBeChecked();

      fireEvent.click(discordToggle);
      expect(discordToggle).toBeChecked();
    });

    it('displays completion message', () => {
      expect(screen.getByText(/All set!/i)).toBeInTheDocument();
      expect(screen.getByText(/Click "Complete Setup" to start using Helix/i)).toBeInTheDocument();
    });
  });

  describe('Progress Bar', () => {
    it('updates progress as user advances through steps', async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      // Progress should be 20% on step 1 (1/5)
      expect(screen.getByText('Step 1 of 5')).toBeInTheDocument();

      // Advance to step 2
      fireEvent.click(screen.getByText('Continue'));
      await waitFor(() => {
        expect(screen.getByText('Step 2 of 5')).toBeInTheDocument();
      });

      // Advance to step 3
      fireEvent.click(screen.getByText('Continue'));
      await waitFor(() => {
        expect(screen.getByText('Step 3 of 5')).toBeInTheDocument();
      });
    });
  });

  describe('Accessibility', () => {
    it('has accessible form labels', async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      fireEvent.click(screen.getByText('Continue'));
      await waitFor(() => {
        expect(screen.getByLabelText(/What's your name?/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Company/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Your role/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Team size/i)).toBeInTheDocument();
      });
    });

    it('has accessible buttons', () => {
      render(<OnboardingFlow onComplete={mockOnComplete} onSkip={mockOnSkip} />);

      expect(screen.getByText('Continue')).toHaveAttribute('class', expect.stringContaining('rounded-lg'));
      expect(screen.getByText('Skip for now')).toHaveAttribute('class', expect.stringContaining('text-gray-400'));
    });
  });

  describe('Edge Cases', () => {
    it('handles rapid navigation without errors', async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      // Rapidly click Continue multiple times
      const continueButton = screen.getByText('Continue');
      fireEvent.click(continueButton);
      fireEvent.click(continueButton);
      fireEvent.click(continueButton);

      await waitFor(() => {
        // Should still be on a valid step
        expect(screen.getByText(/Step \d of 5/i)).toBeInTheDocument();
      });
    });

    it('handles completion on last step', async () => {
      render(<OnboardingFlow onComplete={mockOnComplete} />);

      // Navigate to last step
      for (let i = 0; i < 5; i++) {
        const button = screen.getByText(/Continue|Complete Setup/);
        fireEvent.click(button);
        await waitFor(() => {});
      }

      expect(mockOnComplete).toHaveBeenCalledTimes(1);
    });
  });
});
