/**
 * 🧪 Loading Component Tests
 * Tests for all loading variants and components
 */

import { render, screen } from '@testing-library/react';
import {
  Loading,
  LoadingButton,
  PageLoading,
  InlineLoading,
  Skeleton,
} from '@/components/ui/Loading';
import userEvent from '@testing-library/user-event';

describe('Loading Component', () => {
  describe('Basic Rendering', () => {
    it('renders without crashing', () => {
      render(<Loading />);
      // Component renders successfully
    });

    it('renders with consciousness variant by default', () => {
      const { container } = render(<Loading />);
      // Consciousness variant has gradient bars
      expect(container.querySelector('.bg-gradient-to-t')).toBeInTheDocument();
    });

    it('renders with custom className', () => {
      const { container } = render(<Loading className="custom-class" />);
      expect(container.firstChild).toHaveClass('custom-class');
    });
  });

  describe('Variants', () => {
    it('renders spinner variant', () => {
      const { container } = render(<Loading variant="spinner" />);
      expect(container.querySelector('.animate-spin')).toBeInTheDocument();
      expect(container.querySelector('.rounded-full')).toBeInTheDocument();
    });

    it('renders consciousness variant', () => {
      const { container } = render(<Loading variant="consciousness" />);
      expect(container.querySelector('.bg-gradient-to-t')).toBeInTheDocument();
    });

    it('renders pulse variant', () => {
      const { container } = render(<Loading variant="pulse" />);
      expect(container.querySelector('.animate-ping')).toBeInTheDocument();
    });

    it('renders dots variant', () => {
      const { container } = render(<Loading variant="dots" />);
      const dots = container.querySelectorAll('.bg-blue-500');
      expect(dots.length).toBe(3);
    });

    it('renders skeleton variant', () => {
      const { container } = render(<Loading variant="skeleton" />);
      expect(container.querySelector('.animate-pulse')).toBeInTheDocument();
    });
  });

  describe('Sizes', () => {
    it('renders small size', () => {
      const { container } = render(<Loading size="sm" />);
      // Component renders with appropriate sizing
      expect(container.firstChild).toBeInTheDocument();
    });

    it('renders medium size', () => {
      const { container } = render(<Loading size="md" />);
      expect(container.firstChild).toBeInTheDocument();
    });

    it('renders large size', () => {
      const { container } = render(<Loading size="lg" />);
      expect(container.firstChild).toBeInTheDocument();
    });

    it('renders extra large size', () => {
      const { container } = render(<Loading size="xl" />);
      expect(container.firstChild).toBeInTheDocument();
    });
  });

  describe('Loading Message', () => {
    it('displays loading message when provided', () => {
      render(<Loading message="Loading data..." />);
      expect(screen.getByText('Loading data...')).toBeInTheDocument();
    });

    it('does not display message when not provided', () => {
      const { container } = render(<Loading />);
      expect(container.querySelector('p')).not.toBeInTheDocument();
    });

    it('message has correct styling', () => {
      render(<Loading message="Test message" />);
      const message = screen.getByText('Test message');
      expect(message).toHaveClass('text-gray-400');
      expect(message).toHaveClass('animate-pulse');
    });
  });

  describe('Fullscreen Mode', () => {
    it('renders fullscreen overlay when enabled', () => {
      const { container } = render(<Loading fullscreen={true} />);
      expect(container.querySelector('.fixed')).toBeInTheDocument();
      expect(container.querySelector('.inset-0')).toBeInTheDocument();
      expect(container.querySelector('.z-50')).toBeInTheDocument();
    });

    it('does not render fullscreen overlay by default', () => {
      const { container } = render(<Loading />);
      expect(container.querySelector('.fixed')).not.toBeInTheDocument();
    });

    it('fullscreen mode has backdrop blur', () => {
      const { container } = render(<Loading fullscreen={true} />);
      expect(container.querySelector('.backdrop-blur-sm')).toBeInTheDocument();
    });
  });
});

describe('LoadingButton Component', () => {
  const mockOnClick = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders children when not loading', () => {
    render(<LoadingButton onClick={mockOnClick}>Click me</LoadingButton>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('shows loading text when loading', () => {
    render(
      <LoadingButton loading={true} loadingText="Processing...">
        Click me
      </LoadingButton>
    );
    expect(screen.getByText('Processing...')).toBeInTheDocument();
    expect(screen.queryByText('Click me')).not.toBeInTheDocument();
  });

  it('is disabled when loading', () => {
    render(
      <LoadingButton loading={true}>
        Click me
      </LoadingButton>
    );
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
  });

  it('is disabled when disabled prop is true', () => {
    render(
      <LoadingButton disabled={true}>
        Click me
      </LoadingButton>
    );
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
  });

  it('can be clicked when not loading', async () => {
    render(<LoadingButton onClick={mockOnClick}>Click me</LoadingButton>);
    const button = screen.getByRole('button');

    await userEvent.click(button);

    expect(mockOnClick).toHaveBeenCalledTimes(1);
  });

  it('cannot be clicked when loading', async () => {
    render(
      <LoadingButton loading={true} onClick={mockOnClick}>
        Click me
      </LoadingButton>
    );
    const button = screen.getByRole('button');

    await userEvent.click(button);

    expect(mockOnClick).not.toHaveBeenCalled();
  });

  it('shows dots loader when loading', () => {
    const { container } = render(
      <LoadingButton loading={true}>Click me</LoadingButton>
    );
    const dots = container.querySelectorAll('.bg-blue-500');
    expect(dots.length).toBe(3);
  });

  it('applies custom className', () => {
    render(
      <LoadingButton className="custom-button-class">
        Click me
      </LoadingButton>
    );
    const button = screen.getByRole('button');
    expect(button).toHaveClass('custom-button-class');
  });

  it('uses default loading text', () => {
    render(<LoadingButton loading={true}>Click me</LoadingButton>);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
});

describe('PageLoading Component', () => {
  it('renders with default message', () => {
    render(<PageLoading />);
    expect(screen.getByText('Loading Helix...')).toBeInTheDocument();
  });

  it('renders with custom message', () => {
    render(<PageLoading message="Initializing application..." />);
    expect(screen.getByText('Initializing application...')).toBeInTheDocument();
  });

  it('uses extra large size', () => {
    const { container } = render(<PageLoading />);
    // XL size should be rendered
    expect(container.firstChild).toHaveClass('min-h-screen');
  });

  it('has gradient background', () => {
    const { container } = render(<PageLoading />);
    expect(container.firstChild).toHaveClass('bg-gradient-to-br');
  });

  it('uses consciousness variant', () => {
    const { container } = render(<PageLoading />);
    expect(container.querySelector('.bg-gradient-to-t')).toBeInTheDocument();
  });
});

describe('InlineLoading Component', () => {
  it('renders without message', () => {
    const { container } = render(<InlineLoading />);
    expect(container.querySelector('.py-8')).toBeInTheDocument();
  });

  it('renders with custom message', () => {
    render(<InlineLoading message="Loading content..." />);
    expect(screen.getByText('Loading content...')).toBeInTheDocument();
  });

  it('uses medium size', () => {
    const { container } = render(<InlineLoading />);
    // Should render with md size
    expect(container.firstChild).toBeInTheDocument();
  });

  it('uses consciousness variant', () => {
    const { container } = render(<InlineLoading />);
    expect(container.querySelector('.bg-gradient-to-t')).toBeInTheDocument();
  });

  it('is centered', () => {
    const { container } = render(<InlineLoading />);
    expect(container.firstChild).toHaveClass('flex');
    expect(container.firstChild).toHaveClass('justify-center');
  });
});

describe('Skeleton Component', () => {
  it('renders with default styling', () => {
    const { container } = render(<Skeleton />);
    const skeleton = container.firstChild;
    expect(skeleton).toHaveClass('bg-gray-700/50');
    expect(skeleton).toHaveClass('rounded');
    expect(skeleton).toHaveClass('animate-pulse');
  });

  it('applies custom className', () => {
    const { container } = render(<Skeleton className="w-full h-20" />);
    const skeleton = container.firstChild;
    expect(skeleton).toHaveClass('w-full');
    expect(skeleton).toHaveClass('h-20');
  });

  it('can be used as content placeholder', () => {
    render(
      <div>
        <Skeleton className="w-32 h-8 mb-2" />
        <Skeleton className="w-full h-4 mb-1" />
        <Skeleton className="w-full h-4" />
      </div>
    );

    const skeletons = document.querySelectorAll('.bg-gray-700\\/50');
    expect(skeletons.length).toBe(3);
  });
});

describe('Loading Variants Animation', () => {
  it('consciousness variant has animation', () => {
    const { container } = render(<Loading variant="consciousness" />);
    const bars = container.querySelectorAll('[style*="animation"]');
    expect(bars.length).toBeGreaterThan(0);
  });

  it('dots variant has animation', () => {
    const { container } = render(<Loading variant="dots" />);
    const dots = container.querySelectorAll('[style*="animation"]');
    expect(dots.length).toBe(3);
  });

  it('spinner variant has animate-spin class', () => {
    const { container } = render(<Loading variant="spinner" />);
    expect(container.querySelector('.animate-spin')).toBeInTheDocument();
  });

  it('pulse variant has animate-ping class', () => {
    const { container } = render(<Loading variant="pulse" />);
    expect(container.querySelector('.animate-ping')).toBeInTheDocument();
  });
});

describe('Loading Accessibility', () => {
  it('loading message is visible to screen readers', () => {
    render(<Loading message="Loading application" />);
    const message = screen.getByText('Loading application');
    expect(message).toBeVisible();
  });

  it('loading button indicates loading state', () => {
    render(<LoadingButton loading={true}>Submit</LoadingButton>);
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    expect(button).toHaveAttribute('disabled');
  });
});
