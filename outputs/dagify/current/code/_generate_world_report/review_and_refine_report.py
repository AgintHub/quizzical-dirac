# -- PRD --
# 1. BULLET: Implement a review mechanism that checks the draft report for accuracy by
#   comparing it with the original findings.
#   Reason: To ensure the refined report is accurate and consistent with the original
#           findings.
#   Impact: Improves the reliability of the final report.
#   Complexity: MEDIUM
#   Method: Use natural language processing (NLP) techniques to compare the draft and
#           original findings.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Refine the report's coherence by restructuring sentences or sections if
#   necessary.
#   Reason: To enhance the readability and flow of the final report.
#   Impact: Makes the report more understandable and user-friendly.
#   Complexity: HIGH
#   Method: Employ machine learning models trained on coherent text structures to
#           suggest improvements.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Validate the refined report against a set of predefined quality metrics.
#   Reason: To ensure the report meets the required standards.
#   Impact: Ensures the final report is of high quality.
#   Complexity: LOW
#   Method: Use a checklist of quality metrics to assess the report's quality.
# -- END PRD --

import re
from difflib import SequenceMatcher


def review_and_refine_report(draft: str, original_findings: str) -> str:
    """
    Reviews and refines a draft report for accuracy and coherence based on original findings.

    Args:
        draft: Input parameter of type str
original_findings: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    # Step 1: Review mechanism - compare draft with original findings for accuracy
    # Split both texts into sentences for comparison
    draft_sentences = re.split(r'[.!?]+', draft.strip())
    original_sentences = re.split(r'[.!?]+', original_findings.strip())
    
    # Clean and filter empty sentences
    draft_sentences = [s.strip() for s in draft_sentences if s.strip()]
    original_sentences = [s.strip() for s in original_sentences if s.strip()]
    
    # Check for consistency between draft and original findings
    inconsistent_sentences = []
    for draft_sent in draft_sentences:
        # Find the most similar sentence in original findings
        max_similarity = 0
        for orig_sent in original_sentences:
            similarity = SequenceMatcher(None, draft_sent.lower(), orig_sent.lower()).ratio()
            max_similarity = max(max_similarity, similarity)
        
        # If similarity is too low, mark as potentially inconsistent
        if max_similarity < 0.3:
            inconsistent_sentences.append(draft_sent)
    
    # Step 2: Refine coherence by restructuring sentences
    refined_sentences = []
    for sentence in draft_sentences:
        # Basic coherence improvements
        refined_sentence = sentence.strip()
        
        # Fix common coherence issues
        # Add proper transitions if sentence starts abruptly
        if refined_sentence and not re.match(r'^(However|Therefore|Additionally|Furthermore|Moreover|In conclusion)', refined_sentence, re.IGNORECASE):
            # Check if it's a continuation thought
            if len(refined_sentences) > 0 and not refined_sentence[0].isupper():
                refined_sentence = refined_sentence.capitalize()
        
        # Ensure proper punctuation
        if refined_sentence and not refined_sentence.endswith(('.', '!', '?')):
            refined_sentence += '.'
        
        # Improve sentence structure by fixing run-on sentences
        if len(refined_sentence) > 150 and ' and ' in refined_sentence:
            # Split long sentences with multiple 'and' conjunctions
            parts = refined_sentence.split(' and ', 1)
            if len(parts) == 2:
                first_part = parts[0].strip() + '.'
                second_part = 'Additionally, ' + parts[1].strip()
                refined_sentences.append(first_part)
                refined_sentence = second_part
        
        refined_sentences.append(refined_sentence)
    
    # Step 3: Validate against quality metrics
    refined_text = ' '.join(refined_sentences)
    
    # Quality metric checks
    quality_issues = []
    
    # Check 1: Minimum length requirement
    if len(refined_text.split()) < 10:
        quality_issues.append("Report too short")
    
    # Check 2: Proper sentence structure
    sentence_count = len([s for s in refined_sentences if s.strip()])
    if sentence_count < 3:
        quality_issues.append("Insufficient sentence count")
    
    # Check 3: Coherence check - ensure logical flow
    transition_words = ['however', 'therefore', 'additionally', 'furthermore', 'moreover', 'consequently', 'thus']
    has_transitions = any(word in refined_text.lower() for word in transition_words)
    if not has_transitions and sentence_count > 5:
        # Add some transitions for better flow
        sentences_list = list(refined_sentences)
        if len(sentences_list) >= 2:
            sentences_list[1] = 'Furthermore, ' + sentences_list[1].lower()
        if len(sentences_list) >= 3:
            sentences_list[-1] = 'In conclusion, ' + sentences_list[-1].lower()
        refined_text = ' '.join(sentences_list)
    
    # Check 4: Consistency with original findings
    if inconsistent_sentences:
        # Add a note about potential inconsistencies
        refined_text += f" [Note: {len(inconsistent_sentences)} statements may need verification against original findings.]"
    
    # Final cleanup
    refined_text = re.sub(r'\s+', ' ', refined_text).strip()
    
    return refined_text