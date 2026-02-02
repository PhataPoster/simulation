import re
import sys
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def extract_a_t(xml_bytes: bytes) -> list[str]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []

    texts: list[str] = []
    for node in root.findall(".//a:t", NS):
        if not node.text:
            continue
        text = re.sub(r"\s+", " ", node.text).strip()
        if text:
            texts.append(text)
    return texts


def _slide_num(path: str, prefix: str) -> int:
    m = re.search(rf"{re.escape(prefix)}(\d+)\.xml$", path)
    return int(m.group(1)) if m else 10**9


def extract_pptx_text(pptx_path: Path) -> tuple[str, int, int]:
    out_txt = pptx_path.parent / (pptx_path.stem + "_extracted.txt")

    with zipfile.ZipFile(pptx_path, "r") as z:
        names = z.namelist()

        slide_files = [
            n
            for n in names
            if n.startswith("ppt/slides/slide") and n.endswith(".xml")
        ]
        slide_files.sort(key=lambda n: _slide_num(n, "slide"))

        notes_files = [
            n
            for n in names
            if n.startswith("ppt/notesSlides/notesSlide") and n.endswith(".xml")
        ]
        notes_files.sort(key=lambda n: _slide_num(n, "notesSlide"))

        slide_text: dict[int, list[str]] = {}
        for sf in slide_files:
            num = _slide_num(sf, "slide")
            slide_text[num] = extract_a_t(z.read(sf))

        notes_text: dict[int, list[str]] = {}
        for nf in notes_files:
            num = _slide_num(nf, "notesSlide")
            notes_text[num] = extract_a_t(z.read(nf))

    lines: list[str] = []
    lines.append(f"Source: {pptx_path}")
    lines.append("")

    for i in sorted(slide_text.keys()):
        lines.append(f"=== Slide {i} ===")
        texts = slide_text[i]
        if texts:
            for t in texts:
                lines.append(f"- {t}")
        else:
            lines.append("(no extractable text)")

        nt = notes_text.get(i)
        if nt:
            lines.append("--- Notes ---")
            for t in nt:
                lines.append(f"* {t}")

        lines.append("")

    out_txt.write_text("\n".join(lines), encoding="utf-8")
    return str(out_txt), len(slide_text), len(notes_text)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python extract_pptx_text.py <path-to-pptx>")
        return 2

    pptx_path = Path(sys.argv[1]).expanduser().resolve()
    if not pptx_path.exists():
        print(f"File not found: {pptx_path}")
        return 1

    out_txt, slide_count, notes_count = extract_pptx_text(pptx_path)
    print(f"Wrote: {out_txt}")
    print(f"Slides found: {slide_count}")
    print(f"Notes found: {notes_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
