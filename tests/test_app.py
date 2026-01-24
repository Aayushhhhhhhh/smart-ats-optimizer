import pytest
from unittest.mock import patch, MagicMock
import app
import os

def test_calculate_match_score():
    text1 = "Python machine learning"
    text2 = "Python machine learning"
    assert app.calculate_match_score(text1, text2) == 100.0

    text3 = "Java spring boot"
    assert app.calculate_match_score(text1, text3) == 0.0

    # Partial match
    text4 = "Python data science"
    score = app.calculate_match_score(text1, text4)
    assert 0 < score < 100

from reportlab.pdfgen import canvas

@pytest.fixture
def test_pdf_path(tmp_path):
    pdf_path = tmp_path / "test_resume.pdf"
    c = canvas.Canvas(str(pdf_path))
    c.drawString(100, 750, "This is a test resume.")
    c.save()
    return str(pdf_path)

def test_input_pdf_text(test_pdf_path):
    with open(test_pdf_path, "rb") as f:
        text = app.input_pdf_text(f)
        assert "This is a test resume." in text

@patch("app.ChatOpenAI")
def test_get_llm_response(mock_chat_openai):
    # Setup mock
    mock_llm_instance = MagicMock()
    mock_chat_openai.return_value = mock_llm_instance

    expected_response_content = "Mocked AI response"
    mock_response = MagicMock()
    mock_response.content = expected_response_content
    mock_llm_instance.invoke.return_value = mock_response

    input_text = "Test prompt"
    response = app.get_llm_response(input_text)

    assert response == expected_response_content
    mock_llm_instance.invoke.assert_called_once_with(input_text)
