"""
PATCH SCRIPT — Agrega cuotas y banner al index.html de SL Importados
=====================================================================
USO:
  1. Copiá este archivo a la misma carpeta donde tenés el index.html del repo
  2. Ejecutá: python patch_cuotas.py
  3. Se genera index_nuevo.html — renombralo a index.html y hacé push

ANTES DE CORRER ESTE SCRIPT:
  Agregá en tu Google Sheet (hoja PRODUCTOS), fila 2:
  - Celda L2: 15  (interés % para 3 cuotas)
  - Celda M2: 25  (interés % para 6 cuotas)
"""

import re
import sys
import os

INPUT_FILE = "index.html"
OUTPUT_FILE = "index.html"  # Sobreescribe directamente

def patch_html():
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: No se encontró '{INPUT_FILE}' en esta carpeta.")
        print("Copiá este script a la carpeta del repo sl-importados y ejecutalo de nuevo.")
        sys.exit(1)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # ─────────────────────────────────────
    # 1. AGREGAR CSS PARA CUOTAS Y BANNER
    # ─────────────────────────────────────
    cuotas_css = """
    /* ====== CUOTAS ====== */
    .card-cuotas {
      display: flex; flex-direction: column; gap: 2px; margin-top: 2px;
    }
    .card-cuota-line {
      font-size: 11.5px; color: var(--muted2); font-weight: 400;
    }
    .card-cuota-line strong {
      color: var(--accent); font-weight: 600;
    }
    .modal-financiacion {
      background: var(--surface2); border: 1px solid var(--border);
      border-radius: 12px; padding: 18px; margin-bottom: 4px;
    }
    .modal-fin-row {
      display: flex; justify-content: space-between; align-items: center;
      padding: 10px 0;
    }
    .modal-fin-row:not(:last-child) {
      border-bottom: 1px solid var(--border);
    }
    .modal-fin-label {
      font-size: 13px; color: var(--muted2); font-weight: 400;
    }
    .modal-fin-price {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 20px; color: var(--text); letter-spacing: 0.5px;
    }
    .modal-fin-total {
      font-size: 11px; color: var(--muted); font-weight: 300;
    }
    .modal-fin-contado .modal-fin-price {
      color: var(--accent); font-size: 24px;
    }
    .modal-fin-highlight {
      background: var(--accent-glow); border-radius: 8px; padding: 2px 8px; margin: -2px -8px;
    }
    /* ====== PROMO BANNER ====== */
    .promo-banner {
      background: linear-gradient(90deg, var(--accent), #c62416);
      color: white; text-align: center;
      padding: 9px 16px; font-size: 13px; font-weight: 500;
      letter-spacing: 0.3px;
    }
    @media (max-width: 700px) {
      .promo-banner { font-size: 11px; padding: 7px 12px; }
      .card-cuota-line { font-size: 10.5px; }
    }"""

    # Insert CSS before the closing </style> tag
    html = html.replace("  </style>", cuotas_css + "\n  </style>")

    # ─────────────────────────────────────
    # 2. AGREGAR BANNER PROMOCIONAL
    # ─────────────────────────────────────
    banner_html = '<div class="promo-banner" id="promoBanner">💳 PAGÁ EN CUOTAS — HASTA 6 CUOTAS CON INTERÉS · ENVÍOS A TODO EL PAÍS</div>'

    # Insert before <header>
    html = html.replace("<header>", banner_html + "\n  <header>")

    # ─────────────────────────────────────
    # 3. AGREGAR VARIABLES GLOBALES DE CUOTAS
    # ─────────────────────────────────────
    # After the WSP_NUMBER line, add cuotas variables
    html = html.replace(
        'const WSP_NUMBER = "5492326471208";',
        'const WSP_NUMBER = "5492326471208";\n    let interes3Cuotas = 15, interes6Cuotas = 25; // Defaults, se leen del Sheet'
    )

    # ─────────────────────────────────────
    # 4. LEER INTERESES DESDE EL SHEET (en loadProducts)
    # ─────────────────────────────────────
    # After "const rows = json.table.rows;" add code to read interest rates from row 2
    interest_reader = """
        // Leer intereses de cuotas desde fila 2 del Sheet (celdas L2 y M2 = indices 11 y 12)
        if (rows.length > 1 && rows[1].c) {
          const configRow = rows[1].c;
          if (configRow[11] && configRow[11].v) interes3Cuotas = parseFloat(configRow[11].v) || 15;
          if (configRow[12] && configRow[12].v) interes6Cuotas = parseFloat(configRow[12].v) || 25;
        }
        // Actualizar banner con los valores reales
        const bannerEl = document.getElementById("promoBanner");
        if (bannerEl) bannerEl.textContent = "💳 PAGÁ EN CUOTAS — 3 cuotas (" + interes3Cuotas + "% interés) · 6 cuotas (" + interes6Cuotas + "% interés) · ENVÍOS A TODO EL PAÍS";"""

    html = html.replace(
        "        const rows = json.table.rows;\n        allProducts = [];",
        "        const rows = json.table.rows;\n" + interest_reader + "\n        allProducts = [];"
    )

    # ─────────────────────────────────────
    # 5. MOSTRAR CUOTAS EN CARDS
    # ─────────────────────────────────────
    # In the render() function, after the card-price div, add cuotas
    # Find the card price line and add cuotas after it
    old_card_price = """'<div class="card-price"><span>$</span>' + formatPrice(p.venta) + '</div>' +"""

    cuotas_in_card = """'<div class="card-price"><span>$</span>' + formatPrice(p.venta) + '</div>' +
          (p.venta > 0 ? '<div class="card-cuotas">' +
            '<div class="card-cuota-line"><strong>' + interes3Cuotas + '</strong>x $' + formatPrice(Math.round(p.venta * (1 + interes3Cuotas/100) / 3)) + '</div>' +
            '<div class="card-cuota-line"><strong>' + interes6Cuotas + '</strong>x $' + formatPrice(Math.round(p.venta * (1 + interes6Cuotas/100) / 6)) + '</div>' +
          '</div>' : '') +"""

    # Replace carefully - the old pattern should be unique
    html = html.replace(old_card_price, cuotas_in_card)

    # ─────────────────────────────────────
    # 6. TABLA DE FINANCIACIÓN EN MODAL
    # ─────────────────────────────────────
    # After modal-price div, add financing table
    old_modal_price = """html += '<div class="modal-price"><small>$</small>' + formatPrice(p.venta) + '</div>';"""

    modal_financing = """html += '<div class="modal-price"><small>$</small>' + formatPrice(p.venta) + '</div>';
      // Tabla de financiación
      if (p.venta > 0) {
        const total3 = Math.round(p.venta * (1 + interes3Cuotas/100));
        const total6 = Math.round(p.venta * (1 + interes6Cuotas/100));
        const cuota3 = Math.round(total3 / 3);
        const cuota6 = Math.round(total6 / 6);
        html += '<div class="modal-section-title">Financiacion</div>';
        html += '<div class="modal-financiacion">';
        html += '<div class="modal-fin-row modal-fin-contado"><span class="modal-fin-label">💰 Contado</span><span class="modal-fin-price">$' + formatPrice(p.venta) + '</span></div>';
        html += '<div class="modal-fin-row"><span class="modal-fin-label">3 cuotas de</span><div><span class="modal-fin-price">$' + formatPrice(cuota3) + '</span><span class="modal-fin-total"> (total $' + formatPrice(total3) + ')</span></div></div>';
        html += '<div class="modal-fin-row"><span class="modal-fin-label">6 cuotas de</span><div><span class="modal-fin-price">$' + formatPrice(cuota6) + '</span><span class="modal-fin-total"> (total $' + formatPrice(total6) + ')</span></div></div>';
        html += '</div>';
        html += '<div class="modal-divider"></div>';
      }"""

    html = html.replace(old_modal_price, modal_financing)

    # ─────────────────────────────────────
    # GUARDAR
    # ─────────────────────────────────────
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("=" * 50)
    print("✅ index.html actualizado con:")
    print("   • Cuotas en 3 y 6 pagos en cada card")
    print("   • Tabla de financiación en el modal")
    print("   • Banner promocional arriba")
    print("   • Lectura de intereses desde el Sheet")
    print("=" * 50)
    print()
    print("IMPORTANTE — Agregá en tu Google Sheet:")
    print("  Hoja PRODUCTOS, fila 2:")
    print("  • Celda L2: 15  (interés % para 3 cuotas)")
    print("  • Celda M2: 25  (interés % para 6 cuotas)")
    print()
    print("Ahora hacé: git add . && git commit -m 'Agregar cuotas' && git push")


if __name__ == "__main__":
    patch_html()
