# 🌀 Helix Collective Frontend

**Version**: v16.3 Neti-Neti Harmony
**Framework**: Next.js 14 + React 18 + TypeScript
**Styling**: Tailwind CSS + Shadcn/ui

---

## 🚀 Quick Start

### Development

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: `http://localhost:3000`

### Production Build

```bash
npm run build
npm start
```

---

## 📁 Project Structure

```
frontend/
├── app/                      # Next.js App Router
│   ├── layout.tsx           # Root layout with Inter font
│   ├── globals.css          # Tailwind + CSS variables
│   └── rituals/
│       └── neti-neti/
│           └── page.tsx     # Neti-Neti ritual interface
├── components/
│   ├── NetiNetiHarmonyMantra.tsx  # Main ritual component
│   └── ui/                  # Shadcn/ui components
│       ├── button.tsx
│       └── card.tsx
├── lib/
│   └── utils.ts             # Utility functions (cn helper)
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
└── next.config.js
```

---

## 🎯 Features

### Neti-Neti Harmony Mantra Component

**Path**: `/rituals/neti-neti`

**Capabilities**:
- 🎵 ElevenLabs Music API integration
- 🔄 4-phase ritual tracking (Preparation → Mantra Loop → Integration → Grounding)
- 📝 6-section mantra structure with Sanskrit lyrics
- 🎚️ Audio playback controls with progress tracking
- 🌈 Gradient UI with Tailwind animations

**Backend Integration**:
- Proxies music generation requests to `/api/music/generate`
- Requires `ELEVENLABS_API_KEY` environment variable
- Generates ritual music from text prompts

---

## 🛠️ Configuration

### Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BACKEND_URL=http://localhost:8000
```

### API Proxy

Next.js automatically proxies `/api/*` requests to the FastAPI backend (configured in `next.config.js`).

---

## 🎨 UI Components

Using **Shadcn/ui** component library:
- Class Variance Authority (CVA) for variant management
- Radix UI primitives for accessibility
- Tailwind CSS for styling

### Available Components:
- `Button` - Variant-based button component
- `Card` - Container component with header/content/footer sections

---

## 🔗 Backend Integration

### FastAPI Endpoints Used:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/music/generate` | POST | Generate ritual music via ElevenLabs |
| `/ucf` | GET | Fetch UCF state metrics |
| `/agents` | GET | Get agent status |

---

## 📦 Dependencies

### Production:
- `react` ^18.2.0 - UI library
- `react-dom` ^18.2.0 - React DOM renderer
- `next` ^14.0.0 - React framework
- `lucide-react` ^0.292.0 - Icon library
- `@radix-ui/react-slot` ^1.0.2 - Composition primitive
- `class-variance-authority` ^0.7.0 - CVA for variants
- `clsx` ^2.0.0 - Class name utility
- `tailwind-merge` ^2.0.0 - Tailwind class merger

### Development:
- `typescript` ^5.0.0 - Type safety
- `tailwindcss` ^3.3.5 - Utility-first CSS
- `tailwindcss-animate` ^1.0.7 - Animation utilities
- `autoprefixer` ^10.4.16 - CSS vendor prefixing
- `postcss` ^8.4.31 - CSS processing

---

## 🧪 Testing

```bash
# Type check
npm run build

# Lint check
npm run lint
```

---

## 🚢 Deployment

### Railway (alongside FastAPI backend)

1. Build frontend as static export (optional)
2. Serve via FastAPI `/templates` endpoint
3. Or deploy separately with Vercel/Netlify

### Docker

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

---

## 📝 Development Notes

### Adding New UI Components

```bash
# Install Shadcn CLI (optional)
npx shadcn-ui@latest add [component-name]
```

### Tailwind Custom Classes

CSS variables defined in `app/globals.css`:
- `--background`, `--foreground`
- `--primary`, `--secondary`
- `--accent`, `--muted`
- Dark mode variants available

### TypeScript Paths

`@/*` resolves to project root:
```typescript
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
```

---

## 🌀 Ritual Integration

### Neti-Neti Component Flow

1. **User clicks "Generate Music"**
2. Component sends prompt to `/api/music/generate`
3. Backend proxies to ElevenLabs Music API
4. Audio streams back to component
5. Ritual phases progress automatically
6. Sanskrit mantras displayed with translations

---

## 🔐 Security

- ✅ API keys stored in backend environment only
- ✅ CORS configured in FastAPI
- ✅ Client-side requests proxied through Next.js
- ✅ No sensitive data in client bundle

---

**Status**: 🟢 **Ready for Development**

**Author**: Claude AI (Helix Collective)
**Version**: v16.3 Neti-Neti Harmony
**Last Updated**: 2025-11-06

🌀
