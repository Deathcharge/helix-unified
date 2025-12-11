/**
 * 🧪 Transitions Component Tests
 * Comprehensive tests for all transition/animation components
 */

import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import {
  Transition,
  FadeTransition,
  SlideTransition,
  ScaleTransition,
  BlurTransition,
  ConsciousnessTransition,
  StaggerTransition,
  PageTransition,
  ModalTransition,
  CollapseTransition,
} from '@/components/ui/Transitions';
import React from 'react';

describe('Transitions', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  describe('FadeTransition', () => {
    it('renders children when show is true', () => {
      render(
        <FadeTransition show={true}>
          <div>Fade Content</div>
        </FadeTransition>
      );
      expect(screen.getByText('Fade Content')).toBeInTheDocument();
    });

    it('applies full opacity when shown', () => {
      const { container } = render(
        <FadeTransition show={true}>
          <div>Content</div>
        </FadeTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper).toHaveClass('opacity-100');
    });

    it('applies zero opacity when hidden', () => {
      const { container } = render(
        <FadeTransition show={false}>
          <div>Content</div>
        </FadeTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper).toHaveClass('opacity-0');
    });

    it('unmounts after duration when show becomes false', async () => {
      const { rerender } = render(
        <FadeTransition show={true} duration={300}>
          <div>Content</div>
        </FadeTransition>
      );

      expect(screen.getByText('Content')).toBeInTheDocument();

      rerender(
        <FadeTransition show={false} duration={300}>
          <div>Content</div>
        </FadeTransition>
      );

      // Should still be in DOM immediately
      expect(screen.getByText('Content')).toBeInTheDocument();

      // Fast-forward past duration
      act(() => {
        jest.advanceTimersByTime(300);
      });

      await waitFor(() => {
        expect(screen.queryByText('Content')).not.toBeInTheDocument();
      });
    });

    it('respects custom duration', () => {
      const { container } = render(
        <FadeTransition show={true} duration={500}>
          <div>Content</div>
        </FadeTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transitionDuration).toBe('500ms');
    });

    it('respects custom delay', () => {
      const { container } = render(
        <FadeTransition show={true} delay={200}>
          <div>Content</div>
        </FadeTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transitionDelay).toBe('200ms');
    });

    it('accepts custom className', () => {
      const { container } = render(
        <FadeTransition show={true} className="custom-class">
          <div>Content</div>
        </FadeTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper).toHaveClass('custom-class');
    });

    it('uses default duration of 300ms', () => {
      const { container } = render(
        <FadeTransition show={true}>
          <div>Content</div>
        </FadeTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transitionDuration).toBe('300ms');
    });

    it('uses default delay of 0ms', () => {
      const { container } = render(
        <FadeTransition show={true}>
          <div>Content</div>
        </FadeTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transitionDelay).toBe('0ms');
    });
  });

  describe('SlideTransition', () => {
    it('renders children when show is true', () => {
      render(
        <SlideTransition show={true}>
          <div>Slide Content</div>
        </SlideTransition>
      );
      expect(screen.getByText('Slide Content')).toBeInTheDocument();
    });

    it('slides from bottom (up) by default', () => {
      const { container } = render(
        <SlideTransition show={true}>
          <div>Content</div>
        </SlideTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transform).toBe('translateY(0)');
    });

    it('slides from top (down)', () => {
      const { container } = render(
        <SlideTransition show={true} direction="down">
          <div>Content</div>
        </SlideTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transform).toBe('translateY(0)');
    });

    it('slides from right (left)', () => {
      const { container } = render(
        <SlideTransition show={true} direction="left">
          <div>Content</div>
        </SlideTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transform).toBe('translateX(0)');
    });

    it('slides from left (right)', () => {
      const { container } = render(
        <SlideTransition show={true} direction="right">
          <div>Content</div>
        </SlideTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transform).toBe('translateX(0)');
    });

    it('applies transform when hidden', () => {
      const { container } = render(
        <SlideTransition show={false} direction="up">
          <div>Content</div>
        </SlideTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transform).toBe('translateY(100%)');
    });

    it('respects custom duration', () => {
      const { container } = render(
        <SlideTransition show={true} duration={400}>
          <div>Content</div>
        </SlideTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transitionDuration).toBe('400ms');
    });

    it('unmounts after duration when hidden', async () => {
      const { rerender } = render(
        <SlideTransition show={true} duration={300}>
          <div>Content</div>
        </SlideTransition>
      );

      rerender(
        <SlideTransition show={false} duration={300}>
          <div>Content</div>
        </SlideTransition>
      );

      act(() => {
        jest.advanceTimersByTime(300);
      });

      await waitFor(() => {
        expect(screen.queryByText('Content')).not.toBeInTheDocument();
      });
    });
  });

  describe('ScaleTransition', () => {
    it('renders children when show is true', () => {
      render(
        <ScaleTransition show={true}>
          <div>Scale Content</div>
        </ScaleTransition>
      );
      expect(screen.getByText('Scale Content')).toBeInTheDocument();
    });

    it('applies full scale and opacity when shown', () => {
      const { container } = render(
        <ScaleTransition show={true}>
          <div>Content</div>
        </ScaleTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper).toHaveClass('scale-100');
      expect(wrapper).toHaveClass('opacity-100');
    });

    it('applies reduced scale and opacity when hidden', () => {
      const { container } = render(
        <ScaleTransition show={false}>
          <div>Content</div>
        </ScaleTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper).toHaveClass('scale-95');
      expect(wrapper).toHaveClass('opacity-0');
    });

    it('respects custom duration', () => {
      const { container } = render(
        <ScaleTransition show={true} duration={250}>
          <div>Content</div>
        </ScaleTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transitionDuration).toBe('250ms');
    });
  });

  describe('BlurTransition', () => {
    it('renders children when show is true', () => {
      render(
        <BlurTransition show={true}>
          <div>Blur Content</div>
        </BlurTransition>
      );
      expect(screen.getByText('Blur Content')).toBeInTheDocument();
    });

    it('applies no blur when shown', () => {
      const { container } = render(
        <BlurTransition show={true}>
          <div>Content</div>
        </BlurTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.filter).toBe('blur(0px)');
      expect(wrapper.style.opacity).toBe('1');
    });

    it('applies blur when hidden', () => {
      const { container } = render(
        <BlurTransition show={false}>
          <div>Content</div>
        </BlurTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.filter).toBe('blur(10px)');
      expect(wrapper.style.opacity).toBe('0');
    });

    it('uses default duration of 500ms', () => {
      const { container } = render(
        <BlurTransition show={true}>
          <div>Content</div>
        </BlurTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transitionDuration).toBe('500ms');
    });
  });

  describe('ConsciousnessTransition', () => {
    it('renders children when show is true', () => {
      render(
        <ConsciousnessTransition show={true}>
          <div>Consciousness Content</div>
        </ConsciousnessTransition>
      );
      expect(screen.getByText('Consciousness Content')).toBeInTheDocument();
    });

    it('applies full styles when shown', () => {
      const { container } = render(
        <ConsciousnessTransition show={true}>
          <div>Content</div>
        </ConsciousnessTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.opacity).toBe('1');
      expect(wrapper.style.transform).toBe('translateY(0) scale(1)');
      expect(wrapper.style.filter).toBe('blur(0px) brightness(1)');
    });

    it('applies reduced styles when hidden', () => {
      const { container } = render(
        <ConsciousnessTransition show={false}>
          <div>Content</div>
        </ConsciousnessTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.opacity).toBe('0');
      expect(wrapper.style.transform).toBe('translateY(20px) scale(0.95)');
      expect(wrapper.style.filter).toBe('blur(5px) brightness(0.7)');
    });

    it('uses cubic-bezier timing function', () => {
      const { container } = render(
        <ConsciousnessTransition show={true}>
          <div>Content</div>
        </ConsciousnessTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transitionTimingFunction).toBe('cubic-bezier(0.4, 0, 0.2, 1)');
    });

    it('uses default duration of 600ms', () => {
      const { container } = render(
        <ConsciousnessTransition show={true}>
          <div>Content</div>
        </ConsciousnessTransition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transitionDuration).toBe('600ms');
    });
  });

  describe('Transition (Unified)', () => {
    it('uses fade transition by default', () => {
      const { container } = render(
        <Transition show={true}>
          <div>Content</div>
        </Transition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper).toHaveClass('opacity-100');
    });

    it('renders fade transition when type is fade', () => {
      const { container } = render(
        <Transition type="fade" show={true}>
          <div>Content</div>
        </Transition>
      );
      expect(container.firstChild).toHaveClass('opacity-100');
    });

    it('renders slide transition when type is slide', () => {
      const { container } = render(
        <Transition type="slide" show={true}>
          <div>Content</div>
        </Transition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper).toHaveClass('transition-transform');
    });

    it('renders scale transition when type is scale', () => {
      const { container } = render(
        <Transition type="scale" show={true}>
          <div>Content</div>
        </Transition>
      );
      expect(container.firstChild).toHaveClass('scale-100');
    });

    it('renders blur transition when type is blur', () => {
      const { container } = render(
        <Transition type="blur" show={true}>
          <div>Content</div>
        </Transition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.filter).toBe('blur(0px)');
    });

    it('renders consciousness transition when type is consciousness', () => {
      const { container } = render(
        <Transition type="consciousness" show={true}>
          <div>Content</div>
        </Transition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.filter).toContain('blur');
      expect(wrapper.style.filter).toContain('brightness');
    });

    it('passes through props to child transition', () => {
      const { container } = render(
        <Transition type="fade" show={true} duration={1000} delay={200}>
          <div>Content</div>
        </Transition>
      );
      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transitionDuration).toBe('1000ms');
      expect(wrapper.style.transitionDelay).toBe('200ms');
    });
  });

  describe('StaggerTransition', () => {
    it('renders all children', () => {
      render(
        <StaggerTransition>
          {[
            <div key="1">Child 1</div>,
            <div key="2">Child 2</div>,
            <div key="3">Child 3</div>,
          ]}
        </StaggerTransition>
      );

      expect(screen.getByText('Child 1')).toBeInTheDocument();
      expect(screen.getByText('Child 2')).toBeInTheDocument();
      expect(screen.getByText('Child 3')).toBeInTheDocument();
    });

    it('applies staggered delays to children', () => {
      const { container } = render(
        <StaggerTransition staggerDelay={100}>
          {[
            <div key="1">Child 1</div>,
            <div key="2">Child 2</div>,
            <div key="3">Child 3</div>,
          ]}
        </StaggerTransition>
      );

      const wrappers = container.querySelectorAll('.transition-opacity');
      expect(wrappers[0]).toHaveStyle({ transitionDelay: '0ms' });
      expect(wrappers[1]).toHaveStyle({ transitionDelay: '100ms' });
      expect(wrappers[2]).toHaveStyle({ transitionDelay: '200ms' });
    });

    it('uses fade transition by default', () => {
      const { container } = render(
        <StaggerTransition>
          {[<div key="1">Child 1</div>]}
        </StaggerTransition>
      );

      expect(container.querySelector('.opacity-100')).toBeInTheDocument();
    });

    it('accepts custom transition type', () => {
      const { container } = render(
        <StaggerTransition type="scale">
          {[<div key="1">Child 1</div>]}
        </StaggerTransition>
      );

      expect(container.querySelector('.scale-100')).toBeInTheDocument();
    });

    it('accepts custom className', () => {
      const { container } = render(
        <StaggerTransition className="custom-stagger">
          {[<div key="1">Child</div>]}
        </StaggerTransition>
      );

      expect(container.firstChild).toHaveClass('custom-stagger');
    });
  });

  describe('PageTransition', () => {
    it('renders children', () => {
      render(
        <PageTransition>
          <div>Page Content</div>
        </PageTransition>
      );

      expect(screen.getByText('Page Content')).toBeInTheDocument();
    });

    it('shows content after mounting', async () => {
      const { container } = render(
        <PageTransition>
          <div>Content</div>
        </PageTransition>
      );

      await waitFor(() => {
        const wrapper = container.querySelector('[style*="opacity"]') as HTMLElement;
        expect(wrapper?.style.opacity).toBe('1');
      });
    });

    it('uses consciousness transition', () => {
      const { container } = render(
        <PageTransition>
          <div>Content</div>
        </PageTransition>
      );

      const wrapper = container.querySelector('[style*="filter"]') as HTMLElement;
      expect(wrapper).toBeInTheDocument();
    });

    it('accepts custom className', () => {
      render(
        <PageTransition className="custom-page">
          <div>Content</div>
        </PageTransition>
      );

      const { container } = render(
        <PageTransition className="custom-page">
          <div>Test</div>
        </PageTransition>
      );

      expect(container.querySelector('.custom-page')).toBeInTheDocument();
    });
  });

  describe('ModalTransition', () => {
    it('renders nothing when closed', () => {
      const { container } = render(
        <ModalTransition isOpen={false}>
          <div>Modal Content</div>
        </ModalTransition>
      );

      expect(screen.queryByText('Modal Content')).not.toBeInTheDocument();
    });

    it('renders modal when open', () => {
      render(
        <ModalTransition isOpen={true}>
          <div>Modal Content</div>
        </ModalTransition>
      );

      expect(screen.getByText('Modal Content')).toBeInTheDocument();
    });

    it('renders backdrop when open', () => {
      const { container } = render(
        <ModalTransition isOpen={true}>
          <div>Modal</div>
        </ModalTransition>
      );

      const backdrop = container.querySelector('.bg-black\\/60');
      expect(backdrop).toBeInTheDocument();
    });

    it('calls onClose when backdrop is clicked', async () => {
      const onClose = jest.fn();
      const { container } = render(
        <ModalTransition isOpen={true} onClose={onClose}>
          <div>Modal</div>
        </ModalTransition>
      );

      const backdrop = container.querySelector('.bg-black\\/60');
      if (backdrop) {
        await userEvent.click(backdrop as HTMLElement);
        expect(onClose).toHaveBeenCalledTimes(1);
      }
    });

    it('uses scale transition for content', () => {
      const { container } = render(
        <ModalTransition isOpen={true}>
          <div>Modal</div>
        </ModalTransition>
      );

      const scaleWrapper = container.querySelector('.scale-100');
      expect(scaleWrapper).toBeInTheDocument();
    });

    it('uses fade transition for backdrop', () => {
      const { container } = render(
        <ModalTransition isOpen={true}>
          <div>Modal</div>
        </ModalTransition>
      );

      const fadeWrapper = container.querySelector('.opacity-100');
      expect(fadeWrapper).toBeInTheDocument();
    });

    it('has correct z-index layers', () => {
      const { container } = render(
        <ModalTransition isOpen={true}>
          <div>Modal</div>
        </ModalTransition>
      );

      const backdrop = container.querySelector('.z-40');
      const content = container.querySelector('.z-50');

      expect(backdrop).toBeInTheDocument();
      expect(content).toBeInTheDocument();
    });
  });

  describe('CollapseTransition', () => {
    it('renders children when open', () => {
      render(
        <CollapseTransition isOpen={true}>
          <div>Collapse Content</div>
        </CollapseTransition>
      );

      expect(screen.getByText('Collapse Content')).toBeInTheDocument();
    });

    it('renders children when closed (but height 0)', () => {
      render(
        <CollapseTransition isOpen={false}>
          <div>Collapse Content</div>
        </CollapseTransition>
      );

      // Content is in DOM but not visible
      expect(screen.getByText('Collapse Content')).toBeInTheDocument();
    });

    it('applies height 0 when closed', () => {
      const { container } = render(
        <CollapseTransition isOpen={false}>
          <div>Content</div>
        </CollapseTransition>
      );

      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.height).toBe('0px');
    });

    it('has overflow hidden', () => {
      const { container } = render(
        <CollapseTransition isOpen={true}>
          <div>Content</div>
        </CollapseTransition>
      );

      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper).toHaveClass('overflow-hidden');
    });

    it('respects custom duration', () => {
      const { container } = render(
        <CollapseTransition isOpen={true} duration={500}>
          <div>Content</div>
        </CollapseTransition>
      );

      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transitionDuration).toBe('500ms');
    });

    it('uses default duration of 300ms', () => {
      const { container } = render(
        <CollapseTransition isOpen={true}>
          <div>Content</div>
        </CollapseTransition>
      );

      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.transitionDuration).toBe('300ms');
    });

    it('updates height when toggling', () => {
      const { container, rerender } = render(
        <CollapseTransition isOpen={false}>
          <div>Content</div>
        </CollapseTransition>
      );

      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.style.height).toBe('0px');

      rerender(
        <CollapseTransition isOpen={true}>
          <div>Content</div>
        </CollapseTransition>
      );

      // Height should be set to scrollHeight (non-zero)
      expect(wrapper.style.height).not.toBe('0px');
    });
  });

  describe('Edge Cases', () => {
    it('handles null children gracefully', () => {
      render(<FadeTransition show={true}>{null}</FadeTransition>);
      // Should not crash
    });

    it('handles undefined children gracefully', () => {
      render(<FadeTransition show={true}>{undefined}</FadeTransition>);
      // Should not crash
    });

    it('handles rapid show/hide toggles', () => {
      const { rerender } = render(
        <FadeTransition show={true}>
          <div>Content</div>
        </FadeTransition>
      );

      rerender(
        <FadeTransition show={false}>
          <div>Content</div>
        </FadeTransition>
      );

      rerender(
        <FadeTransition show={true}>
          <div>Content</div>
        </FadeTransition>
      );

      expect(screen.getByText('Content')).toBeInTheDocument();
    });

    it('cleans up timers on unmount', () => {
      const { unmount } = render(
        <FadeTransition show={false} duration={1000}>
          <div>Content</div>
        </FadeTransition>
      );

      unmount();

      // Should not throw error
      act(() => {
        jest.advanceTimersByTime(1000);
      });
    });
  });
});
