#!/usr/bin/env python3
"""Exercise LibreOffice Writer, Calc, and Impress file-format filters."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
import zipfile
from pathlib import Path

MARKER = "Erdem Office macOS baseline"
NAMESPACES = (
    'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
    'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
    'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
    'xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" '
    'xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"'
)


def convert(
    soffice: Path, profile: Path, source: Path, target: str, output: Path
) -> Path:
    output.mkdir(parents=True, exist_ok=True)
    command = [
        str(soffice),
        "--headless",
        "--nologo",
        "--nodefault",
        "--nofirststartwizard",
        f"-env:UserInstallation={profile.as_uri()}",
        "--convert-to",
        target,
        "--outdir",
        str(output),
        str(source),
    ]
    result = subprocess.run(
        command, text=True, capture_output=True, timeout=120, check=False
    )
    if result.returncode:
        raise RuntimeError(
            f"Conversion failed: {' '.join(command)}\n{result.stdout}{result.stderr}"
        )
    extension = target.split(":", 1)[0]
    converted = output / f"{source.stem}.{extension}"
    if not converted.is_file():
        raise RuntimeError(
            f"Expected {converted}; LibreOffice reported:\n{result.stdout}{result.stderr}"
        )
    return converted


def check_package(path: Path, expected_mimetype: str | None = None) -> None:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if expected_mimetype:
            actual = archive.read("mimetype").decode()
            if actual != expected_mimetype:
                raise RuntimeError(
                    f"{path}: expected {expected_mimetype}, found {actual}"
                )
        elif "[Content_Types].xml" not in names:
            raise RuntimeError(f"{path}: missing OOXML [Content_Types].xml")
        content = b"".join(
            archive.read(name) for name in names if name.endswith(".xml")
        )
        if MARKER.encode() not in content:
            raise RuntimeError(f"{path}: test marker was not preserved")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "soffice", type=Path, help="Path to the built soffice executable"
    )
    args = parser.parse_args()
    soffice = args.soffice.resolve()
    if not soffice.is_file():
        parser.error(f"not a file: {soffice}")

    with tempfile.TemporaryDirectory(prefix="erdem-office-smoke-") as temporary:
        root = Path(temporary)
        profile = root / "profile"
        sources = root / "sources"
        generated = root / "generated"
        sources.mkdir()

        writer = sources / "writer.fodt"
        writer.write_text(
            f'<?xml version="1.0" encoding="UTF-8"?><office:document {NAMESPACES} '
            'office:mimetype="application/vnd.oasis.opendocument.text" office:version="1.3">'
            f"<office:body><office:text><text:p>{MARKER}</text:p></office:text></office:body>"
            "</office:document>",
            encoding="utf-8",
        )
        calc = sources / "calc.fods"
        calc.write_text(
            f'<?xml version="1.0" encoding="UTF-8"?><office:document {NAMESPACES} '
            'office:mimetype="application/vnd.oasis.opendocument.spreadsheet" office:version="1.3">'
            f'<office:body><office:spreadsheet><table:table table:name="Smoke"><table:table-row>'
            f'<table:table-cell office:value-type="string"><text:p>{MARKER}</text:p></table:table-cell>'
            "</table:table-row></table:table></office:spreadsheet></office:body></office:document>",
            encoding="utf-8",
        )
        impress = sources / "impress.fodp"
        impress.write_text(
            f'<?xml version="1.0" encoding="UTF-8"?><office:document {NAMESPACES} '
            'office:mimetype="application/vnd.oasis.opendocument.presentation" office:version="1.3">'
            f'<office:body><office:presentation><draw:page draw:name="Slide 1">'
            f"<draw:frame><draw:text-box><text:p>{MARKER}</text:p></draw:text-box></draw:frame>"
            "</draw:page></office:presentation></office:body></office:document>",
            encoding="utf-8",
        )

        odt = convert(soffice, profile, writer, "odt:writer8", generated)
        docx = convert(soffice, profile, writer, "docx:Office Open XML Text", generated)
        pdf = convert(soffice, profile, writer, "pdf:writer_pdf_Export", generated)
        ods = convert(soffice, profile, calc, "ods:calc8", generated)
        xlsx = convert(soffice, profile, calc, "xlsx:Calc MS Excel 2007 XML", generated)
        odp = convert(soffice, profile, impress, "odp:impress8", generated)
        pptx = convert(
            soffice, profile, impress, "pptx:Impress MS PowerPoint 2007 XML", generated
        )

        check_package(odt, "application/vnd.oasis.opendocument.text")
        check_package(ods, "application/vnd.oasis.opendocument.spreadsheet")
        check_package(odp, "application/vnd.oasis.opendocument.presentation")
        for package in (docx, xlsx, pptx):
            check_package(package)
        if pdf.read_bytes()[:5] != b"%PDF-":
            raise RuntimeError(f"{pdf}: invalid PDF header")

        roundtrips = (
            (odt, "odt:writer8", "application/vnd.oasis.opendocument.text"),
            (docx, "odt:writer8", "application/vnd.oasis.opendocument.text"),
            (ods, "ods:calc8", "application/vnd.oasis.opendocument.spreadsheet"),
            (xlsx, "ods:calc8", "application/vnd.oasis.opendocument.spreadsheet"),
            (odp, "odp:impress8", "application/vnd.oasis.opendocument.presentation"),
            (pptx, "odp:impress8", "application/vnd.oasis.opendocument.presentation"),
        )
        for source, target, mimetype in roundtrips:
            converted = convert(
                soffice,
                profile,
                source,
                target,
                root / f"roundtrip-{source.suffix[1:]}",
            )
            check_package(converted, mimetype)

        print("PASS: Writer ODT/DOCX/PDF, Calc ODS/XLSX, and Impress ODP/PPTX")


if __name__ == "__main__":
    main()
