import io
import pytest

from types import SimpleNamespace

import modules.utils.pdf_parser as pdf_parser


class DummyPage:
    def __init__(self, text):
        self._text = text

    def extract_text(self):
        return self._text


class DummyPdfReader:
    def __init__(self, pages):
        self.pages = [DummyPage(p) for p in pages]


def test_extract_text_success(monkeypatch):
    # Arrange: monkeypatch PdfReader to return dummy pages
    monkeypatch.setattr(
        "modules.utils.pdf_parser.PyPDF2.PdfReader",
        lambda uploaded_file: DummyPdfReader(["Page 1 text", "Page 2 text"]),
    )

    fake_file = io.BytesIO(b"%PDF-1.4 fake")

    # Act
    result = pdf_parser.extract_text_from_pdf(fake_file)

    # Assert
    assert "Page 1 text" in result
    assert "Page 2 text" in result


def test_extract_text_no_file_raises():
    with pytest.raises(FileNotFoundError):
        pdf_parser.extract_text_from_pdf(None)


def test_extract_text_reader_raises(monkeypatch):
    # Simulate PdfReader raising an unexpected error
    def _bad_reader(_):
        raise RuntimeError("corrupt pdf")

    monkeypatch.setattr("modules.utils.pdf_parser.PyPDF2.PdfReader", _bad_reader)

    fake_file = io.BytesIO(b"not a pdf")

    with pytest.raises(ValueError) as exc:
        pdf_parser.extract_text_from_pdf(fake_file)

    assert "Error reading PDF" in str(exc.value)
