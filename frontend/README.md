# MedEase Frontend

This folder contains a functional static frontend built from the Stitch UI direction.

## How to open

Open `index.html` directly in a browser.

No npm install or dev server is required for the current mock version.

## Current features

- Main medical text explanation workspace
- English-first UI with Chinese display toggle
- Mock explanation adapter
- Example cases
- Inline medical term explanation popovers
- Mobile-friendly term sheet behavior through responsive CSS
- Safety notice, summary, risk/watch-for panel, next steps, technical detail collapse
- Feedback buttons with toast messages
- Local history stored in `localStorage`
- Session detail page
- Delete / clear history
- Export session JSON
- Empty, loading, insufficient-input, non-medical, and API-error fallback states

## Routes

The app uses hash routes so it can run as a static file:

- `#/`
- `#/history`
- `#/session/<session_id>`

## API mode placeholder

The app is currently wired to API mode through `index.html`. To switch back to mock mode, replace the inline runtime config with:

```html
<script>
  window.MEDEASE_API_MODE = "mock";
</script>
```

To use the local backend, keep:

```html
<script>
  window.MEDEASE_API_MODE = "api";
  window.MEDEASE_API_ENDPOINT = "http://127.0.0.1:8000/api/explain";
</script>
```

The API must return the same normalized session structure used in `app.js`.
