"""
Generate a step-by-step PBCC Pantas on-prem / offline LAN setup guide (DOCX).
Stack: XAMPP on Windows (library server PC).
"""
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = RGBColor(0x00, 0x39, 0xA6)
GREEN = RGBColor(0x14, 0x8A, 0x32)
DARK = RGBColor(0x22, 0x22, 0x22)
GRAY = RGBColor(0x55, 0x55, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xB7, 0x1C, 0x1C)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "documentation" / "PBCC-Library-System-Setup-Guide.docx"
# Fallback if the main file is open/locked in Word or the IDE
OUT_FALLBACK = ROOT / "documentation" / "PBCC-Library-System-Setup-Guide-XAMPP.docx"

doc = Document()
for section in doc.sections:
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)


def set_font(run, size=11, bold=False, color=None, name="Calibri"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    if color is not None:
        run.font.color.rgb = color


def add_title(text, size=22):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    set_font(r, size=size, bold=True, color=NAVY)
    return p


def add_center(text, size=12, bold=False, color=GRAY):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    set_font(r, size=size, bold=bold, color=color)
    return p


def h(text, level=1):
    heading = doc.add_heading(text, level=level)
    for run in heading.runs:
        run.font.color.rgb = NAVY
    return heading


def para(text, bold=False, size=11):
    p = doc.add_paragraph()
    r = p.add_run(text)
    set_font(r, size=size, bold=bold, color=DARK)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.space_before = Pt(0)
    return p


def tip(text):
    p = doc.add_paragraph()
    r1 = p.add_run("TIP: ")
    set_font(r1, bold=True, color=GREEN)
    r2 = p.add_run(text)
    set_font(r2, color=DARK)
    p.paragraph_format.space_after = Pt(8)
    return p


def warn(text):
    p = doc.add_paragraph()
    r1 = p.add_run("IMPORTANT: ")
    set_font(r1, bold=True, color=RED)
    r2 = p.add_run(text)
    set_font(r2, color=DARK)
    p.paragraph_format.space_after = Pt(8)
    return p


def see(text):
    p = doc.add_paragraph()
    r1 = p.add_run("What you should see: ")
    set_font(r1, bold=True, color=NAVY)
    r2 = p.add_run(text)
    set_font(r2, color=DARK)
    p.paragraph_format.space_after = Pt(8)
    return p


def bullet(text):
    p = doc.add_paragraph(style="List Bullet")
    p.clear()
    r = p.add_run(text)
    set_font(r, color=DARK)
    return p


def numbered(text):
    p = doc.add_paragraph(style="List Number")
    p.clear()
    r = p.add_run(text)
    set_font(r, color=DARK)
    return p


def code_block(lines):
    for line in lines:
        p = doc.add_paragraph()
        r = p.add_run(line)
        set_font(r, size=10, name="Consolas", color=DARK)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.left_indent = Inches(0.15)
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), "E7F0FA")
        shd.set(qn("w:val"), "clear")
        p.paragraph_format.element.get_or_add_pPr().append(shd)
    doc.add_paragraph()


def shade_cell(cell, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    shd.set(qn("w:val"), "clear")
    cell._tc.get_or_add_tcPr().append(shd)


def add_table(headers, rows):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    for i, header in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = ""
        r = cell.paragraphs[0].add_run(header)
        set_font(r, size=10, bold=True, color=WHITE)
        shade_cell(cell, "0039A6")
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = t.rows[ri + 1].cells[ci]
            cell.text = ""
            r = cell.paragraphs[0].add_run(val)
            set_font(r, size=10, color=DARK)
    doc.add_paragraph()
    return t


def page_break():
    doc.add_page_break()


# ========== COVER ==========
add_title("PBCC Library System (Pantas)", 24)
add_center("Step-by-Step Setup Guide for a New Computer", 16, bold=True, color=DARK)
add_center("XAMPP on Windows — on-premises library LAN (offline after first install)", 12)
add_center("Pangantucan Bukidnon Community College", 11)
add_center("Pangantucan, Bukidnon", 11)
doc.add_paragraph()
para(
    "This guide walks you through installing and running the PBCC Library System on a new "
    "Windows computer that will serve as the library server using XAMPP. Follow the steps in order. "
    "If a step fails, stop and use the Troubleshooting section."
)
warn(
    "Section 5 (one-time install) needs internet and is usually done once by ICT or the installer. "
    "Library staff mainly use Sections 6–8 every day. SMS and email are not required. "
    "There is no mobile app in this deployment."
)

h("Contents", 1)
for item in [
    "1. What this system is",
    "2. Words you will see",
    "3. What you need before starting",
    "4. Physical setup in the library",
    "5. Should I copy the whole pbcc folder?",
    "6. One-time install on the new computer (XAMPP, with internet)",
    "7. Turn the system ON every day",
    "8. How staff open and use the system",
    "9. Turn the system OFF at the end of the day",
    "10. First-week checklist after install",
    "11. What works without internet",
    "12. Troubleshooting",
    "13. Quick cards to print and post",
]:
    bullet(item)

page_break()

# ========== 1 ==========
h("1. What this system is", 1)
para(
    "The PBCC Library System (Pantas) is the digital system for cataloging books, circulating "
    "items, registering patrons, scanning library visits, room reservations, and reports."
)
para(
    "One computer is the Library Server. It stores all data. Other desks in the library only "
    "need Chrome or Microsoft Edge and must be on the same Wi-Fi or LAN as the server."
)
para(
    "After the first install (while online), the library can run without internet. Staff still "
    "need a connection to the Library Server PC — that PC must stay on while the system is in use."
)

h("How it looks", 2)
code_block(
    [
        "[ Library Server PC ]  ---- same Wi-Fi / LAN ----  [ Circulation desk ]",
        "   XAMPP + Pantas                                 [ Visit / gate scanner PC ]",
        "                                                  [ Optional OPAC / public PC ]",
    ]
)

# ========== 2 ==========
h("2. Words you will see", 1)
add_table(
    ["Word", "Meaning"],
    [
        ["Server", "The main library PC that keeps the data. Keep it ON while people use the system."],
        ["XAMPP", "Helper program that starts Apache (web) and MySQL (database) on Windows."],
        ["phpMyAdmin", "Web page in XAMPP used to create and view the MySQL database."],
        ["MySQL / Database", "Where patrons, books, loans, and logs are saved."],
        ["Browser", "Chrome or Microsoft Edge."],
        ["URL / Address", "What you type in the browser, e.g. http://192.168.1.50:8000"],
        ["IP address", "The server’s number on the local network (example: 192.168.1.50)."],
        ["LAN / Wi-Fi", "Local network. Staff PCs and the server must be on the same one."],
        [".env", "Settings file on the server. Do not share it publicly."],
        ["Command Prompt / Terminal", "Text window where you type commands (cmd or PowerShell)."],
        ["UPS", "Battery backup so brownouts do not suddenly shut off the server."],
    ],
)

page_break()

# ========== 3 ==========
h("3. What you need before starting", 1)
para("Tick these before install day:", bold=True)

h("People", 2)
bullet("ICT person or installer for the one-time install (Section 6)")
bullet("Librarian who will learn daily ON / OFF and login")
bullet("Approval to dedicate one PC as the Library Server")

h("Hardware", 2)
bullet("Windows 10 or 11 PC for the server (8 GB RAM or more preferred)")
bullet("UPS (strongly recommended)")
bullet("Ethernet cable to the library router/switch (preferred for the server)")
bullet("Staff PCs or tablets with Chrome or Edge on the same network")
bullet("Optional: barcode / RFID scanner that types like a keyboard")
bullet("USB drive or shared folder to copy the project (if not downloading on the server)")

h("Software to download (install day — internet required)", 2)
bullet("XAMPP for Windows (PHP 8.2 or newer)")
bullet("Composer for Windows (getcomposer.org)")
bullet("Node.js LTS — only if you still need to build UI assets on this PC")
bullet("The PBCC Pantas project folder (see Section 5)")

h("Information to prepare", 2)
bullet("Fixed / reserved server IP from ICT (example: 192.168.1.50)")
bullet("List of staff who need accounts and roles")
bullet("Internet available for install day only")

# ========== 4 ==========
h("4. Physical setup in the library", 1)
numbered("Place the server in a secure, ventilated spot (ICT room or librarian office).")
numbered("Plug the server into the UPS; plug the UPS into the wall.")
numbered("Connect Ethernet to the library network.")
numbered('Label the PC: "LIBRARY SERVER — DO NOT SHUT DOWN DURING LIBRARY HOURS".')
numbered("Write the staff URL on paper at the server and every desk.")
numbered("Put circulation / scanner / OPAC PCs on the same Wi-Fi or LAN.")
tip("For scanners: click inside the scan box on screen first, then scan. It should type like a keyboard.")

page_break()

# ========== 5 ==========
h("5. Should I copy the whole pbcc folder?", 1)
para(
    "Yes — copy the project to the new computer. That is the normal way to deploy PBCC. "
    "You do not need to rebuild everything from scratch if the folder is already prepared."
)

h("Recommended: copy a prepared folder", 2)
para(
    "On your current PC (d:\\pbcc), after composer install and npm build have already been run, "
    "copy the project to the library PC at:"
)
code_block(["C:\\xampp\\htdocs\\pbcc"])

para("Include these (required):", bold=True)
bullet("app, bootstrap, config, database, public, resources, routes, storage, tests")
bullet("artisan, composer.json, composer.lock, package.json, package-lock.json")
bullet("vendor\\ (PHP packages — large, but saves running composer on the new PC)")
bullet("public\\build\\, public\\vendor\\, public\\css\\tailwind-build.min.css (offline UI assets)")
bullet("documentation\\ (guides)")

para("You can skip these to save space / time:", bold=True)
bullet("node_modules\\ — very large; not needed for daily running if public\\build and public\\vendor already exist")
bullet(".git\\ — optional (only if you want version history on the server)")
bullet("storage\\logs\\*.log — old log files; safe to leave behind")
bullet("Your old .env — better to create a fresh .env on the new PC from .env.example")

warn(
    "Do not rely on copying a machine-specific .env blindly. On the new PC, create .env from "
    ".env.example and set APP_URL and database settings for that computer."
)

h("If the folder is source-only (no vendor / no built assets)", 2)
para(
    "Then on the new PC (with internet once) you must run composer install, npm install, "
    "npm run build, and npm run build:tailwind before serving. See Section 6F."
)

h("After copying", 2)
bullet("Install XAMPP and create the MySQL database (Section 6)")
bullet("Create/edit .env for the new PC")
bullet("Run migrate + seeders if this is a fresh empty database")
bullet("Make sure storage and bootstrap\\cache are writable by Apache/PHP")

page_break()

# ========== 6 ==========
h("6. One-time install on the new computer (XAMPP, with internet)", 1)
para(
    "Do this once on the Library Server. If you already copied a fully built folder "
    "(with vendor\\ and public assets), you can skip the npm build steps."
)

h("A. Install XAMPP", 2)
numbered("Download XAMPP for Windows (PHP 8.2+).")
numbered("Install to the default path: C:\\xampp")
numbered("Open XAMPP Control Panel.")
numbered("Click Start for Apache and Start for MySQL.")
see("Apache and MySQL show green / Running in the XAMPP Control Panel.")

h("B. Install Composer", 2)
numbered("Install Composer for Windows from getcomposer.org.")
numbered("Open a new Command Prompt and run: composer -V")
see("A Composer version number appears.")
tip("If the new PC already has vendor\\ from the copied folder, you may not need Composer until you update packages later.")

h("C. Copy the project into htdocs", 2)
para("Copy the pbcc project to:")
code_block(["C:\\xampp\\htdocs\\pbcc"])
para("See Section 5 for what to include or skip.")

h("D. Create the database (phpMyAdmin)", 2)
numbered("In the browser on the server, open http://localhost/phpmyadmin")
numbered("Click New (or Databases).")
numbered("Database name: pbcc_library")
numbered("Collation: utf8mb4_unicode_ci")
numbered("Click Create.")
code_block(
    [
        "CREATE DATABASE pbcc_library CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
    ]
)

h("E. Enable PHP extensions in XAMPP", 2)
numbered("Open C:\\xampp\\php\\php.ini in Notepad.")
numbered("Find and make sure these lines are enabled (no leading ;):")
code_block(
    [
        "extension=zip",
        "extension=gd",
        "extension=mbstring",
        "extension=openssl",
        "extension=pdo_mysql",
        "extension=fileinfo",
        "extension=curl",
    ]
)
numbered("Save php.ini.")
numbered("In XAMPP Control Panel: Stop Apache, then Start Apache again.")
tip("Backups and some Excel features need extension=zip.")

h("F. Install packages / build assets (only if missing)", 2)
para(
    "Open Command Prompt. Prefer using XAMPP’s PHP by adding it to PATH for the session:"
)
code_block(
    [
        "cd C:\\xampp\\htdocs\\pbcc",
        "set PATH=C:\\xampp\\php;%PATH%",
    ]
)
para("If vendor\\ is missing:")
code_block(["composer install"])
para("If public\\build or public\\vendor UI assets are missing (needs Node.js once):")
code_block(
    [
        "npm install",
        "npm run build",
        "npm run build:tailwind",
    ]
)
para("Always create .env if it does not exist yet:")
code_block(
    [
        "copy .env.example .env",
        "php artisan key:generate",
    ]
)
see(
    "public\\vendor\\, public\\build\\, and public\\css\\tailwind-build.min.css exist. "
    ".env exists and APP_KEY is set."
)

h("G. Edit the .env file", 2)
para("Open C:\\xampp\\htdocs\\pbcc\\.env in Notepad and set at least:")
code_block(
    [
        'APP_NAME="PBCC Library"',
        "APP_ENV=production",
        "APP_DEBUG=false",
        "APP_URL=http://192.168.1.50:8000",
        "",
        "DB_CONNECTION=mysql",
        "DB_HOST=127.0.0.1",
        "DB_PORT=3306",
        "DB_DATABASE=pbcc_library",
        "DB_USERNAME=root",
        "DB_PASSWORD=",
        "",
        "SESSION_DRIVER=file",
        "CACHE_STORE=file",
        "MAIL_MAILER=log",
        "QUEUE_CONNECTION=database",
        "",
        "MYSQL_DUMP_BINARY_PATH=C:/xampp/mysql/bin",
    ]
)
warn(
    "Replace 192.168.1.50 with the real Library Server IP. XAMPP MySQL root password is usually "
    "blank unless you set one. SMS/email are not required — MAIL_MAILER=log is fine."
)

h("H. Create tables and starter accounts", 2)
code_block(
    [
        "cd C:\\xampp\\htdocs\\pbcc",
        "set PATH=C:\\xampp\\php;%PATH%",
        "php artisan migrate",
        "php artisan db:seed --class=MarcFrameworkSeeder",
        "php artisan db:seed --class=RoleSeeder",
        "php artisan db:seed --class=SuperAdminSeeder",
        "php artisan storage:link",
    ]
)

h("I. First login (change password the same day)", 2)
code_block(
    [
        "Email:    super_admin@pantas.test",
        "Password: password",
    ]
)
para(
    "After Section 7 startup, open http://127.0.0.1:8000 on the server, log in, and change this password immediately."
)
warn("These seed credentials are for first setup only. Do not leave password as password in production.")

h("J. Allow other library PCs to connect", 2)
numbered("Set a fixed or DHCP-reserved IP on the Library Server.")
numbered("Windows Firewall: allow inbound TCP port 8000 (or your chosen port).")
numbered("From a staff PC on the same LAN, open http://SERVER-IP:8000")
see("The PBCC landing or login page loads on the staff PC.")
tip(
    "This guide uses php artisan serve on port 8000 so LAN access is simple. "
    "Advanced users may instead point Apache at public\\ as the document root."
)

page_break()

# ========== 7 ==========
h("7. Turn the system ON every day", 1)
numbered("Turn on UPS → turn on the Library Server.")
numbered("Open XAMPP Control Panel → Start Apache → Start MySQL.")
numbered("Open Command Prompt and run:")
code_block(
    [
        "cd C:\\xampp\\htdocs\\pbcc",
        "set PATH=C:\\xampp\\php;%PATH%",
        "php artisan serve --host=0.0.0.0 --port=8000",
    ]
)
numbered("Leave that Command Prompt window open.")
numbered("Test on the server: http://127.0.0.1:8000")
warn("If you close the window that is running php artisan serve, staff will lose access.")

# ========== 8 ==========
h("8. How staff open and use the system", 1)
numbered("Connect to the library Wi-Fi / LAN.")
numbered("Open Chrome or Edge.")
numbered("Go to http://SERVER-IP:8000 (bookmark it).")
numbered("Click LOGIN with your own staff account.")

add_table(
    ["I want to…", "Go to…"],
    [
        ["Borrow / return books", "Library → Circulation"],
        ["Manage books / catalog", "Library → Books"],
        ["Approve new patrons", "Pending registrations"],
        ["Scan library visits", "Library visit scanner"],
        ["School attendance scan", "Attendance → Scanner"],
        ["Reports", "Dashboard / Reports"],
        ["Room reservations", "Library → Rooms"],
        ["Public catalog (OPAC)", "Public OPAC / landing pages"],
    ],
)

# ========== 9 ==========
h("9. Turn the system OFF at the end of the day", 1)
numbered("Ask all staff to log out.")
numbered("Click the Command Prompt window → press Ctrl+C to stop the server.")
numbered("XAMPP Control Panel → Stop Apache and Stop MySQL (if school policy requires it).")
numbered("Shut down the PC or leave it on — follow ICT policy (especially if nightly backups are scheduled).")

page_break()

# ========== 10 ==========
h("10. First-week checklist after install", 1)
bullet("Change the starter super_admin password")
bullet("Create real staff accounts and assign roles (library_admin, library_staff, etc.)")
bullet("Set circulation policy (loan days, fines, holidays)")
bullet("Import or encode programs and patrons")
bullet("Test borrow and return")
bullet("Test library visit scan (and school attendance scan if used)")
bullet("Print and post the Quick Cards in Section 13")
bullet("Agree who starts and stops the server each day")
bullet("Optional: configure local DB backup path and schedule")

# ========== 11 ==========
h("11. What works without internet", 1)
add_table(
    ["Works without internet", "Needs internet (optional)"],
    [
        ["Login, catalog, circulation, scans, reports", "ISBN auto-lookup (Google Books / Open Library)"],
        ["Local file session/cache and local storage", "External cover image download"],
        ["Staff PCs talking to the Library Server on LAN", "First-time composer / npm install only"],
        ["MAIL_MAILER=log (no email needed)", "Cloud SMS / email (not used for this PBCC setup)"],
    ],
)
para("More technical detail: documentation\\offline-lan-setup.md inside the project folder.")

# ========== 12 ==========
h("12. Troubleshooting", 1)
add_table(
    ["What you notice", "What to try"],
    [
        [
            "Site can’t be reached",
            "Server on? XAMPP Apache+MySQL running? Command Prompt still running serve? Same Wi-Fi/LAN? Correct IP? Firewall port 8000?",
        ],
        [
            "php is not recognized",
            "In that Command Prompt run: set PATH=C:\\xampp\\php;%PATH% then try again",
        ],
        [
            "Page has no colors / broken buttons",
            "On server (online once): npm run build and npm run build:tailwind, then Ctrl+F5",
        ],
        [
            "Database / SQL error",
            "Start MySQL in XAMPP; confirm pbcc_library exists in phpMyAdmin; check DB_* in .env",
        ],
        [
            "ZipArchive / zip error",
            "Enable extension=zip in C:\\xampp\\php\\php.ini; restart Apache",
        ],
        [
            "ISBN lookup failed",
            "Normal when offline — catalog the book manually",
        ],
        [
            "Scanner types nowhere",
            "Click inside the scan input box, then scan again",
        ],
        [
            "Login works on server but not other PCs",
            "Use --host=0.0.0.0; allow firewall port 8000; APP_URL should use the LAN IP",
        ],
        [
            "Port 80 already in use / Apache won’t start",
            "Stop other web servers (IIS, Skype, etc.) or change Apache port in XAMPP; artisan serve on 8000 can still work if MySQL is up",
        ],
    ],
)

page_break()

# ========== 13 ==========
h("13. Quick cards to print and post", 1)

h("CARD A — Morning (Library Server)", 2)
code_block(
    [
        "1. UPS + server ON",
        "2. XAMPP → Start Apache + Start MySQL",
        "3. Command Prompt:",
        "   cd C:\\xampp\\htdocs\\pbcc",
        "   set PATH=C:\\xampp\\php;%PATH%",
        "   php artisan serve --host=0.0.0.0 --port=8000",
        "4. Leave window OPEN",
        "5. Test http://127.0.0.1:8000",
    ]
)

h("CARD B — Staff desk", 2)
code_block(
    [
        "1. Library Wi-Fi / LAN",
        "2. Chrome or Edge",
        "3. http://SERVER-IP:8000",
        "4. LOGIN with your account",
    ]
)

h("CARD C — Evening (Library Server)", 2)
code_block(
    [
        "1. Everyone logs out",
        "2. Command Prompt → Ctrl+C",
        "3. XAMPP Stop Apache + Stop MySQL (if required)",
        "4. Shut down / leave ON per ICT policy",
    ]
)

h("CARD D — Fill in for this library", 2)
code_block(
    [
        "ICT name: ____________________",
        "Contact: _____________________",
        "Server IP: ___________________",
        "Staff URL: http://______:8000",
        "Morning backup person: _______",
        "Project folder: C:\\xampp\\htdocs\\pbcc",
    ]
)

doc.add_paragraph()
add_center("End of guide — PBCC Library System (Pantas) / XAMPP", 11, bold=True, color=NAVY)
add_center("Keep this document with the Library Server PC.", 10, color=GRAY)

OUT.parent.mkdir(parents=True, exist_ok=True)
try:
    doc.save(str(OUT))
    print(f"Wrote {OUT}")
except PermissionError:
    doc.save(str(OUT_FALLBACK))
    print(f"Main file locked; wrote {OUT_FALLBACK}")
    print(f"Close {OUT.name} and re-run to replace the main guide.")
