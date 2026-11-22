# AGENTS.md — The Regulated Pulse

## 1. Project snapshot

The Regulated Pulse is a personal blog/podcast about healthcare, technology, law, and policy, created by Priya Chaudhari. It is a static site with no build step, no package manager, and no automated test suite.

Primary files:

- `index.html` — the entire SPA: home/blog, podcast, My Major, FAQ, About Me, legal modals, article bodies, podcast episode bodies, comments, annotations, audio, search, and most CSS/JS.
- `terms.html` — Terms & Conditions.
- `privacy.html` — Privacy Policy.
- `legal.css` — styling shared by legal pages.
- `cookie-consent.css` / `cookie-consent.js` — cookie preference banner and consent behavior.
- `firestore.rules` — Firestore access rules.
- `CNAME` — custom domain: `theregulatedpulse.com`.
- `post-*/index.html` — tiny redirect stubs to hash routes such as `/#post-ai`; do not add new folders per post.
- `tts-post-*.mp3` and `tts-timings.json` — pre-generated article read-aloud audio and timing data.
- `welcome-to-the-pulse.m4a` — browser-compatible AAC version of the welcome post audio.
- `A Giant Leap.m4a`, `UI-UX Design.m4a`, `Welcome to the Pulse.m4a`, `The Realities of Chronic Illness.m4a` — human-recorded audio assets. The original `Welcome to the Pulse.m4a` is ALAC and does not play in Chrome; use `welcome-to-the-pulse.m4a` instead.

Remote:

- GitHub: `https://github.com/priyac3126/regulated-pulse.git`
- Branch: `main`
- Hosting: GitHub Pages via the repository root and `CNAME`.
- Latest known commit when this file was written: `9acd427` (`Redesign as a top-down blog and remove side widgets and recommendations`).

## 2. User content rules — highest priority

- Do **not** create a new folder per blog post. Existing posts live inline in `index.html`; `post-*/index.html` files are only redirects. Never create `new-post/index.html`.
- When the user supplies article text, publish it **exactly** as given. Do not change wording, grammar, spelling, punctuation, phrasing, em dashes, or typos unless explicitly asked. Only change markup/layout around it.
- The user often asks for exact text replacements. Preserve their supplied punctuation and spelling even if it looks like a typo (for example `recieving`, double punctuation, or curly vs straight quotes).
- Do not silently “fix” content. If a change seems necessary, make only the requested change.
- Keep contact addresses consistent: `theregulatedpulse@gmail.com` for general/privacy; `Theregulatedpulsepodcast@gmail.com` for podcast inquiries.

## 3. Current design direction — do not undo

The site is a **top-down editorial blog**, not a dashboard with a left sidebar.

- Sticky top navigation, built by restyling the existing `.dashboard-sidebar`; the old left sidebar must stay gone.
- Default theme is **white**, not dark. New visitors should see a white page.
- **No gradients anywhere.** There is a global rule using `body#top * { background-image: none !important; }` plus additional cleanup. Do not add `linear-gradient`, `radial-gradient`, or background-image gradients. Keep the body `id="top"`.
- Palette: white surfaces, deep navy `#080b11` in dark mode, **saturated blue accent in dark mode**, **deeper blue accent in light mode**, gray borders, restrained category labels. Avoid rainbow card colors and neon glows.
- Typography:
  - Brand: Playfair Display.
  - Section/card/article headings: Source Serif 4.
  - UI/navigation/meta: Plus Jakarta Sans.
  - Article/legal body copy: Source Serif 4.
- Layout:
  - Header row: brand left, horizontal nav right.
  - Main content max-width roughly `1180px`, centered.
  - Blog articles: first article is a full-width featured card, then articles in a 2-column grid.
  - `Vital Signs`: 2-column grid.
  - Podcast episodes: 3-column grid.
  - Newsletter signup: centered below the article grid, presented as an open rule with an underlined email field and a compact submit button, not a card.
  - Podcast “Listen & Subscribe” links are quiet inline links with small official brand dots, not bordered pills.
  - On screens below `800px`, nav icons are hidden so all five top-nav labels fit without horizontal clipping.
- Removed from the page and should not be restored unless explicitly asked:
  - The Editor corner card.
  - On the Shelf widget.
  - “Recommended for You” / “Personalized Picks” for both blog and podcast.
  - The mobile bottom dock (hidden; top nav is used on mobile too).
  - The old reader toolbar tabs (`A−`, multiplier, `A+`, Wide Spacing, Focus Mode).
  - The podcast transcript/chapter box.
- Article/podcast cards:
  - Flat white surface, thin gray border, small radius, no shadow, no gradient.
  - Category label is small uppercase accent text with a small accent square: saturated blue `#7dacfa` in dark mode, deeper blue final `#1d4ed8` in light mode.
  - The old `tag-*` classes still exist in markup but are visually overridden by `.card-premium > span`; edit the override if changing card-label colors.
  - Card hover/focus uses a subtle border change and slight lift, not a gradient.
- The current CSS redesign override block is appended near the end of the main `<style>` block. Add new rules there or later, and verify them in both themes.

## 3a. Color theory and usage

The site follows a restrained editorial 60/30/10 color model:

- **60% surface:** dark `#080b11` or light final light grey `#f0f3f8` (source `#0a0d12`). Cards and the sticky header stay white for separation. Keep large areas quiet and neutral.
- **30% type and structure:** `#f1f5f9` for primary type, `#9fadc1` for secondary text, `#1f2937` for dark borders, `#16181c` source for light borders.
- **10% accent:** dark mode saturated blue `#7dacfa`; light mode deeper blue `#1d4ed8` final (`#81b2ff` pre-filter source).

Accent semantics:

- **Dark mode blue** is a saturated blue sampled from the “Follow Along: On” label.  Use it for links, active nav, category squares/labels, focus rings, small underlines, and accent borders.
- **Light mode blue** is the deeper equivalent accent. Do not substitute green or deeper teal in either theme.
- **Stay in the blue family.** Keep the intentional saturated blue in dark mode; do not drift back to green, turquoise, or deep teal. `/tmp` screenshots and DevTools are the source of truth because the light-mode invert filter changes rendered colors.
- Dark-mode blue hover: `#95c3fb`. Deep blue for a pressed or high-emphasis fill if needed: `#4f8fa8`. Avoid large accent fills; the accent should act like ink, not paint.
- Dark-mode neutrals form a tight ladder: page/card `#080b11`, subtle raised surface `#0b1220`, border `#1f2937`, muted text `#9fadc1`, primary text `#f1f5f9`. Do not introduce unrelated grays.
- Light-mode source colors must be chosen for the invert filter: white final comes from `#000`, light border final comes from `#16181c`, blue final comes from `#81b2ff`, near-black type comes from `#f1f5f9`.
- Treat blue as a **cool, clinical signal**. Dark mode uses the lighter cyan-blue tone; light mode uses the deeper blue tone. Do not introduce a second competing accent.
- Use the accent in short strokes: a square, a rule, a label, an underline, an active indicator, a focus ring. A single viewport band should usually contain only one accent moment.
- Official platform dots (YouTube red, Spotify green, Apple purple, Amazon blue, Pocket Casts red) are exempt because they are tiny brand identifiers. They are not part of the site accent system.
- Measured contrast: `#7dacfa` on `#080b11` is about 8.9:1; `#95c3fb` on `#080b11` is about 11.2:1; `#9fadc1` on `#080b11` is about 8.7:1; `#1d4ed8` on white is about 6.7:1. These are accessible for body and UI text.
- Aim for at least 4.5:1 for normal text and 3:1 for large text, icons, borders, and focus indicators. Never use accent color as the only way to communicate state.
- Borders should stay low-contrast in their resting state and become accent-colored only on hover/focus.
- No gradients. No glow effects. No rainbow category colors. The accent should feel clinical and editorial, not decorative.
- The `ui-ux-pro-max` skill is available in `.opencode/skills/ui-ux-pro-max/`. Use it for color, typography, interaction, and accessibility checks, but keep this site's established tokens rather than copying a generic palette.

Interaction hierarchy:

- Prefer **inline text links** with underlines, arrows, and small accent marks over large filled buttons.
- Filled buttons are reserved for true actions: newsletter submit, cookie choices, auth, comment submit. Keep them compact, not full-width billboards.
- Secondary actions should be quiet text links, not outlined boxes.
- Cards are flat content surfaces, not button-shaped panels. Keep small radii and hairline borders; avoid shadows, pills, and capsule containers for primary navigation.
- Search fields should read as editorial rules/underlines rather than rounded input boxes.

## 4. Critical light-mode color mechanics

This is the most important implementation detail.

The site was originally dark-first. In default light mode, the `<html>` element receives:

```css
filter: invert(1) hue-rotate(180deg);
```

That means CSS source colors are **pre-filter** colors, not the visible final colors. Examples of source → final:

- `#000` → white
- `#0a0d12` → light grey page canvas (`#f0f3f8`)
- `#16181c` → light gray border
- `#81b2ff` → blue accent (~`#1d4ed8`)
- `#f1f5f9` → near-black text
- `#9fadc1` → muted gray text

Dark mode has no filter, so colors render directly:

- Page/card surface: `#080b11`
- Resting border: `#1f2937`
- Primary text: `#f1f5f9`
- Muted text: `#9fadc1`
- Accent: `#7dacfa` (saturated blue, matching the Follow Along label)
- Accent hover: `#95c3fb`

When adding light-mode styles:

1. Choose the desired final color.
2. Invert/hue-map it mentally, or compute the pre-filter source.
3. Test with a screenshot. Do not assume a normal light-theme color will look correct.

Podcast light mode has its own local inversion rules. The outer page/canvas and header have been forced white; the podcast cards/sidebar use local inversion. Be careful when changing podcast backgrounds or navigation colors; test `#podcast` in light mode, not just the blog.

Dark mode uses solid `#080b11` backgrounds. Article/podcast cards use the same deep navy as the page background, with borders for separation.

## 5. Page/routing architecture

`index.html` is an SPA using hash routes:

- `#blog` (default)
- `#podcast`
- `#major`
- `#faq`
- `#about`
- `#post-<postId>` for articles
- `#episode-<epId>` for podcast episodes

The routing function is `navigateTo(hash)`. It hides/shows containers and updates the active nav state. Keep IDs stable:

- `section-blog`, `section-podcast`, `section-major`, `section-faq`, `section-about`
- `blog-list-view`, `blog-post-view`
- `podcast-list-view`, `podcast-episode-view`
- `mobile-tab-*` (hidden on current design, but markup exists)
- `tab-blog`, `tab-podcast`, `tab-major`, `tab-faq`, `tab-about`

Article IDs currently include:

`post-battlefield`, `post-art-cure`, `post-malpractice`, `post-cdc-interview`, `post-book-recs`, `post-compassion`, `post-migration`, `post-na`, `post-giant-leap`, `post-ai`, `post-welcome`, `post-pain-brokers`, `post-med-ed`, `post-epic`, `post-quote-spotlight`.

Podcast IDs: `ep1`–`ep8`.

## 6. Adding/editing articles or episodes

When adding an article, follow the existing inline SPA pattern:

1. Add its full content to a hidden `<article id="post-<id>-container">` in `index.html`.
2. Add its card to the article grid (`#recent-articles-list` or `#vital-signs-section`).
3. Add a click handler for the static card if needed (many cards have `card-<id>-click` IDs and explicit listeners).
4. Add an entry to `BLOG_POST_CATALOG` with `id`, `cardId`, `cat`, `cardClass`, `tagClass`, `tagLabel`, `title`, `subtitle`, and `date`.
5. Add key terms to `ARTICLE_SEMANTIC_CONCEPTS` so search works.
6. Add TOC anchors/search-related content if applicable.
7. If a new audio file is supplied, wire it as a static `.audio-player` with `data-src`; otherwise the site creates a Web Speech/Google Translate TTS player automatically.

For podcast episodes:

1. Add the episode card to `#podcast-list-view`.
2. Add the hidden detail `<article id="podcast-ep<id>-container">`.
3. Add a `PODCAST_EP_CATALOG` entry.
4. Add key terms to `PODCAST_SEMANTIC_CONCEPTS`.
5. Do **not** re-add the removed transcript/chapter box.

## 7. Search behavior

- Blog search: semantic/concept-aware. Uses `BLOG_POST_CATALOG`, `ARTICLE_SEMANTIC_CONCEPTS`, `CONCEPT_SYNONYM_GROUPS`, and `filterBlogCards`.
- Podcast search: uses `PODCAST_EP_CATALOG`, `PODCAST_SEMANTIC_CONCEPTS`, and `filterPodcastCards`.
- Search indexes are built from titles, metadata, curated key terms, and visible detail-card text.
- Podcast search input: `#podcast-search-input`; no-results message: `#podcast-no-results-msg`.
- Blog search input: `#blog-search-input`; no-results message: `#blog-no-results-msg`.

## 8. Cookies, consent, privacy, legal

The banner has three explicit choices:

- **Allow cookies** → `pulseCookieConsentV1 = 'all'`.
- **Essential only** → `'essential'`.
- **No cookies** → `'none'`.

Behavior:

- Before a choice, optional and functional storage writes are blocked.
- `Essential only` blocks optional preference storage but allows essential/functional features.
- `No cookies` also blocks functional storage (sign-in tokens/email state, comment-email state, saved accessibility settings); features may not work.
- The consent choice itself is stored in `localStorage` as essential storage; this is unavoidable if the site is to remember the refusal.
- MailerLite is **deferred** and only loaded after `Allow cookies`.
- The cookie banner is theme-aware. `cookie-consent.js` decides whether to add `.pulse-cookie-banner-light` based on `body.light-mode` / `.legal-page` and whether the global invert filter is active. Keep this behavior when editing the banner.
- `Cookie settings` footer links must call `data-cookie-settings`.
- Legal pages have `<body class="legal-page">` so their cookie banner uses the light treatment.

Privacy Policy is intentionally **concise**. The detailed cookie-example table was removed. Do not re-bloat the cookie section. Keep only essential disclosures: consent choice, optional vs functional storage, no advertising cookies, third-party cookie possibility, and how to change the choice.

The Terms & Conditions were also condensed. Avoid reintroducing duplicated “about the site” / “no professional advice” language.

## 9. Authentication and Apple sign-in

Firebase project: `regulated-pulse`.

Supported/implemented:

- Email-link sign-in.
- Email/password sign-in.
- Google sign-in.
- Apple sign-in code exists (`OAuthProvider('apple.com')`).

Apple is currently **not configured** in the Firebase project. The Identity Toolkit API returns `OPERATION_NOT_ALLOWED`. The site now preflights Apple availability and shows a friendly message instead of silently failing.

Do not claim Apple sign-in is working. To enable it, the owner must:

1. Join the Apple Developer Program.
2. Create a Services ID.
3. Enable Sign in with Apple and configure:
   - Domain: `regulated-pulse.firebaseapp.com`
   - Return URL: `https://regulated-pulse.firebaseapp.com/__/auth/handler`
4. Create a Sign in with Apple key (`.p8`) and note Team ID / Key ID.
5. In Firebase Authentication → Apple, enter the Services ID and OAuth code flow configuration.

The Firebase web API key is public client configuration in `index.html`; do not treat it as a server secret.

## 10. Audio

- Welcome post uses `./welcome-to-the-pulse.m4a` (AAC, ~0:54). The original ALAC file is not browser-compatible.
- Human-narrated posts:
  - A Giant Leap → `./A Giant Leap.m4a`
  - Beyond Compliance → `./UI-UX Design.m4a`
  - These two players have `data-volume-boost="1.75"`; playback uses a Web Audio gain node. Do not remove this unless asked.
- Pre-generated article audio uses `tts-post-<articleId>.mp3` plus `tts-timings.json` and `TTS_EXACT_DURATIONS`.
- Other article/podcast/page players use dynamic Google Translate TTS with a SpeechSynthesis fallback.
- The user has asked for voice-cloning to match Priya’s voice. This is **not implemented** because no local voice-cloning model/API key exists. Do not pretend it is done. An ElevenLabs or Google Cloud Custom Voice key (or similar) is required to regenerate narration in her voice.
- “Quote Spotlight” audio has been reported as awkwardly pronounced. It can be regenerated once a voice service is available.

## 11. Accessibility features

- UserWay-style accessibility menu/panel with persisted settings.
- Local storage key: `pulseA11ySettingsV1`.
- Timestamp key: `pulseA11ySettingsUpdatedAt`.
- Signed-in users sync accessibility settings to Firestore `userPrefs` fields:
  - `a11ySettings`
  - `a11ySettingsUpdatedAt`
- The accessibility trigger is hidden until the welcome animation has finished (`body.pulse-ready`).
- The accessibility panel can be dragged by its header and is clamped to the viewport.
- Keyboard shortcuts: `Ctrl/Cmd + U` toggles the accessibility panel, `Shift + L` switches to light mode, and `Shift + D` switches to dark mode. Ignore these shortcuts while typing in form fields or contenteditable elements.
- Image descriptions are a toggle in the accessibility panel and are **off by default**; the visible `img-a11y-desc` captions only display when `body.uw-image-descriptions` is active.
- Focus Reading mode, font scaling, spacing, dyslexia-friendly text, cursor/reading guide, image descriptions, keyboard shortcuts, and TTS follow-along exist. Do not remove accessibility behavior while restyling.
- The old reader toolbar tabs were intentionally removed; text-size/spacing/focus controls remain accessible via the accessibility panel.

## 12. Comments, highlights, and annotations

- Comments and highlights use Firestore.
- Comment form headings and labels were intentionally softened to `font-weight: 600` (heading) and `500` (labels).
- Post Comment buttons are solid blue (no gradient).
- Do not reintroduce the old comment button gradients.
- Annotation auth uses the existing Firebase auth modal. Keep IDs/handlers stable.
- Unsigned highlights and notes persist in localStorage under `pulseLocalAnnotationsV1`; restore them for the current post on load.
- Existing highlights can be given or edited a note from the highlight popup. Persist note edits locally and to Firestore when signed in.
- Password fields use an eye/eye-off toggle (`.pw-toggle`) instead of a text “Show” button.
- PDF export excludes related-post/comment sections; it offers an “Include my highlights and notes” checkbox and appends a “My Notes” section. PDF highlights print as backgrounds, not underlines.

## 13. Repo/deployment workflow

This repository is static. There is no build or test command.

- Primary repo root: current working directory.
- `regulated-pulse/` is an **ignored secondary clone** of the same remote. It is not tracked by the root repo.
- When editing site files, keep the mirror in sync by copying changed files into `regulated-pulse/`:
  - `index.html`, `terms.html`, `privacy.html`, `legal.css`, `cookie-consent.css`, `cookie-consent.js`, and audio assets if changed.
- Commit and push only when the user asks. When asked to push, stage only intended site files; never stage `.opencode/` (large local tooling, ~66 MB).
- No secrets should be committed. The Firebase web config is public client configuration.
- Commit style: concise, descriptive, sentence case, e.g. `Redesign as a top-down blog and remove side widgets and recommendations`.

Typical push:

```bash
git status --short
git diff --check
git add index.html privacy.html terms.html legal.css cookie-consent.css cookie-consent.js
git commit -m "Describe the change"
git push origin main
```

## 14. Preview and verification

No test framework. Use static checks and headless Chrome.

```bash
node --check cookie-consent.js
python3 -m http.server 8788
```

Open `http://127.0.0.1:8788/index.html`.

Headless Chrome screenshots are useful:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --user-data-dir=/tmp/pulse-check \
  --window-size=1440,1000 --virtual-time-budget=9000 \
  --screenshot=/tmp/pulse-check.png \
  http://127.0.0.1:8788/index.html
```

Notes:

- Headless Chrome enforces a minimum CSS viewport around 500px. A 375px screenshot may crop content; confirm real responsive behavior with CDP device emulation or at 500px.
- Check both `#blog` and `#podcast` in light mode, plus dark mode after forcing body class removal.
- Search for accidental gradients:
  - Manually inspect background-image rules.
  - In DevTools, scan elements where `getComputedStyle(el).backgroundImage !== 'none'`.
  - The current global kill rule is `body#top * { background-image: none !important; }`; specific later `!important` rules can still win, so verify computed styles.
- Validate local links with a script or manual check after adding pages/assets.
- Test the welcome audio plays after opening the welcome post; test the 3 cookie choices and MailerLite loading only after Allow.

## 15. Known pitfalls / do not do

- Do not add gradients anywhere.
- Do not bring back the left sidebar, Editor corner, On the Shelf, Recommended for You, bottom mobile dock, transcript box, or old reader tabs.
- Do not use raw light-theme colors without accounting for the light-mode invert filter.
- Do not use green or deep teal as the dark-mode accent. Dark mode uses saturated blue `#7dacfa`; light mode uses deeper blue `#1d4ed8` final.
- Do not reintroduce large filled button boxes or pill-shaped primary navigation. Prefer inline text links, underlines, and compact action buttons.
- Keep the live contact address as `theregulatedpulse@gmail.com` for general and privacy inquiries.
- Do not change article wording, punctuation, or typos without explicit permission.
- Do not create post folders.
- Do not claim Apple sign-in works until Firebase + Apple provider configuration is complete.
- Do not claim voice cloning is complete; no cloning service is configured.
- Do not commit `.opencode/`.
- Do not re-bloat the privacy policy cookie section.
- Do not use emojis as UI icons.
- Do not remove the body `id="top"`; the no-gradient cleanup depends on it.
- Do not add new `!important` gradient rules without checking the global background-image kill and specificity.
- Do not assume the old `tag-*` colors control current card labels; the redesign override uses `.card-premium > span`.
- Do not add new `@import` font gradients or external background-image assets.

## 16. Current known state

- White top-down blog design is live, with a light grey page canvas and white content surfaces.
- Top nav replaces the old left sidebar.
- Dark-mode accent is saturated blue `#7dacfa`; light-mode accent is deeper blue `#1d4ed8` final.
- Hero actions, search, and newsletter use text/underline treatments instead of large filled boxes.
- Editor, On the Shelf, Recommended for You, and transcript box are removed/hidden.
- No gradients remain in the intended UI; verify after any new styles.
- General and privacy contact email is `theregulatedpulse@gmail.com`.
- Privacy policy and Terms are condensed.
- Cookie banner has 3 options and defers MailerLite.
- Welcome audio is fixed with AAC.
- A Giant Leap and Beyond Compliance have 75% volume boost.
- Apple provider remains disabled.
- Voice cloning remains unavailable.
