# Internationalization (i18n) Guide

## Overview

Helix Unified includes comprehensive internationalization support with locale-aware formatting for dates, numbers, and currencies across 16 languages.

## Supported Languages

- 🇺🇸 English (en)
- 🇨🇳 Chinese Simplified (zh-CN)
- 🇪🇸 Spanish (es)
- 🇮🇳 Hindi (hi)
- 🇸🇦 Arabic (ar)
- 🇵🇹 Portuguese (pt)
- 🇧🇩 Bengali (bn)
- 🇷🇺 Russian (ru)
- 🇯🇵 Japanese (ja)
- 🇫🇷 French (fr)
- 🇩🇪 German (de)
- 🇰🇷 Korean (ko)
- 🇮🇹 Italian (it)
- 🇹🇷 Turkish (tr)
- 🇻🇳 Vietnamese (vi)
- 🕉️ Sanskrit (sa)

## Architecture

### Core Components

1. **`frontend/lib/i18n.ts`** - i18next configuration
2. **`frontend/lib/formatters.ts`** - Intl API formatters
3. **`frontend/lib/use-formatters.ts`** - React hook for formatters
4. **`frontend/lib/language-context.tsx`** - Language state management
5. **`frontend/public/locales/`** - Translation files

## Using Formatters

### Date Formatting

```tsx
import { useFormatters } from '@/lib/use-formatters';

function MyComponent() {
  const formatters = useFormatters();

  const date = new Date('2025-12-12');

  return (
    <div>
      {/* Short format: 12/12/2025 */}
      <p>{formatters.formatDate(date)}</p>

      {/* Long format: December 12, 2025 */}
      <p>{formatters.formatDateLong(date)}</p>

      {/* With time: 12/12/2025, 3:45 PM */}
      <p>{formatters.formatDateTime(date)}</p>

      {/* Relative: 2 days ago */}
      <p>{formatters.formatRelativeTime(date)}</p>
    </div>
  );
}
```

### Number Formatting

```tsx
function NumberExamples() {
  const formatters = useFormatters();

  return (
    <div>
      {/* Standard number: 1,234.56 */}
      <p>{formatters.formatNumber(1234.56)}</p>

      {/* Compact: 1.2K */}
      <p>{formatters.formatCompact(1234)}</p>

      {/* Percentage: 45% */}
      <p>{formatters.formatPercent(0.45)}</p>

      {/* File size: 1.5 MB */}
      <p>{formatters.formatFileSize(1572864)}</p>

      {/* Duration: 1h 23m 45s */}
      <p>{formatters.formatDuration(5025)}</p>
    </div>
  );
}
```

### Currency Formatting

```tsx
function PricingComponent() {
  const formatters = useFormatters('USD');

  return (
    <div>
      {/* $1,234.56 */}
      <p>{formatters.formatCurrency(1234.56)}</p>

      {/* €1.234,56 (if user locale is German) */}
      <p>{formatters.formatCurrency(1234.56, 'EUR')}</p>
    </div>
  );
}
```

## Currency Mapping

Currencies are automatically selected based on user locale:

| Locale | Currency |
|--------|----------|
| en-US  | USD      |
| en-GB  | GBP      |
| es-ES  | EUR      |
| zh-CN  | CNY      |
| ja     | JPY      |
| hi     | INR      |
| ar-SA  | SAR      |

## Language Switching

### Using the Language Selector

```tsx
import { useLanguage } from '@/lib/language-context';

function LanguageSwitcher() {
  const { currentLanguage, changeLanguage, availableLanguages } = useLanguage();

  return (
    <select
      value={currentLanguage}
      onChange={(e) => changeLanguage(e.target.value)}
    >
      {availableLanguages.map(lang => (
        <option key={lang.code} value={lang.code}>
          {lang.nativeName}
        </option>
      ))}
    </select>
  );
}
```

### Backend Integration

Language preferences are automatically saved to the backend when changed:

```typescript
// Language change triggers API call to:
PATCH /auth/me/preferences
{
  "language": "es"
}
```

## Translation Files

### Structure

```
frontend/public/locales/
├── en/
│   └── common.json
├── es/
│   └── common.json
├── fr/
│   └── common.json
└── ...
```

### Example Translation File

```json
{
  "welcome": "Welcome to Helix",
  "dashboard": "Dashboard",
  "settings": "Settings",
  "billing": {
    "title": "Billing & Subscriptions",
    "upgrade": "Upgrade Plan",
    "cancel": "Cancel Subscription"
  }
}
```

### Using Translations

```tsx
import { useTranslation } from 'react-i18next';

function WelcomeMessage() {
  const { t } = useTranslation('common');

  return (
    <div>
      <h1>{t('welcome')}</h1>
      <p>{t('billing.title')}</p>
    </div>
  );
}
```

## Best Practices

### 1. Always Use Formatters

❌ **Don't:**
```tsx
<p>${amount.toFixed(2)}</p>
<p>{new Date(date).toLocaleDateString()}</p>
```

✅ **Do:**
```tsx
<p>{formatters.formatCurrency(amount)}</p>
<p>{formatters.formatDate(date)}</p>
```

### 2. Provide Context in Translations

❌ **Don't:**
```json
{
  "save": "Save"
}
```

✅ **Do:**
```json
{
  "actions": {
    "save": "Save",
    "save_and_continue": "Save and Continue"
  }
}
```

### 3. Handle RTL Languages

For Arabic and other RTL languages, consider layout adjustments:

```tsx
function Layout() {
  const { currentLanguage } = useLanguage();
  const isRTL = ['ar', 'he'].includes(currentLanguage);

  return (
    <div dir={isRTL ? 'rtl' : 'ltr'}>
      {/* content */}
    </div>
  );
}
```

### 4. Test with Multiple Locales

Always test your components with different locales:

```tsx
// In tests
import { createFormatters } from '@/lib/formatters';

describe('PriceDisplay', () => {
  it('formats USD correctly', () => {
    const formatters = createFormatters({ locale: 'en-US' });
    // Test with formatters
  });

  it('formats EUR correctly', () => {
    const formatters = createFormatters({ locale: 'de-DE' });
    // Test with formatters
  });
});
```

## Formatter API Reference

### Date Methods

- `formatDate(date)` - Short date (12/31/2025)
- `formatDateLong(date)` - Long date (December 31, 2025)
- `formatDateTime(date)` - Date with time
- `formatDateTimeLong(date)` - Long date with time
- `formatTime(date)` - Time only
- `formatRelativeTime(date)` - Relative time (2 days ago)

### Number Methods

- `formatNumber(value, options?)` - General number formatting
- `formatCurrency(value, currency?, options?)` - Currency formatting
- `formatPercent(value, options?)` - Percentage formatting
- `formatCompact(value)` - Compact notation (1.2K, 3.4M)
- `formatFileSize(bytes)` - Human-readable file sizes
- `formatDuration(seconds)` - Duration formatting

### Utility Methods

- `getLocale()` - Get current locale
- `getCurrency()` - Get current currency
- `getTimeZone()` - Get current timezone

## Server-Side Rendering (SSR)

For Next.js pages with SSR, use the standalone formatter:

```tsx
import { createFormatters } from '@/lib/formatters';

export async function getServerSideProps({ locale }) {
  const formatters = createFormatters({ locale });

  return {
    props: {
      formattedPrice: formatters.formatCurrency(99.99)
    }
  };
}
```

## Troubleshooting

### Missing translations

If a translation key is missing, it will display the key itself:

```tsx
// If 'new_feature' doesn't exist in translations
{t('new_feature')} // Displays: "new_feature"
```

### Wrong currency symbol

Ensure you're passing the correct currency code:

```tsx
// ✅ Correct
formatters.formatCurrency(99.99, 'EUR')

// ❌ Incorrect
formatters.formatCurrency(99.99, 'euro')
```

### Date formatting issues

Dates should be passed as Date objects, ISO strings, or timestamps:

```tsx
// All valid:
formatters.formatDate(new Date())
formatters.formatDate('2025-12-12')
formatters.formatDate(1734048000000)
```

## Adding New Languages

1. Create locale folder: `frontend/public/locales/[locale]/`
2. Add `common.json` with translations
3. Update `frontend/lib/language-context.tsx`:

```tsx
export const availableLanguages = [
  // ... existing languages
  { code: 'pl', name: 'Polish', nativeName: 'Polski' },
];
```

4. Update `frontend/next-i18next.config.js`:

```js
locales: [..., 'pl'],
```

5. Import in `frontend/lib/i18n.ts`:

```tsx
import plCommon from '@/public/locales/pl/common.json';

const resources = {
  // ... existing
  pl: { common: plCommon },
};
```

## Related Documentation

- [Subscription Management Guide](./SUBSCRIPTION_GUIDE.md)
- [Frontend Architecture](./FRONTEND_ARCHITECTURE.md)
- [API Reference](./API_REFERENCE.md)
