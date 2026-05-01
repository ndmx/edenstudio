# EdenTV Design System

EdenTV uses a small web design system for static marketing, support, and developer documentation pages. The system borrows the discipline of Apple platform design: native-feeling controls, restrained surfaces, semantic color, clear typography, and accessible interaction states.

## Naming Model

Use three layers of class names:

- `site-*` for global shell components such as navigation, footer, page, and sections.
- `ds-*` for reusable design-system primitives such as buttons, cards, badges, document panels, and stat tiles.
- `page-*` for page-specific composition where a reusable component is not yet justified.

Legacy classes such as `navbar`, `panel-card`, `btn`, and `doc-list-item` remain as compatibility aliases while pages are migrated.

## Component Labels

Major reusable regions should include a semantic class and, where helpful, `data-component`.

Examples:

```html
<nav class="navbar site-header" data-component="site-header" aria-label="Primary navigation">
<section class="hero hero-full site-hero" data-component="site-hero">
<article class="panel-card ds-card ds-card--feature" data-component="feature-card">
<footer class="footer site-footer" data-component="site-footer">
```

This makes the HTML easier to scan, easier to test, and easier to map to design-system documentation.

## Visual Tokens

Tokens live in `css/styles.css`.

- `--color-*`: brand and semantic colors.
- `--surface-*`: page, raised, glass, and inset surfaces.
- `--text-*`: primary, secondary, muted, and inverse text.
- `--space-*`: spacing scale.
- `--radius-*`: shape scale.
- `--shadow-*`: elevation scale.
- `--motion-*`: timing and easing.

Keep new CSS semantic. Avoid adding raw hex colors inside feature-specific selectors.

## Brand

The primary wordmark remains `EdenTV`. The favicon and compact mark use a cursive `Etv` monogram.

Current brand asset:

`assets/brand/etv-favicon.svg`

## Interaction Principles

- One clear primary action per section.
- Links should look like links; buttons should be reserved for commands or strong calls to action.
- Hover and focus states must be visible.
- Motion should be subtle and respect `prefers-reduced-motion`.
- Mobile navigation must be keyboard dismissible and close on Escape.

## Accessibility

- Every icon-only control needs an accessible name.
- Navigation uses `aria-label="Primary navigation"`.
- The mobile menu button uses `aria-label`, `aria-controls`, and `aria-expanded`.
- Color meaning should be paired with text labels.
- Text sizes should use `clamp()` or responsive spacing, not viewport-width font scaling alone.

## Migration Rule

When editing an existing page, add the new semantic component class while leaving the old class in place until all CSS and JavaScript dependencies are removed.
