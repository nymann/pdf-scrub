from pathlib import Path
from typing import Iterable

from pdf_information import PDFInfo

from pdf_scrub.toolkit import compress_pdf
from pdf_scrub.toolkit import decrypt_pdf
from pdf_scrub.toolkit import find_possible_watermark_needles
from pdf_scrub.toolkit import remove_metadata
from pdf_scrub.toolkit import remove_watermark
from pdf_scrub.toolkit import uncompress_pdf


class PDF:
    def __init__(self, pdf_file: Path) -> None:
        self.pdf_file = pdf_file
        self.pdf_info = PDFInfo.from_cmd(pdf_file=pdf_file)

    def scrub(self, compress: bool) -> Iterable[bytes]:
        pdf_bytes_without_metadata: bytes = remove_metadata(pdf_bytes=self._get_uncompressed())
        for needle in find_possible_watermark_needles(pdf_bytes=pdf_bytes_without_metadata, pdf_info=self.pdf_info):
            potentially_clean_pdf = remove_watermark(pdf_bytes=pdf_bytes_without_metadata, needle=needle)
            if compress:
                yield compress_pdf(pdf_bytes=potentially_clean_pdf)
            else:
                yield potentially_clean_pdf

    def _get_uncompressed(self) -> bytes:
        if self.pdf_info.encrypted:
            decrypted: bytes = decrypt_pdf(pdf_file=self.pdf_file)
        else:
            with open(file=self.pdf_file, mode="rb") as pdf_buffer:
                decrypted = pdf_buffer.read()
        return uncompress_pdf(pdf_file_buffer=decrypted)
