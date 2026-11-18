# Special Letter 💌 — Web Sürümü

Orijinal `letter.py` (tkinter ASCII animasyonu) **hiç değiştirilmeden** tarayıcıda
gerçek Python olarak çalışır (Pyodide / WebAssembly). `py/webtk.py`, tkinter'in
kullanılan parçalarını taklit edip çizimi HTML canvas'a aktarır.

## Dosyalar
- `index.html` — sayfa, yükleme ekranı, mesaj, canvas çizimi
- `py/letter.py` — orijinal Python animasyonu
- `py/webtk.py` — tarayıcı için tkinter köprüsü

## Vercel'e yükleme
1. Bu klasörü bir GitHub reposuna koy (ya da `vercel` CLI ile bu klasörde `vercel` çalıştır).
2. Vercel'de **Add New → Project** → repoyu seç.
3. Framework Preset: **Other**, Build Command boş, Output Directory boş → **Deploy**.

Build adımı yok, tamamen statik site.

## Özelleştirme
`index.html` içinde en üstteki ayarlar:
```js
const MESAJ = "Dünya Prensesler Günün kutlu olsun 👑";
const MESAJ_SANIYE = 11.5;
```
`R` tuşu ya da sağ alttaki **↻ Tekrar** butonu animasyonu baştan oynatır.

Yerelde denemek için: `python -m http.server` → http://localhost:8000
