# -- PRD --
# 1. BULLET: Compare the generated world definition against the workflow objectives to
#   check for alignment.
#   Reason: To ensure the world definition is relevant and meaningful in the context of
#           the workflow's goals.
#   Impact: Improves the accuracy and relevance of the world definition in relation to
#           workflow objectives.
#   Complexity: MEDIUM
#   Method: Implement a comparison algorithm that assesses the semantic similarity
#           between the world definition and workflow objectives.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Identify and flag any discrepancies or misalignments between the world
#   definition and objectives.
#   Reason: To highlight areas that need refinement or adjustment to better align with
#           workflow goals.
#   Impact: Enhances the quality of the world definition by pinpointing specific areas
#           for improvement.
#   Complexity: HIGH
#   Method: Utilize natural language processing techniques to analyze and identify
#           discrepancies between the definition and objectives.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Return the validated world definition, potentially with adjustments or
#   suggestions for improvement.
#   Reason: To provide a refined world definition that is better aligned with workflow
#           objectives.
#   Impact: Facilitates the generation of a high-quality world definition that meets
#           workflow needs.
#   Complexity: LOW
#   Method: Output the validated definition, incorporating any necessary adjustments or
#           recommendations.
# -- END PRD --

import re
from difflib import SequenceMatcher


def validate_definition_alignment(definition: str, objectives: str) -> str:
    """
    Validates if the generated world definition aligns with the workflow objectives.

    Args:
        definition: Input parameter of type str
objectives: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    # Clean and normalize both texts for comparison
    def clean_text(text):
        # Remove extra whitespace and normalize case
        text = re.sub(r'\s+', ' ', text.strip().lower())
        # Remove punctuation for better semantic comparison
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    cleaned_definition = clean_text(definition)
    cleaned_objectives = clean_text(objectives)
    
    # Extract key terms from both texts
    def extract_key_terms(text):
        # Split into words and filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        words = text.split()
        return [word for word in words if len(word) > 2 and word not in stop_words]
    
    definition_terms = extract_key_terms(cleaned_definition)
    objective_terms = extract_key_terms(cleaned_objectives)
    
    # Calculate semantic similarity using term overlap
    common_terms = set(definition_terms) & set(objective_terms)
    total_unique_terms = set(definition_terms) | set(objective_terms)
    
    # Calculate similarity scores
    term_overlap_score = len(common_terms) / len(total_unique_terms) if total_unique_terms else 0
    sequence_similarity = SequenceMatcher(None, cleaned_definition, cleaned_objectives).ratio()
    
    # Combined alignment score
    alignment_score = (term_overlap_score * 0.6 + sequence_similarity * 0.4)
    
    # Identify discrepancies and provide feedback
    discrepancies = []
    suggestions = []
    
    # Check for missing key objective terms in definition
    missing_terms = set(objective_terms) - set(definition_terms)
    if missing_terms:
        discrepancies.append(f"Missing key objective terms: {', '.join(list(missing_terms)[:5])}")
        suggestions.append(f"Consider incorporating these terms: {', '.join(list(missing_terms)[:3])}")
    
    # Check alignment threshold
    if alignment_score < 0.3:
        discrepancies.append("Low semantic alignment between definition and objectives")
        suggestions.append("Revise the definition to better reflect the stated objectives")
    elif alignment_score < 0.6:
        discrepancies.append("Moderate alignment - some improvements possible")
        suggestions.append("Consider strengthening the connection to key objective themes")
    
    # Generate validation result
    if alignment_score >= 0.7:
        result = f"VALIDATED: The world definition shows strong alignment with objectives (score: {alignment_score:.2f}).\n\nDefinition: {definition}"
    elif alignment_score >= 0.4:
        result = f"PARTIALLY VALIDATED: The world definition shows moderate alignment with objectives (score: {alignment_score:.2f}).\n\nDefinition: {definition}\n\nSuggested improvements:\n" + "\n".join([f"- {s}" for s in suggestions])
    else:
        result = f"NEEDS REVISION: The world definition shows poor alignment with objectives (score: {alignment_score:.2f}).\n\nIdentified issues:\n" + "\n".join([f"- {d}" for d in discrepancies]) + "\n\nSuggested improvements:\n" + "\n".join([f"- {s}" for s in suggestions]) + f"\n\nOriginal definition: {definition}"
    
    return result