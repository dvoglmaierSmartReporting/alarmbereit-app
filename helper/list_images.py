from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path("./app/assets/tools")
ROOT = Path("./app/assets/hallein_leiter")
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def texture_bytes(w, h, channels=4):
    # Kivy textures are typically RGBA (4 bytes/px)
    return w * h * channels


def human_bytes(n):
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


for p in sorted(ROOT.rglob("*")):
    if p.suffix.lower() not in EXTS:
        continue
    try:
        with Image.open(p) as im:
            im = ImageOps.exif_transpose(im)  # respect camera rotation
            w, h = im.size
            mp = (w * h) / 1_000_000
            tex = texture_bytes(w, h)
            print(
                f"{p.name:40}  {w:5}x{h:<5}  {mp:4.1f} MP  ~{human_bytes(tex)} texture"
            )
    except Exception as e:
        print(f"[SKIP] {p} ({e})")
