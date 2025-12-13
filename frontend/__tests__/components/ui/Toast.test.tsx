/**
 * 🧪 Toast Component Tests
 * Comprehensive tests for toast notification system
 */

import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ToastProvider, useToast, toast, setGlobalToast } from '@/components/ui/Toast';
import React from 'react';

// Test component that uses the toast hook
const TestComponent = ({ onToastCreated }: { onToastCreated?: (id: string) => void }) => {
  const { success, error, warning, info, loading, dismissToast, showToast } = useToast();

  return (
    <div>
      <button onClick={() => { const id = success('Success!'); onToastCreated?.(id); }}>
        Show Success
      </button>
      <button onClick={() => { const id = error('Error!', 'Something went wrong'); onToastCreated?.(id); }}>
        Show Error
      </button>
      <button onClick={() => { const id = warning('Warning!'); onToastCreated?.(id); }}>
        Show Warning
      </button>
      <button onClick={() => { const id = info('Info!'); onToastCreated?.(id); }}>
        Show Info
      </button>
      <button onClick={() => { const id = loading('Loading...'); onToastCreated?.(id); }}>
        Show Loading
      </button>
      <button
        onClick={() => {
          const id = showToast({
            type: 'success',
            message: 'Custom Toast',
            duration: 10000,
          });
          onToastCreated?.(id);
        }}
      >
        Show Custom
      </button>
      <button onClick={() => dismissToast('test-id')}>Dismiss Toast</button>
    </div>
  );
};

describe('ToastProvider', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  describe('Provider Setup', () => {
    it('renders children without crashing', () => {
      render(
        <ToastProvider>
          <div>Test Content</div>
        </ToastProvider>
      );
      expect(screen.getByText('Test Content')).toBeInTheDocument();
    });

    it('accepts position prop', () => {
      render(
        <ToastProvider position="bottom-left">
          <div>Test</div>
        </ToastProvider>
      );
      expect(screen.getByText('Test')).toBeInTheDocument();
    });

    it('accepts maxToasts prop', () => {
      render(
        <ToastProvider maxToasts={3}>
          <div>Test</div>
        </ToastProvider>
      );
      expect(screen.getByText('Test')).toBeInTheDocument();
    });
  });

  describe('useToast Hook', () => {
    it('throws error when used outside provider', () => {
      // Suppress console.error for this test
      const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {});

      expect(() => {
        render(<TestComponent />);
      }).toThrow('useToast must be used within ToastProvider');

      consoleError.mockRestore();
    });

    it('returns toast functions when used inside provider', () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      expect(screen.getByText('Show Success')).toBeInTheDocument();
      expect(screen.getByText('Show Error')).toBeInTheDocument();
      expect(screen.getByText('Show Warning')).toBeInTheDocument();
      expect(screen.getByText('Show Info')).toBeInTheDocument();
      expect(screen.getByText('Show Loading')).toBeInTheDocument();
    });
  });

  describe('Success Toast', () => {
    it('displays success toast when triggered', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      const button = screen.getByText('Show Success');
      await userEvent.click(button);

      expect(screen.getByText('Success!')).toBeInTheDocument();
    });

    it('shows success icon', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));

      expect(screen.getByText('✅')).toBeInTheDocument();
    });

    it('returns toast ID', async () => {
      const onToastCreated = jest.fn();
      render(
        <ToastProvider>
          <TestComponent onToastCreated={onToastCreated} />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));

      expect(onToastCreated).toHaveBeenCalledWith(expect.stringContaining('toast-'));
    });
  });

  describe('Error Toast', () => {
    it('displays error toast with description', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Error'));

      expect(screen.getByText('Error!')).toBeInTheDocument();
      expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    });

    it('shows error icon', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Error'));

      expect(screen.getByText('❌')).toBeInTheDocument();
    });
  });

  describe('Warning Toast', () => {
    it('displays warning toast', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Warning'));

      expect(screen.getByText('Warning!')).toBeInTheDocument();
      expect(screen.getByText('⚠️')).toBeInTheDocument();
    });
  });

  describe('Info Toast', () => {
    it('displays info toast', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Info'));

      expect(screen.getByText('Info!')).toBeInTheDocument();
      expect(screen.getByText('ℹ️')).toBeInTheDocument();
    });
  });

  describe('Loading Toast', () => {
    it('displays loading toast', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Loading'));

      expect(screen.getByText('Loading...')).toBeInTheDocument();
      expect(screen.getByText('⏳')).toBeInTheDocument();
    });

    it('loading toast has no duration (stays visible)', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Loading'));

      expect(screen.getByText('Loading...')).toBeInTheDocument();

      // Fast-forward time
      act(() => {
        jest.advanceTimersByTime(10000);
      });

      // Loading toast should still be visible
      expect(screen.getByText('Loading...')).toBeInTheDocument();
    });

    it('loading toast is not dismissible', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Loading'));

      const toast = screen.getByText('Loading...').closest('[role="alert"]');
      expect(toast).toBeInTheDocument();

      // Should not have dismiss button
      const dismissButton = toast?.querySelector('[aria-label="Dismiss"]');
      expect(dismissButton).not.toBeInTheDocument();
    });
  });

  describe('Toast Dismissal', () => {
    it('shows dismiss button by default', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));

      expect(screen.getByLabelText('Dismiss')).toBeInTheDocument();
    });

    it('dismisses toast when X is clicked', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));
      expect(screen.getByText('Success!')).toBeInTheDocument();

      const dismissButton = screen.getByLabelText('Dismiss');
      await userEvent.click(dismissButton);

      await waitFor(() => {
        expect(screen.queryByText('Success!')).not.toBeInTheDocument();
      });
    });
  });

  describe('Auto-dismiss', () => {
    it('auto-dismisses after default duration (5 seconds)', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));
      expect(screen.getByText('Success!')).toBeInTheDocument();

      // Fast-forward 5 seconds
      act(() => {
        jest.advanceTimersByTime(5000);
      });

      await waitFor(() => {
        expect(screen.queryByText('Success!')).not.toBeInTheDocument();
      });
    });

    it('respects custom duration', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Custom'));
      expect(screen.getByText('Custom Toast')).toBeInTheDocument();

      // Fast-forward 5 seconds (less than custom 10s duration)
      act(() => {
        jest.advanceTimersByTime(5000);
      });

      // Should still be visible
      expect(screen.getByText('Custom Toast')).toBeInTheDocument();

      // Fast-forward another 5 seconds (total 10s)
      act(() => {
        jest.advanceTimersByTime(5000);
      });

      await waitFor(() => {
        expect(screen.queryByText('Custom Toast')).not.toBeInTheDocument();
      });
    });
  });

  describe('Progress Bar', () => {
    it('shows progress bar for timed toasts', async () => {
      const { container } = render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));

      // Look for progress bar animation
      const progressBar = container.querySelector('.animate-progress');
      expect(progressBar).toBeInTheDocument();
    });

    it('does not show progress bar for loading toast', async () => {
      const { container } = render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Loading'));

      // Loading toast has duration 0, so no progress bar
      const alert = screen.getByRole('alert');
      const progressBar = alert.querySelector('.animate-progress');
      expect(progressBar).not.toBeInTheDocument();
    });
  });

  describe('Toast Queue Management', () => {
    it('displays multiple toasts', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));
      await userEvent.click(screen.getByText('Show Error'));
      await userEvent.click(screen.getByText('Show Warning'));

      expect(screen.getByText('Success!')).toBeInTheDocument();
      expect(screen.getByText('Error!')).toBeInTheDocument();
      expect(screen.getByText('Warning!')).toBeInTheDocument();
    });

    it('limits toasts to maxToasts', async () => {
      render(
        <ToastProvider maxToasts={2}>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));
      await userEvent.click(screen.getByText('Show Error'));
      await userEvent.click(screen.getByText('Show Warning'));

      // Only the last 2 toasts should be visible
      expect(screen.queryByText('Success!')).not.toBeInTheDocument();
      expect(screen.getByText('Error!')).toBeInTheDocument();
      expect(screen.getByText('Warning!')).toBeInTheDocument();
    });
  });

  describe('Toast Positioning', () => {
    it('applies top-right position by default', () => {
      const { container } = render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      // Container should have top-right position classes
      const toastContainer = container.querySelector('.fixed');
      expect(toastContainer).toHaveClass('top-4', 'right-4');
    });

    it('applies custom position', () => {
      const { container } = render(
        <ToastProvider position="bottom-left">
          <TestComponent />
        </ToastProvider>
      );

      const toastContainer = container.querySelector('.fixed');
      expect(toastContainer).toHaveClass('bottom-4', 'left-4');
    });

    it('supports all position options', () => {
      const positions: Array<'top-left' | 'top-center' | 'top-right' | 'bottom-left' | 'bottom-center' | 'bottom-right'> = [
        'top-left',
        'top-center',
        'top-right',
        'bottom-left',
        'bottom-center',
        'bottom-right',
      ];

      positions.forEach((position) => {
        const { container, unmount } = render(
          <ToastProvider position={position}>
            <div>Test</div>
          </ToastProvider>
        );

        const toastContainer = container.querySelector('.fixed');
        expect(toastContainer).toBeInTheDocument();

        unmount();
      });
    });
  });

  describe('Toast with Actions', () => {
    it('displays action button when provided', async () => {
      const TestWithAction = () => {
        const { showToast } = useToast();
        return (
          <button
            onClick={() =>
              showToast({
                type: 'info',
                message: 'Action Toast',
                action: {
                  label: 'Undo',
                  onClick: () => {},
                },
              })
            }
          >
            Show Action Toast
          </button>
        );
      };

      render(
        <ToastProvider>
          <TestWithAction />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Action Toast'));

      expect(screen.getByText('Undo')).toBeInTheDocument();
    });

    it('calls action onClick when clicked', async () => {
      const mockAction = jest.fn();

      const TestWithAction = () => {
        const { showToast } = useToast();
        return (
          <button
            onClick={() =>
              showToast({
                type: 'info',
                message: 'Action Toast',
                action: {
                  label: 'Click Me',
                  onClick: mockAction,
                },
              })
            }
          >
            Show Action Toast
          </button>
        );
      };

      render(
        <ToastProvider>
          <TestWithAction />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Action Toast'));
      await userEvent.click(screen.getByText('Click Me'));

      expect(mockAction).toHaveBeenCalledTimes(1);
    });
  });

  describe('Global Toast API', () => {
    it('sets global toast handler', () => {
      const mockShowToast = jest.fn();
      setGlobalToast(mockShowToast);

      toast.success('Global Success');

      expect(mockShowToast).toHaveBeenCalledWith({
        type: 'success',
        message: 'Global Success',
        description: undefined,
      });
    });

    it('provides global success method', () => {
      const mockShowToast = jest.fn(() => 'toast-id');
      setGlobalToast(mockShowToast);

      const id = toast.success('Success', 'Description');

      expect(mockShowToast).toHaveBeenCalledWith({
        type: 'success',
        message: 'Success',
        description: 'Description',
      });
      expect(id).toBe('toast-id');
    });

    it('provides global error method', () => {
      const mockShowToast = jest.fn(() => 'toast-id');
      setGlobalToast(mockShowToast);

      toast.error('Error', 'Details');

      expect(mockShowToast).toHaveBeenCalledWith({
        type: 'error',
        message: 'Error',
        description: 'Details',
      });
    });

    it('provides global warning method', () => {
      const mockShowToast = jest.fn(() => 'toast-id');
      setGlobalToast(mockShowToast);

      toast.warning('Warning');

      expect(mockShowToast).toHaveBeenCalledWith({
        type: 'warning',
        message: 'Warning',
        description: undefined,
      });
    });

    it('provides global info method', () => {
      const mockShowToast = jest.fn(() => 'toast-id');
      setGlobalToast(mockShowToast);

      toast.info('Info');

      expect(mockShowToast).toHaveBeenCalledWith({
        type: 'info',
        message: 'Info',
        description: undefined,
      });
    });

    it('provides global loading method', () => {
      const mockShowToast = jest.fn(() => 'toast-id');
      setGlobalToast(mockShowToast);

      toast.loading('Loading');

      expect(mockShowToast).toHaveBeenCalledWith({
        type: 'loading',
        message: 'Loading',
        description: undefined,
        duration: 0,
      });
    });

    it('returns empty string when global toast not initialized', () => {
      setGlobalToast(null as any);

      const id = toast.success('Test');

      expect(id).toBe('');
    });
  });

  describe('Accessibility', () => {
    it('uses role="alert" for toasts', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));

      expect(screen.getByRole('alert')).toBeInTheDocument();
    });

    it('dismiss button has aria-label', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));

      expect(screen.getByLabelText('Dismiss')).toBeInTheDocument();
    });
  });

  describe('Animations', () => {
    it('applies slideIn animation', async () => {
      const { container } = render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));

      const toast = container.querySelector('.animate-slideIn');
      expect(toast).toBeInTheDocument();
    });

    it('includes animation styles', async () => {
      const { container } = render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));

      // Check for style tag with animations
      const styleTag = container.querySelector('style');
      expect(styleTag?.textContent).toContain('@keyframes slideIn');
      expect(styleTag?.textContent).toContain('@keyframes progress');
    });
  });

  describe('Edge Cases', () => {
    it('handles rapid toast creation', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      // Rapidly create multiple toasts
      await userEvent.click(screen.getByText('Show Success'));
      await userEvent.click(screen.getByText('Show Error'));
      await userEvent.click(screen.getByText('Show Warning'));
      await userEvent.click(screen.getByText('Show Info'));

      // All should be visible
      expect(screen.getByText('Success!')).toBeInTheDocument();
      expect(screen.getByText('Error!')).toBeInTheDocument();
      expect(screen.getByText('Warning!')).toBeInTheDocument();
      expect(screen.getByText('Info!')).toBeInTheDocument();
    });

    it('handles dismissing non-existent toast gracefully', async () => {
      render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      // Try to dismiss a toast that doesn't exist
      await userEvent.click(screen.getByText('Dismiss Toast'));

      // Should not throw error
      expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    });

    it('cleans up timers on unmount', async () => {
      const { unmount } = render(
        <ToastProvider>
          <TestComponent />
        </ToastProvider>
      );

      await userEvent.click(screen.getByText('Show Success'));

      unmount();

      // Should not throw error
      act(() => {
        jest.advanceTimersByTime(5000);
      });
    });
  });
});
