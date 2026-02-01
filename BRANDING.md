# TaskFlow - Brand Guidelines

## Logo

### Logo Overview
The TaskFlow logo is a modern, minimalist checkmark enclosed in a circle with green accent color. The design represents task completion, organization, and productivity.

**Design Principles:**
- Clean and simple
- Scalable to any size (SVG format)
- Works in both light and dark contexts
- Communicates completion and trust

### Logo Files

| File | Purpose | Location | Format |
|------|---------|----------|--------|
| `logo.svg` | Full logo for marketing, OG images, large displays | `/frontend/public/logo.svg` | SVG (scalable) |
| `favicon.ico` | Primary browser tab icon (universally supported) | `/frontend/public/favicon.ico` | ICO (16x16px) |
| `favicon.svg` | Modern browser fallback favicon | `/frontend/public/favicon.svg` | SVG (64x64px) |

### Logo Colors

**Primary Logo (on Black Background):**
- Background: `#0B0F0E` (Deep Black-Green)
- Accent: `#00E676` (Bright Green)
- Ring Stroke: `#00E676`
- Checkmark Stroke: `#00E676`

**Logo Usage Rules:**
- ✅ Use on dark backgrounds (primary use case)
- ✅ Use on white backgrounds (adjust colors if needed)
- ✅ Scale proportionally - never distort
- ✅ Maintain minimum 32px size for favicon
- ❌ Do not use other colors
- ❌ Do not rotate or flip
- ❌ Do not remove or alter design elements
- ❌ Do not add drop shadows or effects

### Logo Placement

**Header/Navigation:**
- Used in `/frontend/src/app/tasks/page.tsx` navigation bar
- Size: 40x40px (10x10 background)
- Color: Green (`#00E676`) background with black text "T"

**Favicon:**
- Automatically displayed in browser tabs
- Location: `/public/favicon.svg`
- Configured in Next.js metadata

**OpenGraph Image:**
- Used when sharing links on social media
- Location: `/public/logo.svg`
- Size: 200x200px

## Branding Colors

### Primary Color Palette (Black & Green)

| Element | Hex Value | RGB | Usage |
|---------|-----------|-----|-------|
| Primary Black-Green | `#0B0F0E` | 11, 15, 14 | Main backgrounds |
| Secondary Surface | `#111716` | 17, 23, 22 | Cards, containers |
| Elevated Surface | `#151C1B` | 21, 28, 27 | Modals, panels |
| Border/Divider | `#1F2A28` | 31, 42, 40 | Borders, lines |
| Primary Green | `#00E676` | 0, 230, 118 | Buttons, accents |
| Green Hover | `#00C965` | 0, 201, 101 | Hover states |
| Green Muted | rgba(0, 230, 118, 0.15) | - | Subtle backgrounds |
| Primary Text | `#E6F2EF` | 230, 242, 239 | Main text |
| Secondary Text | `#9FB3AD` | 159, 179, 173 | Labels, descriptions |
| Muted Text | `#6B7F7A` | 107, 127, 122 | Metadata, helpers |
| Danger | `#E5484D` | 229, 72, 77 | Errors, delete |

### Color Usage Guidelines

**Backgrounds:**
- Use `#0B0F0E` for main page backgrounds
- Use `#111716` for card and container backgrounds
- Use `#151C1B` for elevated surfaces (modals, dropdowns)

**Accents & Interactive Elements:**
- Use `#00E676` for primary buttons, links, and focus states
- Use `#00C965` for hover states on green elements
- Use `rgba(0, 230, 118, 0.15)` for subtle green backgrounds

**Text:**
- Use `#E6F2EF` for primary body text and headings
- Use `#9FB3AD` for secondary labels and descriptions
- Use `#6B7F7A` for metadata and helper text

**Status Indicators:**
- Use green (`#00E676`) for success, completed, in-progress
- Use `#E5484D` for danger, errors, delete actions (text/border only)
- Use neutral grays for pending, cancelled states

## Typography

### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto",
             "Helvetica Neue", "Arial", sans-serif;
```

### Type Scale

| Element | Font Size | Font Weight | Line Height | Usage |
|---------|-----------|------------|-------------|-------|
| H1 (Hero) | 56-64px | Bold (700) | 1.2 | Main page headings |
| H2 (Section) | 32-40px | Bold (700) | 1.2 | Section titles |
| H3 (Subsection) | 24-28px | Semibold (600) | 1.3 | Subsection titles |
| Large Text | 18-20px | Regular (400) | 1.5 | Body paragraphs |
| Body Text | 14-16px | Regular (400) | 1.5 | Main content |
| Small Text | 12-14px | Medium (500) | 1.4 | Labels, captions |
| Metadata | 11-12px | Regular (400) | 1.4 | Timestamps, helpers |

## Button Styles

### Primary Button
- Background: `#00E676`
- Text: `#0B0F0E` (black)
- Hover: `#00C965`
- Padding: `px-4 py-2.5`
- Border Radius: `rounded-lg` (8px)
- Font Weight: Medium (500)

### Secondary Button
- Background: Transparent
- Border: `2px solid #00E676`
- Text: `#00E676`
- Hover: `bg-[rgba(0,230,118,0.1)]` with `text-[#00C965]`
- Padding: `px-4 py-2.5`
- Border Radius: `rounded-lg` (8px)
- Font Weight: Medium (500)

### Danger Button
- Background: Transparent
- Border: `1px solid #E5484D` (optional)
- Text: `#E5484D`
- Hover: `text-[#FF6B6B]`
- Padding: `px-4 py-2.5`
- Border Radius: `rounded-lg` (8px)
- Font Weight: Medium (500)
- **Note:** No filled backgrounds for danger buttons

## Icons

### Icon Library
- **Icon Set:** Lucide React
- **Installation:** `npm install lucide-react`
- **Icon Size:** 16x16px (text), 20x20px (buttons), 24x24px (headers)

### Icon Color Guidelines
- **Active/Primary:** Use `#00E676` (primary green)
- **Inactive/Muted:** Use `#9FB3AD` (secondary text) or `#6B7F7A` (muted text)
- **Danger:** Use `#E5484D` (danger color)
- **Text:** Use same color as accompanying text

### Common Icons Used

| Icon | Usage |
|------|-------|
| CheckCircle2 | Completed status, success |
| Hourglass | Pending status, waiting |
| Rocket | In-progress status, active |
| Trash2 | Delete action |
| Edit2 | Edit action |
| Search | Search input |
| Plus | Add/create action |
| LogOut | Logout action |
| AlertTriangle | Error/warning |
| ClipboardList | Task/list |

## Web App Manifest

### Configuration
- **Name:** TaskFlow - Professional Task Management
- **Short Name:** TaskFlow
- **Theme Color:** `#0B0F0E`
- **Background Color:** `#0B0F0E`
- **Display Mode:** Standalone (PWA)

### Manifest Location
```
/public/manifest.json
```

### Features
- App shortcuts for "Create Task" and "View Tasks"
- PWA installation support
- iOS webapp capabilities
- Custom theme colors

## Favicon Setup

### Multiple Favicon Support
The application provides multiple favicon formats for maximum compatibility:

1. **ICO Favicon (Primary):** `/frontend/public/favicon.ico` ⭐
   - **Universally supported** across all browsers
   - Displays correctly in browser tabs, bookmarks, and history
   - Works in all development environments
   - No caching issues
   - Recommended as the primary favicon

2. **SVG Favicon (Fallback):** `/frontend/public/favicon.svg`
   - Modern browsers only
   - Highest quality, scalable
   - Used as fallback if .ico not available

3. **Apple Touch Icon:** `/frontend/public/logo.svg`
   - iOS home screen shortcut
   - iPad bookmark icon

### Meta Tags Configured
```html
<!-- Favicon - Primary .ico format (universally supported) -->
<link rel="icon" href="/favicon.ico?v=1" type="image/x-icon" />

<!-- Fallback SVG favicon for modern browsers -->
<link rel="icon" href="/favicon.svg?v=1" type="image/svg+xml" />

<!-- Apple Touch Icon -->
<link rel="apple-touch-icon" href="/logo.svg" />

<!-- Web App Manifest -->
<link rel="manifest" href="/manifest.json" />

<!-- Theme Color -->
<meta name="theme-color" content="#0B0F0E" />

<!-- iOS Webapp Capabilities -->
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
```

### Why .ico is Primary
- ✅ **Universal Support:** Works in 100% of browsers (old and new)
- ✅ **No Browser Inconsistencies:** SVG support varies across browsers and versions
- ✅ **Reliable Display:** Always shows in browser tabs, bookmarks, and history
- ✅ **No Caching Issues:** Binary format doesn't have the same caching problems as SVG
- ✅ **Developer Experience:** No favicon issues during development

## Implementation Checklist

### Logo & Favicon
- ✅ `logo.svg` created and placed in `/public/`
- ✅ `favicon.svg` created and placed in `/public/`
- ✅ Favicon configured in metadata
- ✅ Manifest file created with icon configuration

### Color System
- ✅ Black & Green color palette applied consistently
- ✅ All pages use the standard color palette
- ✅ No extraneous colors in the design
- ✅ Buttons follow the three-button system

### Metadata
- ✅ Enhanced metadata in `layout.tsx`
- ✅ Open Graph tags configured
- ✅ Twitter Card tags configured
- ✅ Theme colors set

### PWA Support
- ✅ Manifest.json configured
- ✅ App name and descriptions set
- ✅ App shortcuts configured
- ✅ Theme colors configured
- ✅ iOS webapp metadata configured

## Brand Voice

**Mission:** Help users organize and manage their tasks efficiently with a modern, trustworthy application.

**Core Values:**
- **Simple:** Clean, intuitive interface
- **Reliable:** Professional, enterprise-grade
- **Secure:** Trust in data protection
- **Productive:** Empower task management

## File Locations

```
/frontend/public/
├── logo.svg              # Full logo (200x200px, SVG)
├── favicon.ico           # Primary browser favicon (16x16px, ICO)
├── favicon.svg           # Modern browser favicon (64x64px, SVG fallback)
└── manifest.json         # PWA manifest configuration

/frontend/src/app/
└── layout.tsx            # Enhanced metadata and favicon links

/
├── BRANDING.md           # This branding guide
└── (other project files)
```

---

**Version:** 1.0
**Last Updated:** 2026-02-01
**Status:** Active
