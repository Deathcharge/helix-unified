/**
 * 🌀 Helix Utils - CSS class management
 */
import clsx, { type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { cva, type VariantProps } from 'class-variance-authority';

/**
 * Combines and merges class names with Tailwind conflict resolution
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

// Re-export for backwards compatibility
export { type ClassValue, cva, type VariantProps };
