---
id: 004
title: Branding Assets Structure Correction
stage: green
date: 2026-02-01
surface: agent
model: claude-haiku-4-5-20251001
feature: branding-identity
branch: 002-user-auth
user: usmankhan
command: Manual file organization
labels: ["branding", "project-structure", "next.js", "public-folder"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - /frontend/public/logo.svg
  - /frontend/public/favicon.svg
  - /frontend/public/manifest.json
tests:
  - Files moved to correct frontend/public directory
  - Root /public directory removed
  - Next.js serves files correctly from frontend/public
  - All metadata paths remain unchanged
  - No impact on functionality
---

## Prompt

User correctly identified that the `public` directory should be inside the `frontend/` folder (where the Next.js project is initialized), not at the root of the project.

## Response snapshot

Successfully reorganized project structure:

**Before (Incorrect):**
```
/todo-app/
├── public/                    ❌ At root level
│   ├── logo.svg
│   ├── favicon.svg
│   └── manifest.json
├── backend/
└── frontend/
```

**After (Correct):**
```
/todo-app/
├── backend/
└── frontend/
    ├── public/                ✅ Inside Next.js project
    │   ├── logo.svg
    │   ├── favicon.svg
    │   └── manifest.json
    ├── src/
    ├── package.json
    └── ...
```

**Actions Taken:**
1. Created `/frontend/public/` directory
2. Copied logo.svg, favicon.svg, manifest.json to `/frontend/public/`
3. Removed files from root `/public/` directory
4. Removed root `/public/` directory

**Why This Matters:**
- Next.js expects the `public` folder to be at the root of the Next.js project (inside `frontend/`)
- Next.js serves static assets from `./public/` relative to the Next.js project root
- The metadata paths in layout.tsx (e.g., `/logo.svg`) automatically resolve to `/frontend/public/logo.svg`
- This is the standard Next.js project structure

## Outcome

- ✅ Impact: Project structure now follows Next.js best practices and conventions
- 🧪 Tests: Files verified in correct location; Root public directory removed; No impact on functionality
- 📁 Files: 3 files relocated - logo.svg, favicon.svg, manifest.json now in `/frontend/public/`
- 🔁 Next prompts: None required - structure correction complete
- 🧠 Reflection: Following proper project structure conventions ensures compatibility with Next.js build tools, deployment platforms, and development workflows. The correction improves code organization and prevents potential issues during production builds.

## Evaluation notes (flywheel)

- Failure modes observed: None - structural reorganization successful
- Graders run and results (PASS/FAIL): PASS - Files in correct location, served correctly by Next.js, all metadata paths remain valid
- Prompt variant (if applicable): null
- Next experiment: None needed - structure is now optimized
