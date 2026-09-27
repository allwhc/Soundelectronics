import json
import html

with open("manifest.json", encoding="utf-8") as f:
    manifest = json.load(f)

# Section order & display config
# (manifest_key, display_title, kind)
SECTIONS = [
    ("1.Backlight", "Backlight", "grid"),
    ("2.Converters", "Converters", "grid"),
    ("3.TCONS", "T-CONs", "grid"),
    ("4.Microscope", "Microscope", "grid"),
    ("5.Programmers and Tester and Multimeter", "Programmers, Testers &amp; Multimeters", "grid"),
    ("6.FFC", "FFC Cables", "grid"),
    ("7.Inverter and Power Supply", "Inverter &amp; Power Supply", "grid"),
    ("8.Amplifier board", "Amplifier Boards", "grid"),
    ("9.Bluetooth Panel", "Bluetooth Panels", "grid"),
    ("10.Panel", "Panels", "feature"),
    ("10.Speakers for TV 0.5", "Speakers for TV", "grid"),
    ("11.Stand 0.5", "TV Stands", "grid"),
    ("11.Tools", "Tools", "grid"),
]

PANEL_NOTE = "Variety of panels from 32&Prime; to 65&Prime; available. Packing for transport is done with utmost care in foam and wooden box."

OTHER_PRODUCTS = [
    "All kinds of HDMI Cable from 1.5M to 50M",
    "All types of Wall Mount",
    "Universal combo motherboard for TV",
    "All kinds of adapter and Metal SMPS from 5V1A to 24V20A",
    "FBT for CRT TV, CRT base, Solder wire and Yoke",
    "CRT TV KIT",
    "Other power chords and RC cables",
    "Converters like HDMI to VGA, VGA to HDMI, HDMI to AV, AV to HDMI",
]

def esc(s):
    return html.escape(s, quote=True)

def slugify(title):
    return title.lower().replace(" ", "-").replace("&amp;", "and").replace(",", "").replace("'", "")

nav_items = []
sections_html = []

for idx, (key, title, kind) in enumerate(SECTIONS, start=1):
    images = manifest.get(key, {}).get("images", [])
    anchor = f"sec-{idx}"
    nav_items.append((anchor, title))

    if kind == "feature" and images:
        img = images[0]
        sections_html.append(f'''
    <section class="section feature-section" id="{anchor}">
      <div class="section-head">
        <span class="section-num">{idx:02d}</span>
        <h2>{title}</h2>
      </div>
      <div class="feature-layout">
        <div class="feature-image">
          <img src="{esc(img['file'])}" alt="{esc(title)}" loading="lazy" width="{img['width']}" height="{img['height']}">
        </div>
        <div class="feature-text">
          <p><strong>{PANEL_NOTE}</strong></p>
        </div>
      </div>
    </section>''')
    else:
        cards = []
        for img in images:
            cards.append(f'''<figure class="card">
          <img src="{esc(img['file'])}" alt="{esc(title)}" loading="lazy" width="{img['width']}" height="{img['height']}">
        </figure>''')
        cards_html = "\n        ".join(cards)
        sections_html.append(f'''
    <section class="section" id="{anchor}">
      <div class="section-head">
        <span class="section-num">{idx:02d}</span>
        <h2>{title}</h2>
      </div>
      <div class="grid">
        {cards_html}
      </div>
    </section>''')

# Other products page (final numbered section)
other_idx = len(SECTIONS) + 1
other_items_html = "\n        ".join(f"<li>{esc(item)}</li>" for item in OTHER_PRODUCTS)
sections_html.append(f'''
    <section class="section other-section" id="sec-{other_idx}">
      <div class="section-head">
        <span class="section-num">{other_idx:02d}</span>
        <h2>Other Products We Deal In</h2>
      </div>
      <ol class="other-list">
        {other_items_html}
      </ol>
    </section>''')
nav_items.append((f"sec-{other_idx}", "Other Products"))

nav_links = "\n        ".join(f'<a href="#{anchor}">{title}</a>' for anchor, title in nav_items)

sections_joined = "\n".join(sections_html)

html_doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sound Electronics &mdash; Product Catalog</title>
<meta name="description" content="Sound Electronics wholesale dealer catalog: Panels, LED/LCD spare parts, IC, Transistor, CRT spares, Wires and Cables, LNB, Receiver, LCD/LED stand and other spares.">
<link rel="icon" href="assets/images/logo.webp">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>

<header class="topbar">
  <div class="topbar-inner">
    <img src="assets/images/logo.webp" alt="Sound Electronics logo" class="topbar-logo" width="40" height="40">
    <span class="topbar-name">SOUND ELECTRONICS</span>
    <button class="menu-toggle" id="menuToggle" aria-label="Open menu">&#9776;</button>
  </div>
  <nav class="navdrawer" id="navDrawer">
    {nav_links}
  </nav>
</header>

<section class="cover" id="cover">
  <div class="cover-inner">
    <img src="assets/images/logo.webp" alt="Sound Electronics" class="cover-logo" width="180" height="180">
    <h1>SOUND ELECTRONICS</h1>
    <p class="tagline">Wholesale Dealer in Panel, LED/LCD Spare Parts, IC, Transistor, CRT Spares, Wires &amp; Cables, LNB, Receiver, LCD/LED Stand &amp; Other Spares</p>
    <div class="cover-contact">
      <a href="tel:+919773679006">&#128222; +91 97736 79006</a>
      <a href="mailto:rdjainsound@gmail.com">&#9993; rdjainsound@gmail.com</a>
      <span>&#128205; 6A, Soonawala Building, 44-B, Proctor Road, near Hotel Grant, Grant Road (E), Mumbai 400 007</span>
    </div>
    <div class="cover-actions">
      <a href="#" class="btn btn-whatsapp" id="whatsappShareBtn" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.2h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2m0 1.8a8.1 8.1 0 0 1 5.75 2.38 8.08 8.08 0 0 1 2.38 5.73c0 4.48-3.65 8.13-8.14 8.13a8.14 8.14 0 0 1-4.14-1.13l-.3-.17-3.11.82.83-3.03-.19-.31a8.07 8.07 0 0 1-1.25-4.34c0-4.48 3.65-8.08 8.17-8.08M8.5 6.85c-.16 0-.43.06-.66.31s-.87.86-.87 2.08.89 2.42 1.02 2.58 1.72 2.77 4.28 3.77c2.12.83 2.55.67 3.01.63s1.48-.6 1.69-1.19.21-1.09.15-1.19-.24-.17-.5-.29-1.48-.73-1.71-.81-.4-.13-.57.13-.65.81-.8.98-.3.19-.55.06a6.9 6.9 0 0 1-2.03-1.25 7.6 7.6 0 0 1-1.41-1.75c-.15-.25-.02-.39.11-.51.11-.11.25-.29.37-.44s.16-.25.24-.42.04-.31-.02-.44-.57-1.4-.79-1.9-.42-.44-.57-.44-.32-.02-.49-.02"/></svg>
        Share on WhatsApp
      </a>
      <a href="sound-electronics-catalog.pdf" class="btn btn-download" download>
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 2a1 1 0 0 1 1 1v10.59l3.3-3.3a1 1 0 1 1 1.4 1.42l-5 5a1 1 0 0 1-1.4 0l-5-5a1 1 0 1 1 1.4-1.42l3.3 3.3V3a1 1 0 0 1 1-1M5 19a1 1 0 0 0 0 2h14a1 1 0 0 0 0-2z"/></svg>
        Download Brochure
      </a>
    </div>
  </div>
  <div class="cover-scroll-hint">Scroll to browse products &darr;</div>
</section>

<main>
{sections_joined}
</main>

<section class="contact-section" id="contact">
  <div class="section-head">
    <h2>Get In Touch</h2>
  </div>
  <div class="contact-card">
    <img src="assets/images/logo.webp" alt="Sound Electronics" class="contact-card-logo" width="72" height="72">
    <h3>SOUND ELECTRONICS</h3>
    <p class="contact-card-tag">Wholesale Dealer in Panel, LED/LCD Spare Parts, IC, Transistor, CRT Spares, Wires &amp; Cables, LNB, Receiver, LCD/LED Stand &amp; Other Spares</p>
    <ul class="contact-card-list">
      <li>&#128222; <a href="tel:+919773679006">Mayank &mdash; +91 97736 79006</a></li>
      <li>&#9993; <a href="mailto:rdjainsound@gmail.com">rdjainsound@gmail.com</a></li>
      <li>&#128205; 6A, Soonawala Building, 44-B, Proctor Road, near Hotel Grant, Grant Road (E), Mumbai 400 007</li>
    </ul>
  </div>
</section>

<footer class="site-footer">
  <img src="assets/images/logo.webp" alt="Sound Electronics" width="60" height="60">
  <p><strong>SOUND ELECTRONICS</strong></p>
  <p>6A, Soonawala Building, 44-B, Proctor Road, near Hotel Grant, Grant Road (E), Mumbai 400 007</p>
  <p><a href="tel:+919773679006">+91 97736 79006</a> &nbsp;|&nbsp; <a href="mailto:rdjainsound@gmail.com">rdjainsound@gmail.com</a></p>
  <div class="footer-actions">
    <a href="#" class="btn btn-whatsapp" id="whatsappShareBtn2" target="_blank" rel="noopener">Share on WhatsApp</a>
    <a href="sound-electronics-catalog.pdf" class="btn btn-download" download>Download Brochure</a>
  </div>
  <p class="footer-copy">&copy; 2026 Sound Electronics. All rights reserved.</p>
</footer>

<button id="backToTop" aria-label="Back to top">&uarr;</button>

<script src="assets/script.js"></script>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_doc)

print("index.html written.", len(sections_html), "sections.")
