# -- PRD --
# 1. BULLET: Develop a natural language processing (NLP) or text generation algorithm to
#   craft a narrative that integrates the given themes, geographical
#   patterns, and cultural patterns.
#   Reason: To create a cohesive and meaningful story from the provided inputs.
#   Impact: Enables the generation of a comprehensive narrative that can be used for
#           further analysis or presentation.
#   Complexity: HIGH
#   Method: Utilize a deep learning-based text generation model, such as a transformer,
#           fine-tuned on relevant narrative structures and patterns.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement input validation and preprocessing to ensure that the themes,
#   geographical patterns, and cultural patterns are properly formatted and
#   cleaned before being used to craft the narrative.
#   Reason: To prevent errors and ensure the quality of the generated narrative.
#   Impact: Improves the robustness and reliability of the narrative generation
#           process.
#   Complexity: MEDIUM
#   Method: Apply standard preprocessing techniques such as tokenization, stopword
#           removal, and normalization.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Provide an option to customize the narrative generation based on specific
#   requirements or preferences, such as tone, style, or length.
#   Reason: To make the narrative generation more flexible and adaptable to different
#           use cases.
#   Impact: Enhances the usability and versatility of the crafted narrative.
#   Complexity: MEDIUM
#   Method: Introduce parameters that control the narrative's characteristics and use
#           conditional generation techniques.
# -- END PRD --

import re
import random


def craft_integrated_narrative(themes: str, geo_patterns: str, cultural_patterns: str) -> str:
    """
    Crafts a comprehensive narrative integrating themes, geographical patterns, and cultural patterns into a cohesive story.

    Args:
        themes: Input parameter of type str
geo_patterns: Input parameter of type str
cultural_patterns: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    # Input validation and preprocessing
    def clean_and_validate_input(text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        # Remove extra whitespace, normalize text
        cleaned = re.sub(r'\s+', ' ', text.strip())
        # Remove special characters that might interfere with narrative flow
        cleaned = re.sub(r'[^a-zA-Z0-9\s.,;:!?-]', '', cleaned)
        return cleaned
    
    # Clean inputs
    clean_themes = clean_and_validate_input(themes)
    clean_geo = clean_and_validate_input(geo_patterns)
    clean_cultural = clean_and_validate_input(cultural_patterns)
    
    # If all inputs are empty, return a default message
    if not clean_themes and not clean_geo and not clean_cultural:
        return "A story waiting to be told, where themes, places, and cultures converge in harmony."
    
    # Narrative templates and connectors
    narrative_starters = [
        "In a land where",
        "Once upon a time, in a place where",
        "The story begins in a region where",
        "Across the landscapes where",
        "In the heart of territories where"
    ]
    
    theme_connectors = [
        "guided by the principles of",
        "shaped by the essence of",
        "influenced by the themes of",
        "driven by the core values of",
        "embodying the spirit of"
    ]
    
    geo_connectors = [
        "the geographical patterns reveal",
        "the landscape tells a story of",
        "the terrain speaks of",
        "the natural formations suggest",
        "the geographical features demonstrate"
    ]
    
    cultural_connectors = [
        "the cultural tapestry weaves together",
        "the traditions and customs reflect",
        "the cultural heritage embodies",
        "the social patterns indicate",
        "the cultural fabric reveals"
    ]
    
    narrative_endings = [
        "creating a harmonious blend of tradition and progress.",
        "forging a unique identity that bridges past and future.",
        "establishing a legacy that resonates through generations.",
        "building a community where diversity becomes strength.",
        "crafting a story that continues to evolve and inspire."
    ]
    
    # Build narrative sections
    narrative_parts = []
    
    # Opening
    starter = random.choice(narrative_starters)
    narrative_parts.append(starter)
    
    # Integrate geographical patterns first
    if clean_geo:
        geo_connector = random.choice(geo_connectors)
        geo_section = f"{geo_connector} {clean_geo}"
        narrative_parts.append(geo_section)
    
    # Integrate cultural patterns
    if clean_cultural:
        cultural_connector = random.choice(cultural_connectors)
        cultural_section = f"{cultural_connector} {clean_cultural}"
        narrative_parts.append(cultural_section)
    
    # Integrate themes
    if clean_themes:
        theme_connector = random.choice(theme_connectors)
        theme_section = f"The community finds itself {theme_connector} {clean_themes}"
        narrative_parts.append(theme_section)
    
    # Conclusion
    ending = random.choice(narrative_endings)
    narrative_parts.append(ending)
    
    # Join all parts into a cohesive narrative
    # Add appropriate punctuation and connectors
    full_narrative = ""
    for i, part in enumerate(narrative_parts):
        if i == 0:
            full_narrative += part
        elif i == len(narrative_parts) - 1:
            full_narrative += f", ultimately {part}"
        else:
            connectors = [", where ", ". Here, ", ", and ", ". Moreover, "]
            connector = random.choice(connectors)
            full_narrative += f"{connector}{part}"
    
    # Ensure proper capitalization and punctuation
    full_narrative = full_narrative.strip()
    if not full_narrative.endswith(('.', '!', '?')):
        full_narrative += '.'
    
    # Capitalize first letter
    if full_narrative:
        full_narrative = full_narrative[0].upper() + full_narrative[1:]
    
    return full_narrative