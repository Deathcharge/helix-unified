/**
 * 🧪 Card Component Tests
 * Tests for all card component variants
 */

import { render, screen } from '@testing-library/react';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from '@/components/ui/card';
import React from 'react';

describe('Card Components', () => {
  describe('Card', () => {
    it('renders without crashing', () => {
      render(<Card>Card content</Card>);
      expect(screen.getByText('Card content')).toBeInTheDocument();
    });

    it('renders as a div element', () => {
      const { container } = render(<Card>Content</Card>);
      const card = container.firstChild;
      expect(card?.nodeName).toBe('DIV');
    });

    it('applies base styling classes', () => {
      const { container } = render(<Card>Content</Card>);
      const card = container.firstChild as HTMLElement;
      expect(card).toHaveClass('rounded-xl');
      expect(card).toHaveClass('border');
      expect(card).toHaveClass('shadow');
    });

    it('accepts custom className', () => {
      const { container } = render(<Card className="custom-class">Content</Card>);
      const card = container.firstChild as HTMLElement;
      expect(card).toHaveClass('custom-class');
    });

    it('merges custom classes with base classes', () => {
      const { container } = render(<Card className="mt-4">Content</Card>);
      const card = container.firstChild as HTMLElement;
      expect(card).toHaveClass('rounded-xl');
      expect(card).toHaveClass('mt-4');
    });

    it('forwards ref correctly', () => {
      const ref = React.createRef<HTMLDivElement>();
      render(<Card ref={ref}>Content</Card>);
      expect(ref.current).toBeInstanceOf(HTMLDivElement);
    });

    it('accepts HTML div attributes', () => {
      render(<Card data-testid="test-card" id="my-card">Content</Card>);
      const card = screen.getByTestId('test-card');
      expect(card).toHaveAttribute('id', 'my-card');
    });

    it('renders children correctly', () => {
      render(
        <Card>
          <p>Child 1</p>
          <p>Child 2</p>
        </Card>
      );
      expect(screen.getByText('Child 1')).toBeInTheDocument();
      expect(screen.getByText('Child 2')).toBeInTheDocument();
    });
  });

  describe('CardHeader', () => {
    it('renders without crashing', () => {
      render(<CardHeader>Header content</CardHeader>);
      expect(screen.getByText('Header content')).toBeInTheDocument();
    });

    it('renders as a div element', () => {
      const { container } = render(<CardHeader>Content</CardHeader>);
      const header = container.firstChild;
      expect(header?.nodeName).toBe('DIV');
    });

    it('applies base styling classes', () => {
      const { container } = render(<CardHeader>Content</CardHeader>);
      const header = container.firstChild as HTMLElement;
      expect(header).toHaveClass('flex');
      expect(header).toHaveClass('flex-col');
      expect(header).toHaveClass('space-y-1.5');
      expect(header).toHaveClass('p-6');
    });

    it('accepts custom className', () => {
      const { container } = render(<CardHeader className="custom-header">Content</CardHeader>);
      const header = container.firstChild as HTMLElement;
      expect(header).toHaveClass('custom-header');
    });

    it('forwards ref correctly', () => {
      const ref = React.createRef<HTMLDivElement>();
      render(<CardHeader ref={ref}>Content</CardHeader>);
      expect(ref.current).toBeInstanceOf(HTMLDivElement);
    });
  });

  describe('CardTitle', () => {
    it('renders without crashing', () => {
      render(<CardTitle>Title</CardTitle>);
      expect(screen.getByText('Title')).toBeInTheDocument();
    });

    it('renders as h3 element', () => {
      render(<CardTitle>Title</CardTitle>);
      const title = screen.getByText('Title');
      expect(title.tagName).toBe('H3');
    });

    it('applies base styling classes', () => {
      render(<CardTitle>Title</CardTitle>);
      const title = screen.getByText('Title');
      expect(title).toHaveClass('font-semibold');
      expect(title).toHaveClass('leading-none');
      expect(title).toHaveClass('tracking-tight');
    });

    it('accepts custom className', () => {
      render(<CardTitle className="custom-title">Title</CardTitle>);
      const title = screen.getByText('Title');
      expect(title).toHaveClass('custom-title');
    });

    it('forwards ref correctly', () => {
      const ref = React.createRef<HTMLParagraphElement>();
      render(<CardTitle ref={ref}>Title</CardTitle>);
      expect(ref.current).toBeInstanceOf(HTMLHeadingElement);
    });
  });

  describe('CardDescription', () => {
    it('renders without crashing', () => {
      render(<CardDescription>Description text</CardDescription>);
      expect(screen.getByText('Description text')).toBeInTheDocument();
    });

    it('renders as p element', () => {
      render(<CardDescription>Description</CardDescription>);
      const description = screen.getByText('Description');
      expect(description.tagName).toBe('P');
    });

    it('applies base styling classes', () => {
      render(<CardDescription>Description</CardDescription>);
      const description = screen.getByText('Description');
      expect(description).toHaveClass('text-sm');
      expect(description).toHaveClass('text-slate-500');
    });

    it('accepts custom className', () => {
      render(<CardDescription className="custom-desc">Description</CardDescription>);
      const description = screen.getByText('Description');
      expect(description).toHaveClass('custom-desc');
    });

    it('forwards ref correctly', () => {
      const ref = React.createRef<HTMLParagraphElement>();
      render(<CardDescription ref={ref}>Description</CardDescription>);
      expect(ref.current).toBeInstanceOf(HTMLParagraphElement);
    });
  });

  describe('CardContent', () => {
    it('renders without crashing', () => {
      render(<CardContent>Content text</CardContent>);
      expect(screen.getByText('Content text')).toBeInTheDocument();
    });

    it('renders as div element', () => {
      const { container } = render(<CardContent>Content</CardContent>);
      const content = container.firstChild;
      expect(content?.nodeName).toBe('DIV');
    });

    it('applies base styling classes', () => {
      const { container } = render(<CardContent>Content</CardContent>);
      const content = container.firstChild as HTMLElement;
      expect(content).toHaveClass('p-6');
      expect(content).toHaveClass('pt-0');
    });

    it('accepts custom className', () => {
      const { container } = render(<CardContent className="custom-content">Content</CardContent>);
      const content = container.firstChild as HTMLElement;
      expect(content).toHaveClass('custom-content');
    });

    it('forwards ref correctly', () => {
      const ref = React.createRef<HTMLDivElement>();
      render(<CardContent ref={ref}>Content</CardContent>);
      expect(ref.current).toBeInstanceOf(HTMLDivElement);
    });
  });

  describe('CardFooter', () => {
    it('renders without crashing', () => {
      render(<CardFooter>Footer content</CardFooter>);
      expect(screen.getByText('Footer content')).toBeInTheDocument();
    });

    it('renders as div element', () => {
      const { container } = render(<CardFooter>Footer</CardFooter>);
      const footer = container.firstChild;
      expect(footer?.nodeName).toBe('DIV');
    });

    it('applies base styling classes', () => {
      const { container } = render(<CardFooter>Footer</CardFooter>);
      const footer = container.firstChild as HTMLElement;
      expect(footer).toHaveClass('flex');
      expect(footer).toHaveClass('items-center');
      expect(footer).toHaveClass('p-6');
      expect(footer).toHaveClass('pt-0');
    });

    it('accepts custom className', () => {
      const { container } = render(<CardFooter className="custom-footer">Footer</CardFooter>);
      const footer = container.firstChild as HTMLElement;
      expect(footer).toHaveClass('custom-footer');
    });

    it('forwards ref correctly', () => {
      const ref = React.createRef<HTMLDivElement>();
      render(<CardFooter ref={ref}>Footer</CardFooter>);
      expect(ref.current).toBeInstanceOf(HTMLDivElement);
    });
  });

  describe('Card Composition', () => {
    it('renders complete card with all components', () => {
      render(
        <Card>
          <CardHeader>
            <CardTitle>Card Title</CardTitle>
            <CardDescription>Card Description</CardDescription>
          </CardHeader>
          <CardContent>
            <p>Main content goes here</p>
          </CardContent>
          <CardFooter>
            <button>Action</button>
          </CardFooter>
        </Card>
      );

      expect(screen.getByText('Card Title')).toBeInTheDocument();
      expect(screen.getByText('Card Description')).toBeInTheDocument();
      expect(screen.getByText('Main content goes here')).toBeInTheDocument();
      expect(screen.getByText('Action')).toBeInTheDocument();
    });

    it('maintains proper hierarchy', () => {
      render(
        <Card data-testid="card">
          <CardHeader data-testid="header">
            <CardTitle data-testid="title">Title</CardTitle>
          </CardHeader>
          <CardContent data-testid="content">Content</CardContent>
        </Card>
      );

      const card = screen.getByTestId('card');
      const header = screen.getByTestId('header');
      const title = screen.getByTestId('title');
      const content = screen.getByTestId('content');

      expect(card).toContainElement(header);
      expect(header).toContainElement(title);
      expect(card).toContainElement(content);
    });

    it('renders card without footer', () => {
      render(
        <Card>
          <CardHeader>
            <CardTitle>Title</CardTitle>
          </CardHeader>
          <CardContent>Content</CardContent>
        </Card>
      );

      expect(screen.getByText('Title')).toBeInTheDocument();
      expect(screen.getByText('Content')).toBeInTheDocument();
    });

    it('renders card without header', () => {
      render(
        <Card>
          <CardContent>Just content</CardContent>
          <CardFooter>Footer</CardFooter>
        </Card>
      );

      expect(screen.getByText('Just content')).toBeInTheDocument();
      expect(screen.getByText('Footer')).toBeInTheDocument();
    });

    it('renders card with only content', () => {
      render(
        <Card>
          <CardContent>Minimal card</CardContent>
        </Card>
      );

      expect(screen.getByText('Minimal card')).toBeInTheDocument();
    });
  });

  describe('Styling Variations', () => {
    it('applies custom styles to nested components', () => {
      render(
        <Card className="bg-red-500">
          <CardHeader className="bg-blue-500">
            <CardTitle className="text-xl">Title</CardTitle>
            <CardDescription className="text-gray-600">Description</CardDescription>
          </CardHeader>
          <CardContent className="bg-green-500">Content</CardContent>
          <CardFooter className="bg-yellow-500">Footer</CardFooter>
        </Card>
      );

      const { container } = render(
        <Card className="bg-red-500">
          <CardHeader className="bg-blue-500">Header</CardHeader>
        </Card>
      );

      expect(container.querySelector('.bg-red-500')).toBeInTheDocument();
      expect(container.querySelector('.bg-blue-500')).toBeInTheDocument();
    });

    it('maintains spacing with space-y in header', () => {
      const { container } = render(
        <CardHeader>
          <CardTitle>Title</CardTitle>
          <CardDescription>Description</CardDescription>
        </CardHeader>
      );

      const header = container.firstChild as HTMLElement;
      expect(header).toHaveClass('space-y-1.5');
    });

    it('removes top padding from content', () => {
      const { container } = render(<CardContent>Content</CardContent>);
      const content = container.firstChild as HTMLElement;
      expect(content).toHaveClass('pt-0');
    });

    it('removes top padding from footer', () => {
      const { container } = render(<CardFooter>Footer</CardFooter>);
      const footer = container.firstChild as HTMLElement;
      expect(footer).toHaveClass('pt-0');
    });
  });

  describe('Accessibility', () => {
    it('uses semantic heading for title', () => {
      render(<CardTitle>Accessible Title</CardTitle>);
      const title = screen.getByText('Accessible Title');
      expect(title.tagName).toBe('H3');
    });

    it('accepts aria attributes on Card', () => {
      render(<Card aria-label="Product card">Content</Card>);
      const card = screen.getByLabelText('Product card');
      expect(card).toBeInTheDocument();
    });

    it('accepts aria attributes on all components', () => {
      render(
        <Card aria-labelledby="card-title">
          <CardHeader aria-label="Card header">
            <CardTitle id="card-title">Title</CardTitle>
          </CardHeader>
          <CardContent aria-label="Card content">Content</CardContent>
          <CardFooter aria-label="Card footer">Footer</CardFooter>
        </Card>
      );

      expect(screen.getByLabelText('Card header')).toBeInTheDocument();
      expect(screen.getByLabelText('Card content')).toBeInTheDocument();
      expect(screen.getByLabelText('Card footer')).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('handles empty card', () => {
      const { container } = render(<Card />);
      expect(container.firstChild).toBeInTheDocument();
      expect(container.firstChild).toBeEmptyDOMElement();
    });

    it('handles empty header', () => {
      const { container } = render(<CardHeader />);
      expect(container.firstChild).toBeInTheDocument();
      expect(container.firstChild).toBeEmptyDOMElement();
    });

    it('handles null children', () => {
      render(
        <Card>
          {null}
          <CardContent>Content</CardContent>
        </Card>
      );

      expect(screen.getByText('Content')).toBeInTheDocument();
    });

    it('handles conditional rendering', () => {
      const showDescription = false;
      render(
        <Card>
          <CardHeader>
            <CardTitle>Title</CardTitle>
            {showDescription && <CardDescription>Description</CardDescription>}
          </CardHeader>
        </Card>
      );

      expect(screen.getByText('Title')).toBeInTheDocument();
      expect(screen.queryByText('Description')).not.toBeInTheDocument();
    });
  });

  describe('Multiple Refs', () => {
    it('allows refs on all components simultaneously', () => {
      const cardRef = React.createRef<HTMLDivElement>();
      const headerRef = React.createRef<HTMLDivElement>();
      const titleRef = React.createRef<HTMLParagraphElement>();
      const descRef = React.createRef<HTMLParagraphElement>();
      const contentRef = React.createRef<HTMLDivElement>();
      const footerRef = React.createRef<HTMLDivElement>();

      render(
        <Card ref={cardRef}>
          <CardHeader ref={headerRef}>
            <CardTitle ref={titleRef}>Title</CardTitle>
            <CardDescription ref={descRef}>Description</CardDescription>
          </CardHeader>
          <CardContent ref={contentRef}>Content</CardContent>
          <CardFooter ref={footerRef}>Footer</CardFooter>
        </Card>
      );

      expect(cardRef.current).toBeInstanceOf(HTMLDivElement);
      expect(headerRef.current).toBeInstanceOf(HTMLDivElement);
      expect(titleRef.current).toBeInstanceOf(HTMLHeadingElement);
      expect(descRef.current).toBeInstanceOf(HTMLParagraphElement);
      expect(contentRef.current).toBeInstanceOf(HTMLDivElement);
      expect(footerRef.current).toBeInstanceOf(HTMLDivElement);
    });
  });

  describe('Real-world Examples', () => {
    it('renders product card', () => {
      render(
        <Card>
          <CardHeader>
            <CardTitle>Premium Plan</CardTitle>
            <CardDescription>Best for growing teams</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">$49/mo</div>
            <ul>
              <li>Unlimited projects</li>
              <li>24/7 support</li>
            </ul>
          </CardContent>
          <CardFooter>
            <button>Subscribe</button>
          </CardFooter>
        </Card>
      );

      expect(screen.getByText('Premium Plan')).toBeInTheDocument();
      expect(screen.getByText('Best for growing teams')).toBeInTheDocument();
      expect(screen.getByText('$49/mo')).toBeInTheDocument();
      expect(screen.getByText('Subscribe')).toBeInTheDocument();
    });

    it('renders notification card', () => {
      render(
        <Card>
          <CardHeader>
            <CardTitle>New Message</CardTitle>
            <CardDescription>2 minutes ago</CardDescription>
          </CardHeader>
          <CardContent>
            <p>You have a new message from Alice</p>
          </CardContent>
        </Card>
      );

      expect(screen.getByText('New Message')).toBeInTheDocument();
      expect(screen.getByText('2 minutes ago')).toBeInTheDocument();
      expect(screen.getByText('You have a new message from Alice')).toBeInTheDocument();
    });
  });
});
