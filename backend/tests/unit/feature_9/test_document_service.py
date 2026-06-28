import io
from unittest.mock import patch, MagicMock

from app.services.document_service import DocumentService


def test_validate_file_extension_permitida():
    # Act
    valido, msg = DocumentService.validate_file_extension("contrato.pdf")

    assert valido is True
    assert msg is None


def test_validate_file_extension_nao_permitida():
    # Act
    valido, msg = DocumentService.validate_file_extension("virus.exe")

    assert valido is False
    assert msg is not None


def test_validate_file_extension_sem_extensao():
    # Act
    valido, msg = DocumentService.validate_file_extension("arquivo_sem_ponto")

    assert valido is False


def test_validate_file_size_dentro_do_limite():
    arquivo = io.BytesIO(b"conteudo pequeno")

    # Act
    valido, msg = DocumentService.validate_file_size(arquivo)

    assert valido is True
    assert msg is None


def test_validate_file_size_acima_do_limite(monkeypatch):
    # Arrange: rebaixa o limite para 5 bytes
    monkeypatch.setattr(DocumentService, "MAX_SIZE", 5)
    arquivo = io.BytesIO(b"conteudo bem maior que cinco bytes")

    # Act
    valido, msg = DocumentService.validate_file_size(arquivo)

    assert valido is False








