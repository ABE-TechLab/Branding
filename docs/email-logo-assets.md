# Email-ready logo assets

This guide covers the transparent PNG exports in `public/logos/` and how to use their URLs after the Branding repository is deployed as a static Vercel project.

## Files and intended backgrounds

| File | Intended background | Export size | Suggested email display width |
| --- | --- | ---: | ---: |
| `abe-techlab-mark-light-v1.png` | White, off-white, or other light surfaces | 320 × 255 px | 160 px |
| `abe-techlab-mark-dark-v1.png` | Charcoal, black, or other dark surfaces | 320 × 255 px | 160 px |

Both PNG files have transparent backgrounds. The original SVG source files remain in `assets/logos/` and have not been modified. These PNGs are faithful raster exports of the current working SVG approximations; they do not establish that the underlying mark is final master artwork.

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

## Public image URLs

Replace `<production-domain>` with the actual Vercel production domain:

- Light background: `https://<production-domain>/logos/abe-techlab-mark-light-v1.png`
- Dark background: `https://<production-domain>/logos/abe-techlab-mark-dark-v1.png`

The Branding GitHub repository can remain private. The Vercel project must be configured to serve these static files publicly without deployment protection or authentication in front of the asset paths. Test each URL in a private/incognito browser window before using it in outbound email.

The URL remains stable while the production domain stays assigned to this project, the deployment remains available, and the asset path is not removed. For a future logo revision, publish a new versioned filename such as `abe-techlab-mark-light-v2.png` instead of overwriting a versioned file; update templates and brand-profile references deliberately.

## HTML example

Use the light variant when the logo sits on a light email surface:

```html
<a href="https://your-company.example">
  <img
    src="https://<production-domain>/logos/abe-techlab-mark-light-v1.png"
    alt="ABE TechLab"
    width="160"
    style="display:block;height:auto;border:0;outline:none;text-decoration:none;"
  >
</a>
```

For a dark email section, use `abe-techlab-mark-dark-v1.png` instead.

## ABEmail

In ABEmail, open **Settings → Brand Profile → Logo URL** and paste the image URL itself (not an HTML snippet). The designed-email renderer generates the HTML image element when it renders the brand profile.

A logo URL is only a stable source location; it cannot force every recipient's email client to show remote images. Recipients or email clients may still block remote images due to privacy or security settings. Keep useful alternative text and make sure the email still communicates the sender's identity without relying only on the image.
