/**
 * 🧪 Button Component Tests
 * Comprehensive tests for button variants and functionality
 */

import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from '@/components/ui/button';
import React from 'react';

describe('Button', () => {
  describe('Basic Rendering', () => {
    it('renders without crashing', () => {
      render(<Button>Click me</Button>);
      expect(screen.getByText('Click me')).toBeInTheDocument();
    });

    it('renders as a button element by default', () => {
      render(<Button>Button</Button>);
      const button = screen.getByRole('button');
      expect(button.tagName).toBe('BUTTON');
    });

    it('renders children correctly', () => {
      render(<Button>Test Content</Button>);
      expect(screen.getByText('Test Content')).toBeInTheDocument();
    });

    it('renders complex children', () => {
      render(
        <Button>
          <span>Icon</span>
          <span>Text</span>
        </Button>
      );
      expect(screen.getByText('Icon')).toBeInTheDocument();
      expect(screen.getByText('Text')).toBeInTheDocument();
    });
  });

  describe('Variants', () => {
    it('renders default variant', () => {
      render(<Button>Default</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('bg-primary');
    });

    it('renders destructive variant', () => {
      render(<Button variant="destructive">Delete</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('bg-destructive');
    });

    it('renders outline variant', () => {
      render(<Button variant="outline">Outline</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('border');
      expect(button).toHaveClass('border-input');
    });

    it('renders secondary variant', () => {
      render(<Button variant="secondary">Secondary</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('bg-secondary');
    });

    it('renders ghost variant', () => {
      render(<Button variant="ghost">Ghost</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('hover:bg-accent');
    });

    it('renders link variant', () => {
      render(<Button variant="link">Link</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('text-primary');
      expect(button).toHaveClass('underline-offset-4');
    });
  });

  describe('Sizes', () => {
    it('renders default size', () => {
      render(<Button>Default Size</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('h-9');
      expect(button).toHaveClass('px-4');
    });

    it('renders small size', () => {
      render(<Button size="sm">Small</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('h-8');
      expect(button).toHaveClass('px-3');
      expect(button).toHaveClass('text-xs');
    });

    it('renders large size', () => {
      render(<Button size="lg">Large</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('h-10');
      expect(button).toHaveClass('px-8');
    });

    it('renders icon size', () => {
      render(<Button size="icon">🔍</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('h-9');
      expect(button).toHaveClass('w-9');
    });
  });

  describe('Variant and Size Combinations', () => {
    it('combines destructive with small size', () => {
      render(<Button variant="destructive" size="sm">Delete</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('bg-destructive');
      expect(button).toHaveClass('h-8');
    });

    it('combines outline with large size', () => {
      render(<Button variant="outline" size="lg">Outline Large</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('border');
      expect(button).toHaveClass('h-10');
    });

    it('combines ghost with icon size', () => {
      render(<Button variant="ghost" size="icon">×</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('hover:bg-accent');
      expect(button).toHaveClass('h-9');
      expect(button).toHaveClass('w-9');
    });
  });

  describe('Custom Classes', () => {
    it('accepts custom className', () => {
      render(<Button className="custom-class">Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('custom-class');
    });

    it('merges custom classes with variant classes', () => {
      render(<Button variant="destructive" className="my-4">Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('bg-destructive');
      expect(button).toHaveClass('my-4');
    });
  });

  describe('Disabled State', () => {
    it('can be disabled', () => {
      render(<Button disabled>Disabled</Button>);
      const button = screen.getByRole('button');
      expect(button).toBeDisabled();
    });

    it('applies disabled styling', () => {
      render(<Button disabled>Disabled</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('disabled:pointer-events-none');
      expect(button).toHaveClass('disabled:opacity-50');
    });

    it('does not trigger onClick when disabled', async () => {
      const onClick = jest.fn();
      render(<Button disabled onClick={onClick}>Disabled</Button>);
      const button = screen.getByRole('button');

      await userEvent.click(button);

      expect(onClick).not.toHaveBeenCalled();
    });
  });

  describe('Click Handlers', () => {
    it('calls onClick when clicked', async () => {
      const onClick = jest.fn();
      render(<Button onClick={onClick}>Click Me</Button>);

      await userEvent.click(screen.getByRole('button'));

      expect(onClick).toHaveBeenCalledTimes(1);
    });

    it('passes event to onClick handler', async () => {
      const onClick = jest.fn();
      render(<Button onClick={onClick}>Click Me</Button>);

      await userEvent.click(screen.getByRole('button'));

      expect(onClick).toHaveBeenCalledWith(expect.objectContaining({
        type: 'click',
      }));
    });

    it('handles multiple clicks', async () => {
      const onClick = jest.fn();
      render(<Button onClick={onClick}>Click Me</Button>);

      await userEvent.click(screen.getByRole('button'));
      await userEvent.click(screen.getByRole('button'));
      await userEvent.click(screen.getByRole('button'));

      expect(onClick).toHaveBeenCalledTimes(3);
    });
  });

  describe('HTML Button Attributes', () => {
    it('accepts type attribute', () => {
      render(<Button type="submit">Submit</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('type', 'submit');
    });

    it('accepts id attribute', () => {
      render(<Button id="test-button">Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('id', 'test-button');
    });

    it('accepts data attributes', () => {
      render(<Button data-testid="custom-button">Button</Button>);
      expect(screen.getByTestId('custom-button')).toBeInTheDocument();
    });

    it('accepts aria attributes', () => {
      render(<Button aria-label="Close dialog">×</Button>);
      expect(screen.getByLabelText('Close dialog')).toBeInTheDocument();
    });

    it('accepts name attribute', () => {
      render(<Button name="submit-btn">Submit</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('name', 'submit-btn');
    });

    it('accepts value attribute', () => {
      render(<Button value="yes">Yes</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('value', 'yes');
    });
  });

  describe('AsChild Prop', () => {
    it('renders as child element when asChild is true', () => {
      render(
        <Button asChild>
          <a href="/test">Link Button</a>
        </Button>
      );

      const link = screen.getByRole('link');
      expect(link).toBeInTheDocument();
      expect(link).toHaveAttribute('href', '/test');
    });

    it('applies button classes to child element', () => {
      render(
        <Button asChild variant="destructive">
          <a href="/delete">Delete</a>
        </Button>
      );

      const link = screen.getByRole('link');
      expect(link).toHaveClass('bg-destructive');
    });

    it('applies size classes to child element', () => {
      render(
        <Button asChild size="lg">
          <span>Custom Element</span>
        </Button>
      );

      const span = screen.getByText('Custom Element');
      expect(span).toHaveClass('h-10');
      expect(span).toHaveClass('px-8');
    });
  });

  describe('Ref Forwarding', () => {
    it('forwards ref to button element', () => {
      const ref = React.createRef<HTMLButtonElement>();
      render(<Button ref={ref}>Button</Button>);

      expect(ref.current).toBeInstanceOf(HTMLButtonElement);
      expect(ref.current?.textContent).toBe('Button');
    });

    it('allows ref to access button methods', () => {
      const ref = React.createRef<HTMLButtonElement>();
      render(<Button ref={ref}>Focus Me</Button>);

      ref.current?.focus();

      expect(ref.current).toHaveFocus();
    });
  });

  describe('Accessibility', () => {
    it('is keyboard accessible', async () => {
      const onClick = jest.fn();
      render(<Button onClick={onClick}>Button</Button>);

      const button = screen.getByRole('button');
      button.focus();

      expect(button).toHaveFocus();

      // Simulate Enter key
      await userEvent.keyboard('{Enter}');

      expect(onClick).toHaveBeenCalled();
    });

    it('has focus-visible styles', () => {
      render(<Button>Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('focus-visible:outline-none');
      expect(button).toHaveClass('focus-visible:ring-1');
    });

    it('works with screen readers', () => {
      render(<Button aria-label="Save document">Save</Button>);
      expect(screen.getByLabelText('Save document')).toBeInTheDocument();
    });

    it('indicates disabled state to screen readers', () => {
      render(<Button disabled>Disabled Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('disabled');
    });
  });

  describe('Common Button Patterns', () => {
    it('renders icon-only button', () => {
      render(<Button size="icon" aria-label="Search">🔍</Button>);
      const button = screen.getByLabelText('Search');
      expect(button).toBeInTheDocument();
      expect(button).toHaveClass('h-9', 'w-9');
    });

    it('renders button with leading icon', () => {
      render(
        <Button>
          <span>➕</span> Add Item
        </Button>
      );
      expect(screen.getByText('Add Item')).toBeInTheDocument();
      expect(screen.getByText('➕')).toBeInTheDocument();
    });

    it('renders button with trailing icon', () => {
      render(
        <Button>
          Next <span>→</span>
        </Button>
      );
      expect(screen.getByText('Next')).toBeInTheDocument();
      expect(screen.getByText('→')).toBeInTheDocument();
    });

    it('renders submit button', () => {
      render(<Button type="submit">Submit Form</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('type', 'submit');
    });

    it('renders reset button', () => {
      render(<Button type="reset">Reset</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('type', 'reset');
    });
  });

  describe('Style Classes', () => {
    it('has base styling classes', () => {
      render(<Button>Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('inline-flex');
      expect(button).toHaveClass('items-center');
      expect(button).toHaveClass('justify-center');
      expect(button).toHaveClass('rounded-md');
      expect(button).toHaveClass('font-medium');
    });

    it('has transition classes', () => {
      render(<Button>Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('transition-colors');
    });

    it('prevents text wrapping', () => {
      render(<Button>Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('whitespace-nowrap');
    });
  });

  describe('Edge Cases', () => {
    it('handles empty children', () => {
      render(<Button></Button>);
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
      expect(button).toBeEmptyDOMElement();
    });

    it('handles null children', () => {
      render(<Button>{null}</Button>);
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });

    it('handles undefined variant gracefully', () => {
      render(<Button variant={undefined}>Button</Button>);
      const button = screen.getByRole('button');
      // Should fall back to default variant
      expect(button).toHaveClass('bg-primary');
    });

    it('handles undefined size gracefully', () => {
      render(<Button size={undefined}>Button</Button>);
      const button = screen.getByRole('button');
      // Should fall back to default size
      expect(button).toHaveClass('h-9');
    });
  });

  describe('Integration with Forms', () => {
    it('submits form when type is submit', () => {
      const onSubmit = jest.fn((e) => e.preventDefault());

      render(
        <form onSubmit={onSubmit}>
          <Button type="submit">Submit</Button>
        </form>
      );

      const button = screen.getByRole('button');
      button.click();

      expect(onSubmit).toHaveBeenCalled();
    });

    it('does not submit when disabled', () => {
      const onSubmit = jest.fn((e) => e.preventDefault());

      render(
        <form onSubmit={onSubmit}>
          <Button type="submit" disabled>Submit</Button>
        </form>
      );

      const button = screen.getByRole('button');
      button.click();

      expect(onSubmit).not.toHaveBeenCalled();
    });
  });
});
