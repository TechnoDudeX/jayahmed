# jayahmed.ca

Personal landing page for Jay Ahmed — Project Management Consultant (PMP, CSM, CSPO).

## Stack

Single-file static site. Vanilla HTML, CSS, and JS with inline styles and scripts. No build step.

- `index.html` — the page
- `headshot.jpg` — hero portrait
- `og-image.jpg` — Open Graph / social share image (regenerate with `generate_og.py`)

## Local development

```sh
python3 -m http.server 3000
```

Then open http://localhost:3000.

Or just open `index.html` directly in a browser.

## Deployment

Hosted on **Netlify**, auto-deploys on push to `main`.

Domain `jayahmed.ca` is registered with GoDaddy and points to Netlify via Netlify DNS (nameservers delegated at the registrar).
