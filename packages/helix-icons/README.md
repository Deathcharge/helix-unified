# @helix/icons

Custom icon set for the Helix Unified platform. Replaces `lucide-react` with brand-specific icons optimized for our design system.

## Installation

```bash
npm install @helix/icons
# or
yarn add @helix/icons
# or
pnpm add @helix/icons
```

## Usage

```tsx
import { HelixLogo, Dashboard, Agent, Brain } from '@helix/icons';

function MyComponent() {
  return (
    <div>
      <HelixLogo size={32} color="#6366f1" />
      <Dashboard size={24} />
      <Agent strokeWidth={1.5} />
      <Brain size={48} color="currentColor" />
    </div>
  );
}
```

## Available Icons

### Core Helix
- `HelixLogo` - Main Helix logo
- `HelixSpin` - Animated/loading variant
- `Agent` - Agent representation
- `Brain` - AI/Intelligence
- `Consciousness` - Consciousness analytics
- `Network` - Network/connections

### Navigation
- `Dashboard`, `Menu`, `Close`
- `ChevronLeft`, `ChevronRight`, `ChevronUp`, `ChevronDown`

### Actions
- `Plus`, `Minus`, `Edit`, `Trash`, `Copy`
- `Download`, `Upload`, `Search`, `Filter`, `Settings`

### Status
- `Check`, `Success`, `Error`, `Warning`, `Info`, `AlertCircle`

### Users & Communication
- `User`, `Users`, `UserPlus`
- `Mail`, `MessageCircle`, `Bell`

### Files
- `File`, `FileText`, `Folder`, `FolderOpen`

## Props

All icons accept the following props:

```tsx
interface IconProps {
  size?: number | string;      // Default: 24
  color?: string;              // Default: 'currentColor'
  strokeWidth?: number;        // Default: 2
  className?: string;
  style?: React.CSSProperties;
  // ... all standard SVG props
}
```

## Migration from lucide-react

```tsx
// Before
import { Home, User, Settings } from 'lucide-react';

// After
import { Dashboard, User, Settings } from '@helix/icons';
```

Most icon names are similar or identical. Key changes:
- `Home` → `Dashboard`
- `X` → `Close`
- Other icons map 1:1

## Development

```bash
# Build
npm run build

# Watch mode
npm run dev

# Type check
npm run type-check
```

## License

MIT © Helix Team
