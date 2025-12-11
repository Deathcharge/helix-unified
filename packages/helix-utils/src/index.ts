/**
 * 🌀 @helix/utils
 * Helix-branded utility functions for CSS class management
 * Replaces: clsx, tailwind-merge, class-variance-authority
 */

// ============================================================================
// CSS Class Utilities
// ============================================================================

export type ClassValue =
  | ClassValue[]
  | string
  | number
  | boolean
  | undefined
  | null
  | { [key: string]: any };

/**
 * Combines class names into a single string (replaces clsx)
 * @param inputs - Class values to combine
 * @returns Combined class string
 */
export function clsx(...inputs: ClassValue[]): string {
  const classes: string[] = [];

  for (let i = 0; i < inputs.length; i++) {
    const input = inputs[i];

    if (!input) continue;

    const inputType = typeof input;

    if (inputType === 'string' || inputType === 'number') {
      classes.push(String(input));
    } else if (Array.isArray(input)) {
      if (input.length) {
        const inner = clsx(...input);
        if (inner) classes.push(inner);
      }
    } else if (inputType === 'object') {
      for (const key in input as object) {
        if ((input as any)[key]) {
          classes.push(key);
        }
      }
    }
  }

  return classes.join(' ');
}

/**
 * Merges Tailwind CSS classes, handling conflicts intelligently
 * @param classLists - Class strings to merge
 * @returns Merged class string with conflicts resolved
 */
export function twMerge(...classLists: string[]): string {
  // Tailwind class conflict resolution
  // This is a simplified version - handles most common cases
  const classString = classLists.filter(Boolean).join(' ');
  const classes = classString.split(' ').filter(Boolean);

  // Track the last occurrence of each Tailwind utility type
  const classMap = new Map<string, string>();

  // Common Tailwind prefixes that should override each other
  const prefixes = [
    'bg-', 'text-', 'border-', 'rounded-', 'shadow-', 'p-', 'px-', 'py-', 'pt-', 'pb-', 'pl-', 'pr-',
    'm-', 'mx-', 'my-', 'mt-', 'mb-', 'ml-', 'mr-', 'w-', 'h-', 'min-w-', 'min-h-', 'max-w-', 'max-h-',
    'flex-', 'grid-', 'gap-', 'space-x-', 'space-y-', 'font-', 'leading-', 'tracking-', 'opacity-',
    'z-', 'top-', 'bottom-', 'left-', 'right-', 'inset-', 'overflow-', 'cursor-', 'transition-',
  ];

  for (const className of classes) {
    let prefix = '';

    // Find matching prefix
    for (const p of prefixes) {
      if (className.startsWith(p)) {
        prefix = p;
        break;
      }
    }

    // If we found a prefix, use it as key; otherwise use the full class name
    const key = prefix || className;
    classMap.set(key, className);
  }

  return Array.from(classMap.values()).join(' ');
}

/**
 * Combines and merges class names with Tailwind conflict resolution
 * @param inputs - Class values to combine and merge
 * @returns Merged class string
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

// ============================================================================
// Class Variance Authority (CVA) replacement
// ============================================================================

export type VariantProps<T extends (...args: any) => any> = Omit<
  Parameters<T>[0],
  'class' | 'className'
>;

type ConfigSchema = Record<string, Record<string, ClassValue>>;
type ConfigVariants<T extends ConfigSchema> = {
  [Variant in keyof T]?: keyof T[Variant] | null | undefined;
};
type ConfigCompoundVariants<T extends ConfigSchema> = Array<
  T extends ConfigSchema
    ? ConfigVariants<T> & {
        class?: ClassValue;
        className?: ClassValue;
      }
    : never
>;

export interface VariantConfig<V extends ConfigSchema> {
  base?: ClassValue;
  variants?: V;
  compoundVariants?: ConfigCompoundVariants<V>;
  defaultVariants?: ConfigVariants<V>;
}

/**
 * Creates a variant-based class name generator (replaces class-variance-authority)
 * @param config - Variant configuration
 * @returns Function that generates class names based on variant props
 */
export function cva<V extends ConfigSchema>(
  config: VariantConfig<V>
): (props?: ConfigVariants<V> & { class?: ClassValue; className?: ClassValue }) => string {
  return (props) => {
    const {
      base = '',
      variants = {} as V,
      compoundVariants = [],
      defaultVariants = {},
    } = config;

    const { class: className, className: classNameProp, ...variantProps } = props || {};

    // Start with base classes
    const classes: ClassValue[] = [base];

    // Add variant classes
    for (const variantName in variants) {
      const variantValue = (variantProps as any)[variantName] ?? (defaultVariants as any)[variantName];

      if (variantValue !== null && variantValue !== undefined) {
        const variantClasses = variants[variantName][variantValue as keyof typeof variants[typeof variantName]];
        if (variantClasses) {
          classes.push(variantClasses);
        }
      }
    }

    // Add compound variant classes
    for (const compoundVariant of compoundVariants) {
      const { class: compoundClass, className: compoundClassName, ...compoundVariantProps } = compoundVariant;

      let matches = true;
      for (const key in compoundVariantProps) {
        const propValue = (variantProps as any)[key] ?? (defaultVariants as any)[key];
        if (propValue !== (compoundVariantProps as any)[key]) {
          matches = false;
          break;
        }
      }

      if (matches) {
        classes.push(compoundClass, compoundClassName);
      }
    }

    // Add custom className props
    classes.push(className, classNameProp);

    return cn(...classes);
  };
}

// ============================================================================
// Export all utilities
// ============================================================================

export default {
  clsx,
  twMerge,
  cn,
  cva,
};
