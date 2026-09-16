# Verifica que ninguna lámina del deck EP4 desborde y guarda capturas por lámina.
import sys, pathlib, json
from playwright.sync_api import sync_playwright
from PIL import Image

HTML = pathlib.Path(__file__).resolve().parent.parent / "03-presentacion-EP4" / "presentacion-propuesta-marley.html"
OUT = pathlib.Path(__file__).parent / "deck4"
OUT.mkdir(exist_ok=True)

JS = """() => {
  const res = [];
  document.querySelectorAll('.s').forEach((s, i) => {
    const r = s.getBoundingClientRect();
    const f = s.querySelector('footer.f');
    const fTop = f ? f.getBoundingClientRect().top - r.top : r.height;
    let maxB = 0, maxR = 0, culprit = '';
    s.querySelectorAll('*').forEach(el => {
      if (el.closest('footer.f,.ph,.tint,.veil,.diag')) return;
      const e = el.getBoundingClientRect();
      if (!e.width || !e.height) return;
      const b = e.bottom - r.top;
      if (b > maxB) { maxB = b; culprit = el.tagName + '.' + el.className + ' ' + (el.textContent || '').trim().slice(0, 40); }
      maxR = Math.max(maxR, e.right - r.left);
    });
    res.push({ n: i + 1, alto: Math.round(r.height), contenido: Math.round(maxB), footer: Math.round(fTop),
               choca: maxB > fTop - 6, anchoMax: Math.round(maxR), desbordaX: maxR > r.width + 1, culprit });
  });
  return res;
}"""

def correr(w, h, capturar):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(HTML.as_uri())
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(1200)
        pg.add_style_tag(content="html{scroll-behavior:auto!important;scroll-snap-type:none!important}")
        # para capturas/PDF: el video muestra su portada fija en vez de un fotograma al azar
        pg.evaluate("(()=>{const v=document.getElementById('demo'); if(v){v.pause(); v.removeAttribute('src'); v.load();}})()")
        pg.wait_for_timeout(300)
        datos = pg.evaluate(JS)
        if capturar:
            n = len(datos)
            for i in range(n):
                pg.evaluate(f"document.querySelectorAll('.s')[{i}].scrollIntoView()")
                pg.wait_for_timeout(150)
                pg.screenshot(path=str(OUT / f"{w}-{i+1:02d}.png"))
        b.close()
    return datos

for (w, h) in [(1920, 1080), (1366, 768)]:
    d = correr(w, h, True)
    print(f"== {w}x{h}")
    for x in d:
        flag = "CHOCA" if x["choca"] else "ok"
        if x["desbordaX"]: flag += " X"
        print(f"{x['n']:02d} {flag:8} contenido {x['contenido']}/{x['footer']}  {x['culprit'] if x['choca'] else ''}")

# Hoja de contacto de 1920 para revisión rápida
imgs = sorted(OUT.glob("1920-*.png"))
tw, th = 640, 360
hoja = Image.new("RGB", (tw * 3, th * ((len(imgs) + 2) // 3)), "white")
for k, f in enumerate(imgs):
    im = Image.open(f).resize((tw, th))
    hoja.paste(im, ((k % 3) * tw, (k // 3) * th))
hoja.save(OUT / "hoja-1920.png")
