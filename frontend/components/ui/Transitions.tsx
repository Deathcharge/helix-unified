"use client";

/**
 * ✨ Animated Transitions Component
 * Smooth animations for page transitions, fades, slides, and more
 */

import React, { ReactNode, useEffect, useState } from 'react';

export type TransitionType = 'fade' | 'slide' | 'scale' | 'blur' | 'consciousness';
export type SlideDirection = 'up' | 'down' | 'left' | 'right';

interface TransitionProps {
  /** Children to animate */
  children: ReactNode;
  /** Animation type */
  type?: TransitionType;
  /** Slide direction (for slide transition) */
  direction?: SlideDirection;
  /** Duration in milliseconds */
  duration?: number;
  /** Delay before animation starts */
  delay?: number;
  /** Show/hide trigger */
  show?: boolean;
  /** Custom className */
  className?: string;
}

/**
 * Fade Transition
 */
export const FadeTransition: React.FC<TransitionProps> = ({
  children,
  duration = 300,
  delay = 0,
  show = true,
  className = '',
}) => {
  const [shouldRender, setShouldRender] = useState(show);

  useEffect(() => {
    if (show) {
      setShouldRender(true);
    } else {
      const timer = setTimeout(() => setShouldRender(false), duration);
      return () => clearTimeout(timer);
    }
  }, [show, duration]);

  if (!shouldRender) return null;

  return (
    <div
      className={`transition-opacity ${show ? 'opacity-100' : 'opacity-0'} ${className}`}
      style={{
        transitionDuration: `${duration}ms`,
        transitionDelay: `${delay}ms`,
      }}
    >
      {children}
    </div>
  );
};

/**
 * Slide Transition
 */
export const SlideTransition: React.FC<TransitionProps> = ({
  children,
  direction = 'up',
  duration = 300,
  delay = 0,
  show = true,
  className = '',
}) => {
  const [shouldRender, setShouldRender] = useState(show);

  useEffect(() => {
    if (show) {
      setShouldRender(true);
    } else {
      const timer = setTimeout(() => setShouldRender(false), duration);
      return () => clearTimeout(timer);
    }
  }, [show, duration]);

  const transforms = {
    up: show ? 'translateY(0)' : 'translateY(100%)',
    down: show ? 'translateY(0)' : 'translateY(-100%)',
    left: show ? 'translateX(0)' : 'translateX(100%)',
    right: show ? 'translateX(0)' : 'translateX(-100%)',
  };

  if (!shouldRender) return null;

  return (
    <div
      className={`transition-transform ${className}`}
      style={{
        transform: transforms[direction],
        transitionDuration: `${duration}ms`,
        transitionDelay: `${delay}ms`,
      }}
    >
      {children}
    </div>
  );
};

/**
 * Scale Transition
 */
export const ScaleTransition: React.FC<TransitionProps> = ({
  children,
  duration = 300,
  delay = 0,
  show = true,
  className = '',
}) => {
  const [shouldRender, setShouldRender] = useState(show);

  useEffect(() => {
    if (show) {
      setShouldRender(true);
    } else {
      const timer = setTimeout(() => setShouldRender(false), duration);
      return () => clearTimeout(timer);
    }
  }, [show, duration]);

  if (!shouldRender) return null;

  return (
    <div
      className={`transition-transform ${show ? 'scale-100 opacity-100' : 'scale-95 opacity-0'} ${className}`}
      style={{
        transitionDuration: `${duration}ms`,
        transitionDelay: `${delay}ms`,
      }}
    >
      {children}
    </div>
  );
};

/**
 * Blur Transition (consciousness-themed)
 */
export const BlurTransition: React.FC<TransitionProps> = ({
  children,
  duration = 500,
  delay = 0,
  show = true,
  className = '',
}) => {
  const [shouldRender, setShouldRender] = useState(show);

  useEffect(() => {
    if (show) {
      setShouldRender(true);
    } else {
      const timer = setTimeout(() => setShouldRender(false), duration);
      return () => clearTimeout(timer);
    }
  }, [show, duration]);

  if (!shouldRender) return null;

  return (
    <div
      className={`transition-all ${className}`}
      style={{
        filter: show ? 'blur(0px)' : 'blur(10px)',
        opacity: show ? 1 : 0,
        transitionDuration: `${duration}ms`,
        transitionDelay: `${delay}ms`,
      }}
    >
      {children}
    </div>
  );
};

/**
 * Consciousness Transition (Helix-themed wave effect)
 */
export const ConsciousnessTransition: React.FC<TransitionProps> = ({
  children,
  duration = 600,
  delay = 0,
  show = true,
  className = '',
}) => {
  const [shouldRender, setShouldRender] = useState(show);

  useEffect(() => {
    if (show) {
      setShouldRender(true);
    } else {
      const timer = setTimeout(() => setShouldRender(false), duration);
      return () => clearTimeout(timer);
    }
  }, [show, duration]);

  if (!shouldRender) return null;

  return (
    <div
      className={`transition-all ${className}`}
      style={{
        opacity: show ? 1 : 0,
        transform: show ? 'translateY(0) scale(1)' : 'translateY(20px) scale(0.95)',
        filter: show ? 'blur(0px) brightness(1)' : 'blur(5px) brightness(0.7)',
        transitionDuration: `${duration}ms`,
        transitionDelay: `${delay}ms`,
        transitionTimingFunction: 'cubic-bezier(0.4, 0, 0.2, 1)',
      }}
    >
      {children}
    </div>
  );
};

/**
 * Unified Transition Component
 */
export const Transition: React.FC<TransitionProps> = ({ type = 'fade', ...props }) => {
  switch (type) {
    case 'fade':
      return <FadeTransition {...props} />;
    case 'slide':
      return <SlideTransition {...props} />;
    case 'scale':
      return <ScaleTransition {...props} />;
    case 'blur':
      return <BlurTransition {...props} />;
    case 'consciousness':
      return <ConsciousnessTransition {...props} />;
    default:
      return <FadeTransition {...props} />;
  }
};

/**
 * Stagger Children Transition
 * Animates children with staggered delays
 */
export const StaggerTransition: React.FC<{
  children: ReactNode[];
  staggerDelay?: number;
  type?: TransitionType;
  className?: string;
}> = ({ children, staggerDelay = 100, type = 'fade', className = '' }) => {
  return (
    <div className={className}>
      {React.Children.map(children, (child, index) => (
        <Transition type={type} delay={index * staggerDelay}>
          {child}
        </Transition>
      ))}
    </div>
  );
};

/**
 * Page Transition Wrapper
 * For Next.js page transitions
 */
export const PageTransition: React.FC<{
  children: ReactNode;
  className?: string;
}> = ({ children, className = '' }) => {
  const [show, setShow] = useState(false);

  useEffect(() => {
    setShow(true);
  }, []);

  return (
    <ConsciousnessTransition show={show} duration={600} className={className}>
      {children}
    </ConsciousnessTransition>
  );
};

/**
 * Modal Transition
 * For modal/overlay animations
 */
export const ModalTransition: React.FC<{
  children: ReactNode;
  isOpen: boolean;
  onClose?: () => void;
}> = ({ children, isOpen, onClose }) => {
  return (
    <>
      {/* Backdrop */}
      <FadeTransition show={isOpen} duration={200}>
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
          onClick={onClose}
        />
      </FadeTransition>

      {/* Modal Content */}
      <div className="fixed inset-0 flex items-center justify-center z-50 pointer-events-none">
        <ScaleTransition show={isOpen} duration={300}>
          <div className="pointer-events-auto">{children}</div>
        </ScaleTransition>
      </div>
    </>
  );
};

/**
 * Collapse Transition
 * Smooth height transitions
 */
export const CollapseTransition: React.FC<{
  children: ReactNode;
  isOpen: boolean;
  duration?: number;
}> = ({ children, isOpen, duration = 300 }) => {
  const [height, setHeight] = useState<number | 'auto'>(isOpen ? 'auto' : 0);
  const ref = React.useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current) {
      const scrollHeight = ref.current.scrollHeight;
      setHeight(isOpen ? scrollHeight : 0);
    }
  }, [isOpen]);

  return (
    <div
      ref={ref}
      className="overflow-hidden transition-all"
      style={{
        height,
        transitionDuration: `${duration}ms`,
      }}
    >
      {children}
    </div>
  );
};

export default Transition;
