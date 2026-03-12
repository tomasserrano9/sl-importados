"""
PATCH 2 — Ajustes visuales: banner más grande sin %, search bar claro
"""
import os, sys

f = "index.html"
if not os.path.exists(f):
    print("ERROR: no se encontro index.html"); sys.exit(1)

with open(f, "r", encoding="utf-8") as fh:
    html = fh.read()

# 1. Banner más grande, sin porcentaje de interés
html = html.replace(
    """    .promo-banner {
      background: linear-gradient(90deg, var(--accent), #c62416);
      color: white; text-align: center;
      padding: 9px 16px; font-size: 13px; font-weight: 500;
      letter-spacing: 0.3px;
    }""",
    """    .promo-banner {
      background: linear-gradient(90deg, var(--accent), #c62416);
      color: white; text-align: center;
      padding: 14px 16px; font-size: 15px; font-weight: 600;
      letter-spacing: 0.5px;
    }"""
)

# Mobile banner
html = html.replace(
    """      .promo-banner { font-size: 11px; padding: 7px 12px; }""",
    """      .promo-banner { font-size: 12px; padding: 11px 12px; }"""
)

# 2. Banner text — remove % interest, just show cuotas
# Change the JS that updates the banner to NOT show interest %
html = html.replace(
    '''if (bannerEl) bannerEl.textContent = "\\u{1F4B3} PAG\\u00C1 EN CUOTAS \\u2014 3 cuotas (" + interes3Cuotas + "%) \\u00B7 6 cuotas (" + interes6Cuotas + "%) \\u00B7 ENV\\u00CDOS A TODO EL PA\\u00CDS";''',
    '''if (bannerEl) bannerEl.textContent = "\\u{1F4B3} PAG\\u00C1 EN CUOTAS \\u2014 Hasta 3 y 6 cuotas \\u00B7 ENV\\u00CDOS A TODO EL PA\\u00CDS";'''
)

# Also update the static HTML banner
html = html.replace(
    'PAG\u00c1 EN CUOTAS \u2014 HASTA 6 CUOTAS CON INTER\u00c9S \u00b7 ENV\u00cdOS A TODO EL PA\u00cdS',
    'PAG\u00c1 EN CUOTAS \u2014 Hasta 3 y 6 cuotas \u00b7 ENV\u00cdOS A TODO EL PA\u00cdS'
)

# 3. Search bar — lighter background color
html = html.replace(
    """    .search-bar input {
      width: 100%;
      background: var(--hf-surface2);
      border: 1px solid var(--hf-border);
      border-radius: 12px;
      padding: 11px 40px 11px 44px;
      color: var(--hf-text);""",
    """    .search-bar input {
      width: 100%;
      background: #2e2e2e;
      border: 1px solid #444;
      border-radius: 12px;
      padding: 11px 40px 11px 44px;
      color: #ffffff;"""
)

html = html.replace(
    """    .search-bar input:focus {
      border-color: var(--accent);
      background: var(--hf-surface3);
      box-shadow: 0 0 0 3px var(--accent-glow);
    }""",
    """    .search-bar input:focus {
      border-color: var(--accent);
      background: #383838;
      box-shadow: 0 0 0 3px var(--accent-glow);
    }"""
)

html = html.replace(
    """    .search-bar input::placeholder { color: var(--hf-muted); }""",
    """    .search-bar input::placeholder { color: #999; }"""
)

with open(f, "w", encoding="utf-8") as fh:
    fh.write(html)

print("✅ Cambios aplicados:")
print("   • Banner más grande sin % de interés")
print("   • Search bar con color más claro y visible")
print()
print("Hacé: git add . && git commit -m 'Ajustes visuales' && git push")
