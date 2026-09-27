import os
import json
import re
from PIL import Image, ImageOps

SRC_ROOT = r"C:\Users\Lab_Engineer\Downloads\Catalog\Catalog"
OUT_ROOT = r"C:\Users\Lab_Engineer\Downloads\Catalog\brochure\assets\images"
EXTRA_ROOT = r"C:\Users\Lab_Engineer\Downloads\Catalog\brochure\assets\images\extra"

os.makedirs(OUT_ROOT, exist_ok=True)
os.makedirs(EXTRA_ROOT, exist_ok=True)

# folders where cropping must NOT happen (by leading number)
NO_CROP_NUMBERS = {"1", "4", "5"}

MAX_DIM = 800  # max width/height for product photos
WEBP_QUALITY = 68

def get_folder_number(folder_name):
    m = re.match(r"^(\d+)\.", folder_name)
    return m.group(1) if m else None

def autocrop_whitespace(im, bg_thresh=245, pad=12):
    """Crop near-white/near-uniform borders around the subject."""
    rgb = im.convert("RGB")
    # Build a mask of "non-background" pixels (not near-white)
    gray = rgb.convert("L")
    # Use a threshold: pixels darker than bg_thresh are considered content
    mask = gray.point(lambda p: 255 if p < bg_thresh else 0)
    bbox = mask.getbbox()
    if bbox is None:
        return im
    left, top, right, bottom = bbox
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(im.width, right + pad)
    bottom = min(im.height, bottom + pad)
    # sanity: don't crop if bbox is nearly the whole image already or too small
    if (right - left) < 20 or (bottom - top) < 20:
        return im
    return im.crop((left, top, right, bottom))

def process_file(src_path, dst_path, do_crop):
    try:
        im = Image.open(src_path)
        im = ImageOps.exif_transpose(im)
        if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
            im = im.convert("RGBA")
            background = Image.new("RGBA", im.size, (255, 255, 255, 255))
            im = Image.alpha_composite(background, im).convert("RGB")
        else:
            im = im.convert("RGB")

        if do_crop:
            im = autocrop_whitespace(im)

        w, h = im.size
        if max(w, h) > MAX_DIM:
            scale = MAX_DIM / max(w, h)
            im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)

        im.save(dst_path, "WEBP", quality=WEBP_QUALITY, method=6)
        return im.size
    except Exception as e:
        print(f"ERROR processing {src_path}: {e}")
        return None

def safe_name(name):
    base = os.path.splitext(name)[0]
    base = re.sub(r"[^A-Za-z0-9_\-]+", "_", base)
    return base

manifest = {}

folders = sorted(
    [f for f in os.listdir(SRC_ROOT) if os.path.isdir(os.path.join(SRC_ROOT, f))]
)

for folder in folders:
    folder_path = os.path.join(SRC_ROOT, folder)
    number = get_folder_number(folder)
    do_crop = number not in NO_CROP_NUMBERS if number else True

    out_folder_slug = safe_name(folder)
    out_folder_path = os.path.join(OUT_ROOT, out_folder_slug)
    os.makedirs(out_folder_path, exist_ok=True)

    files = sorted(os.listdir(folder_path))
    entries = []
    for fname in files:
        fpath = os.path.join(folder_path, fname)
        if not os.path.isfile(fpath):
            continue
        ext = os.path.splitext(fname)[1].lower()
        if ext not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        out_name = safe_name(fname) + ".webp"
        out_path = os.path.join(out_folder_path, out_name)
        size = process_file(fpath, out_path, do_crop)
        if size:
            entries.append({
                "file": f"assets/images/{out_folder_slug}/{out_name}",
                "width": size[0],
                "height": size[1]
            })
            print(f"OK: {folder}/{fname} -> {out_folder_slug}/{out_name} ({size[0]}x{size[1]}) crop={do_crop}")

    manifest[folder] = {
        "number": number,
        "crop_applied": do_crop,
        "images": entries
    }

with open(os.path.join(os.path.dirname(OUT_ROOT), "..", "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print("\nDONE. Manifest written.")
