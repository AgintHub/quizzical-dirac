# -- PRD --
# 1. BULLET: Combine the extracted text, handwritten text, and converted components into a
#   single data structure.
#   Reason: This step is necessary to gather all the relevant information into a single
#           data structure for further processing.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use a Python dictionary to store the combined data.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Use a JSON library to convert the combined data structure into a JSON string.
#   Reason: This step is necessary to generate the output in JSON format.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the `json` library in Python to convert the dictionary into a JSON
#           string.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Use a Markdown library to convert the combined data structure into a Markdown
#   string.
#   Reason: This step is necessary to generate the output in Markdown format.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a Markdown library such as `markdown` in Python to convert the
#           dictionary into a Markdown string.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Format the JSON and Markdown strings according to the required output
#   structure.
#   Reason: This step is necessary to ensure that the output is in the correct format.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use string formatting techniques to format the JSON and Markdown strings.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class TextExtractionOutput(BaseModel):
    """Pydantic model for text_extraction node outputs."""
    extracted_text: str = Field(..., description="The extracted text.")
    layout_info: str = Field(..., description="The layout information of the extracted text.")


class HandwrittenTextRecognitionOutput(BaseModel):
    """Pydantic model for handwritten_text_recognition node outputs."""
    handwritten_text: str = Field(..., description="The recognized handwritten text.")


class ComponentConversionOutput(BaseModel):
    """Pydantic model for component_conversion node outputs."""
    converted_components: List[str] = Field(..., description="The converted components in natural language text.")


class OutputGenerationOutput(BaseModel):
    """Pydantic model for output_generation node outputs."""
    json_output: str = Field(..., description="The output in JSON format.")
    markdown_output: str = Field(..., description="The output in Markdown format.")


def output_generation(text_extraction_input: TextExtractionOutput, handwritten_text_recognition_input: HandwrittenTextRecognitionOutput, component_conversion_input: ComponentConversionOutput, **kwargs) -> OutputGenerationOutput:
    """Generate the output in JSON and Markdown formats.

    Args:
        text_extraction_input: Input from the 'text_extraction' node.
        handwritten_text_recognition_input: Input from the 'handwritten_text_recognition' node.
        component_conversion_input: Input from the 'component_conversion' node.
        **kwargs: Additional keyword arguments.

    Returns:
        OutputGenerationOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return OutputGenerationOutput(
        json_output="",
        markdown_output="",
    )