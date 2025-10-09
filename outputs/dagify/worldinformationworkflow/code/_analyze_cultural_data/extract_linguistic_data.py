# -- PRD --
# 1. BULLET: Implement the extract_linguistic_data function to process the input list of
#   languages and return a list of extracted linguistic data.
#   Reason: This is necessary to fulfill the requirement of analyzing cultural data by
#           extracting relevant information from the given languages.
#   Impact: The extracted linguistic data will be used to identify cultural patterns
#           and themes, which will be crucial for the overall analysis.
#   Complexity: MEDIUM
#   Method: The implementation can involve using natural language processing techniques
#           or simple string manipulation to extract relevant data from the
#           input languages.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle edge cases where the input list is empty or contains invalid data.
#   Reason: To ensure the robustness of the function and prevent potential errors.
#   Impact: Proper handling of edge cases will improve the overall reliability of the
#           cultural data analysis pipeline.
#   Complexity: LOW
#   Method: Implement simple checks at the beginning of the function to handle empty or
#           invalid inputs.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Consider integrating with external linguistic data sources or APIs to enhance
#   the extraction process.
#   Reason: To potentially improve the accuracy and comprehensiveness of the extracted
#           linguistic data.
#   Impact: Integrating external data sources could significantly enhance the quality
#           of the analysis, but may also introduce additional complexity
#           and dependencies.
#   Complexity: HIGH
#   Method: Research and evaluate potential external linguistic data sources or APIs,
#           and design an integration strategy that balances benefits and
#           complexity.
# -- END PRD --

from typing import List

import re


def extract_linguistic_data(languages: str) -> List[str]:
    """
    A shim function that extracts linguistic data from the given list of languages.

    Args:
        languages: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Handle edge cases - empty or invalid input
    if not languages or not isinstance(languages, str):
        return []
    
    # Clean and normalize the input string
    cleaned_languages = languages.strip()
    if not cleaned_languages:
        return []
    
    # Split the languages string into individual language entries
    # Handle various separators (comma, semicolon, newline)
    language_list = re.split(r'[,;\n]+', cleaned_languages)
    
    extracted_data = []
    
    for lang in language_list:
        lang = lang.strip()
        if not lang:
            continue
            
        # Extract linguistic features from each language entry
        linguistic_features = []
        
        # Extract language family information if present
        if 'indo-european' in lang.lower():
            linguistic_features.append('family:indo-european')
        elif 'sino-tibetan' in lang.lower():
            linguistic_features.append('family:sino-tibetan')
        elif 'afro-asiatic' in lang.lower():
            linguistic_features.append('family:afro-asiatic')
        
        # Extract script information
        if 'latin' in lang.lower() or 'roman' in lang.lower():
            linguistic_features.append('script:latin')
        elif 'cyrillic' in lang.lower():
            linguistic_features.append('script:cyrillic')
        elif 'arabic' in lang.lower():
            linguistic_features.append('script:arabic')
        elif 'chinese' in lang.lower() or 'mandarin' in lang.lower():
            linguistic_features.append('script:chinese')
        
        # Extract geographic region information
        if any(region in lang.lower() for region in ['european', 'europe']):
            linguistic_features.append('region:europe')
        elif any(region in lang.lower() for region in ['asian', 'asia']):
            linguistic_features.append('region:asia')
        elif any(region in lang.lower() for region in ['african', 'africa']):
            linguistic_features.append('region:africa')
        
        # Extract basic language name and normalize it
        lang_name = re.sub(r'[^a-zA-Z\s]', '', lang).strip().lower()
        if lang_name:
            linguistic_features.append(f'language:{lang_name}')
        
        # Add the extracted features as a combined string
        if linguistic_features:
            extracted_data.append('|'.join(linguistic_features))
        else:
            # Fallback: just add the cleaned language name
            if lang_name:
                extracted_data.append(f'language:{lang_name}')
    
    return extracted_data