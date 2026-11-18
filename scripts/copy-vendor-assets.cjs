const fs = require('fs');
const path = require('path');

/**
 * Copy npm packages into public/vendor so the LAN server needs no CDN at runtime.
 * Run via: npm run copy-vendor (also postinstall).
 */

function ensureDir(dir) {
    fs.mkdirSync(dir, { recursive: true });
}

function copyFile(from, to) {
    if (!fs.existsSync(from)) {
        console.warn('[copy-vendor-assets] Skip (missing):', from);
        return false;
    }
    ensureDir(path.dirname(to));
    fs.copyFileSync(from, to);
    console.log('[copy-vendor-assets] Copied', to);
    return true;
}

function copyDir(from, to) {
    if (!fs.existsSync(from)) {
        console.warn('[copy-vendor-assets] Skip dir (missing):', from);
        return false;
    }
    ensureDir(to);
    for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
        const src = path.join(from, entry.name);
        const dest = path.join(to, entry.name);
        if (entry.isDirectory()) {
            copyDir(src, dest);
        } else {
            fs.copyFileSync(src, dest);
        }
    }
    console.log('[copy-vendor-assets] Copied dir', to);
    return true;
}

const fileCopies = [
    {
        from: 'node_modules/bootstrap/dist/css/bootstrap.min.css',
        to: 'public/vendor/bootstrap/css/bootstrap.min.css',
    },
    {
        from: 'node_modules/bootstrap/dist/css/bootstrap.min.css.map',
        to: 'public/vendor/bootstrap/css/bootstrap.min.css.map',
    },
    {
        from: 'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js',
        to: 'public/vendor/bootstrap/js/bootstrap.bundle.min.js',
    },
    {
        from: 'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js.map',
        to: 'public/vendor/bootstrap/js/bootstrap.bundle.min.js.map',
    },
    {
        from: 'node_modules/jquery/dist/jquery.min.js',
        to: 'public/vendor/jquery/jquery.min.js',
    },
    {
        from: 'node_modules/bootstrap-icons/font/bootstrap-icons.css',
        to: 'public/vendor/bootstrap-icons/bootstrap-icons.css',
    },
    {
        from: 'node_modules/fullcalendar/index.global.min.js',
        to: 'public/vendor/fullcalendar/index.global.min.js',
    },
    {
        from: 'node_modules/qz-tray/qz-tray.js',
        to: 'public/vendor/qz-tray/qz-tray.js',
    },
    {
        // Chart.js 4 ships a single UMD build (already minified); no separate .min file.
        from: 'node_modules/chart.js/dist/chart.umd.js',
        to: 'public/vendor/chart.js/chart.umd.js',
    },
    {
        from: 'node_modules/sweetalert2/dist/sweetalert2.all.min.js',
        to: 'public/vendor/sweetalert2/sweetalert2.all.min.js',
    },
    // Figtree
    {
        from: 'node_modules/@fontsource/figtree/latin-400.css',
        to: 'public/vendor/fontsource/figtree/latin-400.css',
    },
    {
        from: 'node_modules/@fontsource/figtree/latin-500.css',
        to: 'public/vendor/fontsource/figtree/latin-500.css',
    },
    {
        from: 'node_modules/@fontsource/figtree/latin-600.css',
        to: 'public/vendor/fontsource/figtree/latin-600.css',
    },
    // Poppins
    {
        from: 'node_modules/@fontsource/poppins/latin-400.css',
        to: 'public/vendor/fontsource/poppins/latin-400.css',
    },
    {
        from: 'node_modules/@fontsource/poppins/latin-600.css',
        to: 'public/vendor/fontsource/poppins/latin-600.css',
    },
    {
        from: 'node_modules/@fontsource/poppins/latin-700.css',
        to: 'public/vendor/fontsource/poppins/latin-700.css',
    },
    // Martel Sans
    {
        from: 'node_modules/@fontsource/martel-sans/latin-900.css',
        to: 'public/vendor/fontsource/martel-sans/latin-900.css',
    },
    // Inter (OPAC landing — replaces Google Fonts)
    {
        from: 'node_modules/@fontsource/inter/latin-400.css',
        to: 'public/vendor/fontsource/inter/latin-400.css',
    },
    {
        from: 'node_modules/@fontsource/inter/latin-500.css',
        to: 'public/vendor/fontsource/inter/latin-500.css',
    },
    {
        from: 'node_modules/@fontsource/inter/latin-600.css',
        to: 'public/vendor/fontsource/inter/latin-600.css',
    },
    {
        from: 'node_modules/@fontsource/inter/latin-700.css',
        to: 'public/vendor/fontsource/inter/latin-700.css',
    },
];

const dirCopies = [
    {
        from: 'node_modules/bootstrap-icons/font/fonts',
        to: 'public/vendor/bootstrap-icons/fonts',
    },
    {
        from: 'node_modules/@fontsource/figtree/files',
        to: 'public/vendor/fontsource/figtree/files',
    },
    {
        from: 'node_modules/@fontsource/poppins/files',
        to: 'public/vendor/fontsource/poppins/files',
    },
    {
        from: 'node_modules/@fontsource/martel-sans/files',
        to: 'public/vendor/fontsource/martel-sans/files',
    },
    {
        from: 'node_modules/@fontsource/inter/files',
        to: 'public/vendor/fontsource/inter/files',
    },
];

for (const { from, to } of fileCopies) {
    copyFile(from, to);
}

for (const { from, to } of dirCopies) {
    copyDir(from, to);
}

console.log('[copy-vendor-assets] Done.');
