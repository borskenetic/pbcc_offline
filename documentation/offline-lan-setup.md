# Offline LAN setup (PBCC)

Run Pantas on a **library LAN server with no internet** after a one-time online install. Browsers on the LAN talk to the local Laravel app on the library PC. SMS and email are optional and not required for core workflows.

## One-time setup (while online)

```bash
composer install
npm install
npm run build
npm run build:tailwind
# npm install already runs copy-vendor; re-run if needed:
npm run copy-vendor
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan db:seed --class=MarcFrameworkSeeder
php artisan storage:link
```

After this, **Node.js is not required to serve** the app. Keep PHP, MySQL/MariaDB, and the web server on the library PC.

**PBCC recommended stack:** XAMPP on Windows. Put the project at `C:\xampp\htdocs\pbcc`, start Apache + MySQL in the XAMPP Control Panel, then run `php artisan serve --host=0.0.0.0 --port=8000` for LAN access. Full staff-facing steps: `documentation/PBCC-Library-System-Setup-Guide.docx`.

### What the asset commands do

| Command | Output |
|---------|--------|
| `npm install` / `npm run copy-vendor` | Copies Bootstrap, jQuery, icons, Chart.js, SweetAlert2, FullCalendar, fonts, qz-tray into `public/vendor/` |
| `npm run build` | Vite production assets in `public/build/` (main shell Tailwind/Flowbite via `@vite`) |
| `npm run build:tailwind` | Standalone `public/css/tailwind-build.min.css` (guest layout, some report pages) |

## Serving offline

1. Set `APP_URL` to the LAN address staff will use, with **http** (not https) and the serve port  
   (example: `http://192.168.1.10:8000`). Asset `href`s follow this — `https://` breaks styles on XAMPP/LAN.
2. Prefer local drivers in `.env`: `SESSION_DRIVER=file`, `CACHE_STORE=file`, `MAIL_MAILER=log`.
3. Start MySQL and the PHP app as usual (`php artisan serve --host=0.0.0.0 --port=8000`).
4. SMS/email are not required for library use; leave them unset or `MAIL_MAILER=log`.
5. After changing `.env`, run `php artisan config:clear` and `php artisan view:clear`.

## Features that need internet (graceful when offline)

These are optional. When offline they do **not** crash core workflows:

| Feature | Offline behavior |
|---------|------------------|
| ISBN copy catalog (Open Library / Google Books) | Clear flash: services unreachable — catalog manually |
| External cover image download | Skipped; book still saves |
| Cloud SMS | Unused for PBCC on-prem; keep `MAIL_MAILER=log` |

## Verify LAN-only UI

With the host disconnected from the internet (or outbound blocked):

- [ ] Login / guest layout styled (no CDN Tailwind)
- [ ] Authenticated sidebar, SweetAlert2 dialogs, themes
- [ ] Dashboards and visit/attendance report charts (local Chart.js)
- [ ] Holiday calendar on circulation policy / fines (local FullCalendar)
- [ ] OPAC landing fonts and print scripts (local Inter + qz-tray + SweetAlert2)
- [ ] Book copies staff page loads without daisyUI / Tailwind browser CDN
- [ ] ISBN lookup shows unreachable message, not HTTP 500 (if used)

## Not in scope

- Browser PWA / working with no connection to the Laravel server
- Pantas-UI mobile offline sync
