from pathlib import Path
from PIL import Image, ImageOps

INPUT_DIR = Path("../app/assets/hallein_leiter")
INPUT_DIR = Path("../app/assets/tools")
INPUT_DIR = Path("../app/assets/todo")
OUTPUT_DIR = Path("../app/assets/hallein_leiter_2")
OUTPUT_DIR = Path("../app/assets/tools_2")
OUTPUT_DIR = Path("../app/assets/todo_2")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_W, MAX_H = 1920, 1080  # ← pick your cap
MAX_W, MAX_H = 1000, 1000  # ← pick your cap
FORMAT = "JPEG"  # "JPEG" | "WEBP" | "PNG"
# Good starting points:
SAVE_KW = {
    "JPEG": dict(quality=85, subsampling=1, optimize=True, progressive=False),
    # subsampling: 0=4:4:4 (best color, slightly larger), 1=4:2:0 (good default)
    "WEBP": dict(quality=80, method=6),  # method 6 = slower/better
    "PNG": dict(optimize=True),
}[FORMAT]

EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def fit_box(w, h, max_w, max_h):
    scale = min(max_w / w, max_h / h, 1.0)  # never upscale
    return int(w * scale), int(h * scale)


for p in sorted(INPUT_DIR.rglob("*")):
    if p.suffix.lower() not in EXTS:
        continue
    try:
        with Image.open(p) as im:
            im = ImageOps.exif_transpose(im)  # fix orientation
            w, h = im.size
            nw, nh = fit_box(w, h, MAX_W, MAX_H)
            if (nw, nh) == (w, h):
                # copy-through (already small)
                out = OUTPUT_DIR / (
                    p.stem + (".jpg" if FORMAT == "JPEG" else "." + FORMAT.lower())
                )
                im.save(out, **SAVE_KW)
                continue
            im = im.resize((nw, nh), Image.LANCZOS)
            # (Optional) tiny sharpen to counter downscale softness
            # from PIL import ImageFilter
            # im = im.filter(ImageFilter.UnsharpMask(radius=0.7, percent=80, threshold=2))
            out = OUTPUT_DIR / (
                p.stem + (".jpg" if FORMAT == "JPEG" else "." + FORMAT.lower())
            )
            im.save(out, **SAVE_KW)
            print(f"Downscaled {p.name}: {w}x{h} → {nw}x{nh}")
    except Exception as e:
        print(f"[SKIP] {p} ({e})")
