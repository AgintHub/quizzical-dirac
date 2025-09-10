# -- PRD --
# 1. BULLET: Receive the preprocessed document from the document_preprocessing node.
#   Reason: The preprocessed document is required to accurately detect languages.
#   Impact: LOW
#   Complexity: LOW
#   Method: Use the output of the document_preprocessing node as input.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Use a language detection library (e.g. langdetect, polyglot) to analyze the
#   preprocessed document and detect languages.
#   Reason: Language detection libraries provide accurate and efficient language
#           detection capabilities.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Utilize a library's API to analyze the document and return a list of
#           detected languages.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Filter the detected languages to remove any languages with low confidence
#   scores.
#   Reason: Low confidence scores may indicate inaccurate language detection.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Apply a threshold to the confidence scores to filter out languages with low
#           confidence.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Return the list of detected languages in the output structure.
#   Reason: The output structure requires a list of detected languages.
#   Impact: LOW
#   Complexity: LOW
#   Method: Format the list of detected languages according to the output structure.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class DocumentPreprocessingOutput(BaseModel):
    """Pydantic model for document_preprocessing node outputs."""
    preprocessed_document: str = Field(..., description="The preprocessed document.")


class LanguageDetectionOutput(BaseModel):
    """Pydantic model for language_detection node outputs."""
    languages: List[str] = Field(..., description="The languages detected in the document.")


def language_detection(document_preprocessing_input: DocumentPreprocessingOutput, **kwargs) -> LanguageDetectionOutput:
    """Detect the languages present in the document.

    Args:
        document_preprocessing_input: Input from the 'document_preprocessing' node.
        **kwargs: Additional keyword arguments.

    Returns:
        LanguageDetectionOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return LanguageDetectionOutput(
        languages=[],
    )