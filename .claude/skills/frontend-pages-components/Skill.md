---
name: frontend-pages-components
description: Build responsive frontend pages and reusable UI components with clean layout and modern styling.
---

# Frontend Pages & Components Development

## Instructions

1. **Page Structure**
   - Semantic HTML5 layout
   - Clear separation of sections (header, main, footer)
   - Consistent spacing and alignment

2. **Components**
   - Reusable UI components (buttons, cards, forms, navbars)
   - Component-based structure (React/Vue or vanilla HTML)
   - Props / variants for flexibility

3. **Layout**
   - Responsive grid or flexbox system
   - Mobile-first design
   - Proper use of containers and breakpoints

4. **Styling**
   - Modern CSS (Flexbox, Grid)
   - Utility-first or component-scoped styles
   - Consistent color palette and typography
   - Hover and focus states

## Best Practices
- Keep components small and reusable
- Follow mobile-first responsive design
- Maintain consistent spacing and typography
- Avoid inline styles; use classes
- Ensure accessibility (ARIA, contrast, keyboard navigation)

## Example Structure
```html
<main class="container">
  <section class="page-section">
    <h1 class="page-title">Page Title</h1>
    <div class="card-grid">
      <div class="card">
        <h2>Component Title</h2>
        <p>Reusable component content</p>
        <button class="btn-primary">Action</button>
      </div>
    </div>
  </section>
</main>
