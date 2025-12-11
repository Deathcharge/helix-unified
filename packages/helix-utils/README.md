# @helix/utils

🌀 Helix-branded utility functions for CSS class management

Replaces: `clsx`, `tailwind-merge`, `class-variance-authority`

## Installation

```bash
npm install @helix/utils
# or
yarn add @helix/utils
```

## Usage

### `cn()` - Combine and Merge Classes

Combines class names with Tailwind CSS conflict resolution:

```typescript
import { cn } from '@helix/utils';

// Basic usage
cn('px-4 py-2', 'bg-blue-500');
// => 'px-4 py-2 bg-blue-500'

// Handles conflicts - later classes win
cn('px-4 py-2', 'px-6');
// => 'py-2 px-6'

// Conditional classes
cn('base-class', condition && 'conditional-class');

// Object syntax
cn('base-class', {
  'active-class': isActive,
  'disabled-class': isDisabled
});
```

### `cva()` - Class Variance Authority

Create variant-based component styles:

```typescript
import { cva, type VariantProps } from '@helix/utils';

const button = cva({
  base: 'font-semibold border rounded',
  variants: {
    intent: {
      primary: 'bg-blue-500 text-white border-transparent',
      secondary: 'bg-white text-gray-800 border-gray-400',
    },
    size: {
      small: 'text-sm py-1 px-2',
      medium: 'text-base py-2 px-4',
      large: 'text-lg py-3 px-6',
    },
  },
  compoundVariants: [
    {
      intent: 'primary',
      size: 'large',
      class: 'uppercase',
    },
  ],
  defaultVariants: {
    intent: 'primary',
    size: 'medium',
  },
});

// Usage
button({ intent: 'secondary', size: 'large' });
// => 'font-semibold border rounded bg-white text-gray-800 border-gray-400 text-lg py-3 px-6'

// TypeScript support
type ButtonProps = VariantProps<typeof button>;
```

### Individual Functions

```typescript
import { clsx, twMerge } from '@helix/utils';

// clsx - combine class values
clsx('foo', 'bar'); // => 'foo bar'
clsx('foo', { bar: true }); // => 'foo bar'
clsx(['foo', 'bar']); // => 'foo bar'

// twMerge - merge with Tailwind conflict resolution
twMerge('px-4 py-2', 'px-6'); // => 'py-2 px-6'
```

## Features

- ✅ **Zero dependencies** - Pure TypeScript implementation
- 🔥 **Tiny bundle size** - ~2KB minified
- ⚡ **Fast** - Optimized for performance
- 🎯 **Type-safe** - Full TypeScript support
- 🌀 **Helix-branded** - Part of the Helix ecosystem

## API Reference

### `cn(...inputs: ClassValue[]): string`

Combines and merges class names with Tailwind conflict resolution.

### `clsx(...inputs: ClassValue[]): string`

Combines class names (replacement for the `clsx` package).

### `twMerge(...classLists: string[]): string`

Merges Tailwind classes with conflict resolution.

### `cva(config: VariantConfig): Function`

Creates a variant-based class name generator (replacement for `class-variance-authority`).

## License

MIT
