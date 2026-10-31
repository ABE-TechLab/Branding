# Email-ready and adaptive logo assets

This guide covers the transparent PNG exports and adaptive SVG in `public/logos/`, including how to use their URLs after the Branding repository is deployed as a static Vercel project.

## Files and intended use

| File | Intended use | Export size / display size |
| --- | --- | --- |
| `abe-techlab-mark-adaptive.svg` | Websites, portfolio pages, and modern browser contexts that support SVG `prefers-color-scheme` | Vector; scales to display size |
| `abe-techlab-mark-light-v1.png` | Email and light-background contexts | 320 × 255 px; suggested 160 px display width |
| `abe-techlab-mark-dark-v1.png` | Email and dark-background contexts | 320 × 255 px; suggested 160 px display width |

The PNG files have transparent backgrounds. The original light and dark SVG source files remain in `assets/logos/` and have not been modified. The PNG and adaptive SVG are faithful derivatives of the current working SVG approximations; they do not establish that the underlying mark is final master artwork.

## Adaptive SVG behavior

The adaptive SVG is a single file. It uses the CSS `prefers-color-scheme` media feature internally:

- Light color scheme (the default): the main mark is charcoal (`#111111`).
- Dark color scheme: the main mark changes to off-white (`#F9F9F6`).
- Both schemes retain the lime accent (`#A7E021`).
- The canvas remains transparent.

When embedded with an `<img>` element, supported browsers can evaluate the SVG's media query using the user's preferred color scheme or the embedding page's inherited `color-scheme`. The exact behavior depends on the browser and the host renderer. Test the target browser/Markdown renderer; retain the separate light/dark variants wherever deterministic rendering is essential.

Example:

```html
<img
  src="https://<production-domain>/logos/abe-techlab-mark-adaptive.svg"
  alt="ABE TechLab"
  width="160"
  style="display:block;height:auto;border:0;"
>
```

A web page can also set the intended scheme for a particular embedded image using CSS:

```html
<div class="light-surface">
  <img src="/logos/abe-techlab-mark-adaptive.svg" alt="ABE TechLab">
</div>
<div class="dark-surface">
  <img src="/logos/abe-techlab-mark-adaptive.svg" alt="ABE TechLab">
</div>
```

```css
.light-surface { color-scheme: light; background: #fff; }
.dark-surface { color-scheme: dark; background: #111; }
```

The logo itself does not detect an arbitrary background color. It responds to the preferred/inherited color scheme supplied by the browser or embedding page.

## Email compatibility

Do not rely on the adaptive SVG for outbound email. Many email clients sanitize, proxy, or inconsistently render SVG and embedded CSS/media queries. Use the light or dark PNG variant selected for the email's actual background instead.

## Vercel project setup

Connect this repository to a Vercel project using these settings:

- Framework Preset: **Other**
- Root Directory: `./`
- Build Command: disabled / empty
- Output Directory: `public`
- Install Command: disabled / empty
- No environment variables are required.

Deploy the production branch. The `public/index.html` file becomes the root page and files inside `public/` are served from the deployment root.

Use the project's production domain or a custom domain assigned to the project. Do not use a preview deployment URL, a GitHub file page, a GitHub API download URL, or a URL containing a temporary token or signed query parameters.

## Public asset URLs

Replace `<production-domain>` with the actual Vercel production domain:

- Adaptive SVG: `https://<production-domain>/logos/abe-techlab-mark-adaptive.svg`
- Light PNG: `https://<production-domain>/logos/abe-techlab-mark-light-v1.png`
- Dark PNG: `https://<production-domain>/logos/abe-techlab-mark-dark-v1.png`

The Branding GitHub repository can remain private. The Vercel project must serve these static files publicly without deployment protection or authentication in front of the asset paths. Test each URL in a private/incognito browser window before using it in external websites or email.

The URLs remain stable while the production domain stays assigned to this project, the deployment remains available, and the asset paths are not removed. For future artwork revisions, publish versioned filenames (for example, `abe-techlab-mark-adaptive-v2.svg` or `abe-techlab-mark-light-v2.png`) instead of overwriting versioned files; update templates and brand-profile references deliberately.

## ABEmail

In ABEmail, open **Settings → Brand Profile → Logo URL** and paste the selected PNG image URL itself (not an HTML snippet). Use the light PNG on light email surfaces and the dark PNG on dark email surfaces. The designed-email renderer generates the HTML image element when it renders the brand profile.

A logo URL is only a stable source location; it cannot force every recipient's email client to show remote images. Recipients or email clients may still block remote images due to privacy or security settings. Keep useful alternative text and make sure the email still communicates the sender's identity without relying only on the image.
