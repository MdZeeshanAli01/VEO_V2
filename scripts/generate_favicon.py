from PIL import Image, ImageDraw
from pathlib import Path

assets_dir = Path("web_app/assets")
assets_dir.mkdir(parents=True, exist_ok=True)

svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#06B6D4" />
      <stop offset="100%" stop-color="#3B82F6" />
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="#0F172A" />
  <rect x="4" y="4" width="56" height="56" rx="10" fill="none" stroke="#1E293B" stroke-width="2"/>
  <polygon points="32,14 50,24 32,34 14,24" fill="url(#grad)" opacity="0.95" />
  <polygon points="14,24 32,34 32,50 14,40" fill="#0284C7" opacity="0.8" />
  <polygon points="50,24 32,34 32,50 50,40" fill="#2563EB" opacity="0.8" />
  <circle cx="32" cy="34" r="3" fill="#F8FAFC" />
</svg>"""

with open(assets_dir / "favicon.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

img = Image.new("RGBA", (64, 64), color=(15, 23, 42, 255))
draw = ImageDraw.Draw(img)
draw.polygon([(32, 14), (50, 24), (32, 34), (14, 24)], fill=(6, 182, 212, 240))
draw.polygon([(14, 24), (32, 34), (32, 50), (14, 40)], fill=(2, 132, 199, 210))
draw.polygon([(50, 24), (32, 34), (32, 50), (50, 40)], fill=(37, 99, 235, 210))
draw.ellipse([(29, 31), (35, 37)], fill=(248, 250, 252, 255))

img.save("web_app/favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (64, 64)])
img.save("web_app/assets/favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (64, 64)])
print("Favicon generated successfully!")

