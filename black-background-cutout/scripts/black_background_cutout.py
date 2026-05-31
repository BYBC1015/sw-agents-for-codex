#!/usr/bin/env python3
"""Fast local cutout for black or simple solid-color backgrounds."""

from __future__ import annotations

import argparse
import glob
import zipfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


SUPPORTED_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


def parse_bg_color(value: str) -> tuple[int, int, int]:
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Use R,G,B, for example 0,0,0")
    try:
        rgb = tuple(int(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("R,G,B values must be integers") from exc
    if any(channel < 0 or channel > 255 for channel in rgb):
        raise argparse.ArgumentTypeError("R,G,B values must be between 0 and 255")
    return rgb  # type: ignore[return-value]


def expand_inputs(patterns: list[str]) -> list[Path]:
    files: list[Path] = []
    for pattern in patterns:
        expanded = glob.glob(pattern)
        if not expanded:
            expanded = [pattern]
        for item in expanded:
            path = Path(item)
            if path.is_dir():
                files.extend(
                    child
                    for child in sorted(path.iterdir())
                    if child.is_file() and child.suffix.lower() in SUPPORTED_SUFFIXES
                )
            elif path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
                files.append(path)
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in files:
        resolved = path.resolve()
        if resolved not in seen:
            unique.append(resolved)
            seen.add(resolved)
    return unique


def max_channel_distance(rgb: Image.Image, bg_color: tuple[int, int, int]) -> Image.Image:
    r, g, b = rgb.split()
    br, bg, bb = bg_color
    dr = r.point(lambda value: abs(value - br))
    dg = g.point(lambda value: abs(value - bg))
    db = b.point(lambda value: abs(value - bb))
    return ImageChops.lighter(ImageChops.lighter(dr, dg), db)


def alpha_from_distance(distance: Image.Image, start: float, opaque: float) -> Image.Image:
    if opaque <= start:
        raise ValueError("opaque threshold must be greater than start threshold")
    lut = []
    for value in range(256):
        if value <= start:
            alpha = 0
        elif value >= opaque:
            alpha = 255
        else:
            alpha = int(round((value - start) / (opaque - start) * 255))
        lut.append(max(0, min(255, alpha)))
    return distance.point(lut)


def checkerboard(size: tuple[int, int], block: int = 24) -> Image.Image:
    width, height = size
    bg = Image.new("RGB", size, (238, 238, 238))
    draw = ImageDraw.Draw(bg)
    for y in range(0, height, block):
        for x in range(0, width, block):
            if ((x // block) + (y // block)) % 2:
                draw.rectangle(
                    (x, y, min(x + block, width), min(y + block, height)),
                    fill=(205, 205, 205),
                )
    return bg.convert("RGBA")


def trimmed_rgba(rgba: Image.Image, alpha: Image.Image, padding: int) -> Image.Image:
    mask = alpha.point(lambda value: 255 if value > 5 else 0)
    bbox = mask.getbbox()
    if not bbox:
        return rgba
    left, top, right, bottom = bbox
    left = max(left - padding, 0)
    top = max(top - padding, 0)
    right = min(right + padding, rgba.width)
    bottom = min(bottom + padding, rgba.height)
    return rgba.crop((left, top, right, bottom))


def safe_name(path: Path) -> str:
    return "".join(char if char.isalnum() or char in "._-" else "_" for char in path.stem)


def save_preview(image_path: Path, preview_path: Path, size: tuple[int, int] = (900, 420)) -> None:
    canvas = checkerboard(size)
    obj = Image.open(image_path).convert("RGBA")
    obj.thumbnail((size[0] - 32, size[1] - 32), Image.Resampling.LANCZOS)
    canvas.alpha_composite(obj, ((size[0] - obj.width) // 2, (size[1] - obj.height) // 2))
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(preview_path, quality=95)


def zip_outputs(out_root: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for folder in ["full_canvas", "trimmed", "previews"]:
            for path in sorted((out_root / folder).glob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(out_root))


def process_file(
    src: Path,
    out_root: Path,
    bg_color: tuple[int, int, int],
    start: float,
    opaque: float,
    padding: int,
) -> tuple[Path, Path, Path, tuple[int, int], tuple[int, int]]:
    full_dir = out_root / "full_canvas"
    trim_dir = out_root / "trimmed"
    preview_dir = out_root / "previews"
    full_dir.mkdir(parents=True, exist_ok=True)
    trim_dir.mkdir(parents=True, exist_ok=True)
    preview_dir.mkdir(parents=True, exist_ok=True)

    rgb = Image.open(src).convert("RGB")
    distance = max_channel_distance(rgb, bg_color)
    alpha = alpha_from_distance(distance, start, opaque)

    rgba = rgb.convert("RGBA")
    rgba.putalpha(alpha)

    stem = safe_name(src)
    full_path = full_dir / f"{stem}_transparent.png"
    trim_path = trim_dir / f"{stem}_transparent_trimmed.png"
    preview_path = preview_dir / f"{stem}_preview.jpg"

    rgba.save(full_path)
    trimmed = trimmed_rgba(rgba, alpha, padding)
    trimmed.save(trim_path)
    save_preview(trim_path, preview_path)
    return full_path, trim_path, preview_path, rgba.size, trimmed.size


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Remove black or simple solid backgrounds from local images.")
    parser.add_argument("inputs", nargs="+", help="Image files, folders, or glob patterns.")
    parser.add_argument("--output-dir", help="Output folder. Defaults to cutout_transparent_png beside the first input.")
    parser.add_argument("--bg-color", type=parse_bg_color, default=(0, 0, 0), help="Background color as R,G,B. Default: 0,0,0.")
    parser.add_argument("--edge-start", type=float, default=2.0, help="Distance at or below this becomes transparent.")
    parser.add_argument("--opaque-at", type=float, default=24.0, help="Distance at or above this becomes opaque.")
    parser.add_argument("--tolerance-start", type=float, help="Alias for --edge-start for non-black solid colors.")
    parser.add_argument("--opaque-distance", type=float, help="Alias for --opaque-at for non-black solid colors.")
    parser.add_argument("--padding", type=int, default=24, help="Trimmed output padding in pixels.")
    parser.add_argument("--no-zip", action="store_true", help="Do not refresh the ZIP archive.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    files = expand_inputs(args.inputs)
    if not files:
        raise SystemExit("No supported image files found.")

    start = args.tolerance_start if args.tolerance_start is not None else args.edge_start
    opaque = args.opaque_distance if args.opaque_distance is not None else args.opaque_at
    if opaque <= start:
        raise SystemExit("opaque-at / opaque-distance must be greater than edge-start / tolerance-start.")

    out_root = Path(args.output_dir).resolve() if args.output_dir else files[0].parent / "cutout_transparent_png"
    out_root.mkdir(parents=True, exist_ok=True)

    results = []
    for src in files:
        results.append(process_file(src, out_root, args.bg_color, start, opaque, args.padding))

    zip_path = out_root / "cutout_transparent_png.zip"
    if not args.no_zip:
        zip_outputs(out_root, zip_path)

    print(f"processed={len(results)}")
    print(f"out_root={out_root}")
    print(f"full_canvas={out_root / 'full_canvas'}")
    print(f"trimmed={out_root / 'trimmed'}")
    print(f"previews={out_root / 'previews'}")
    if not args.no_zip:
        print(f"zip={zip_path}")
    for full_path, trim_path, preview_path, full_size, trim_size in results:
        print(
            f"{trim_path.name}: full={full_path.name} {full_size}, "
            f"trimmed={trim_size}, preview={preview_path.name}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
