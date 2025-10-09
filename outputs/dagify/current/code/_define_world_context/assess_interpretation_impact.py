# -- PRD --
# 1. BULLET: Develop a method to quantify or qualify the impact of different
#   interpretations on workflow objectives.
#   Reason: To provide a systematic way of assessing how different understandings of
#           'world' affect the workflow's goals.
#   Impact: Enables the selection of the most appropriate interpretation based on its
#           potential impact.
#   Complexity: MEDIUM
#   Method: Use a combination of natural language processing (NLP) and machine learning
#           techniques to analyze the interpretations and objectives, and
#           then apply a scoring or ranking algorithm to determine their
#           impact.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Consider the context and constraints provided by the workflow purpose and
#   input data.
#   Reason: To ensure the impact assessment is relevant and tailored to the specific
#           workflow.
#   Impact: Increases the accuracy and relevance of the impact analysis by taking into
#           account the specific context.
#   Complexity: LOW
#   Method: Integrate the workflow purpose and input data analysis into the impact
#           assessment algorithm, potentially through the use of contextual
#           embeddings or by conditioning the analysis on these inputs.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Ensure the output is in a usable format for downstream processing.
#   Reason: To facilitate the integration of the impact analysis into the overall
#           workflow definition process.
#   Impact: Simplifies the subsequent steps in the workflow by providing a clear and
#           structured output.
#   Complexity: LOW
#   Method: Format the output as a dictionary or JSON object that can be easily parsed
#           and used by subsequent nodes in the workflow.
# -- END PRD --

import json
import re


def assess_interpretation_impact(interpretations: str, workflow_objectives: str) -> str:
    """
    Evaluates the potential impact of different interpretations of 'world' on the workflow objectives.

    Args:
        interpretations: Input parameter of type str
workflow_objectives: Input parameter of type str

    Returns:
        str: Output of type dict
    """
    
    # Parse interpretations and objectives
    try:
        # Split interpretations by common delimiters if it's a delimited string
        if '|' in interpretations:
            interpretation_list = [interp.strip() for interp in interpretations.split('|')]
        elif ';' in interpretations:
            interpretation_list = [interp.strip() for interp in interpretations.split(';')]
        elif '\n' in interpretations:
            interpretation_list = [interp.strip() for interp in interpretations.split('\n')]
        else:
            interpretation_list = [interpretations.strip()]
        
        # Split objectives similarly
        if '|' in workflow_objectives:
            objective_list = [obj.strip() for obj in workflow_objectives.split('|')]
        elif ';' in workflow_objectives:
            objective_list = [obj.strip() for obj in workflow_objectives.split(';')]
        elif '\n' in workflow_objectives:
            objective_list = [obj.strip() for obj in workflow_objectives.split('\n')]
        else:
            objective_list = [workflow_objectives.strip()]
            
    except Exception:
        interpretation_list = [interpretations]
        objective_list = [workflow_objectives]
    
    # Simple keyword-based impact scoring
    impact_results = []
    
    for i, interpretation in enumerate(interpretation_list):
        interpretation_lower = interpretation.lower()
        impact_score = 0.0
        relevance_matches = []
        
        # Calculate impact based on keyword overlap and semantic similarity
        for objective in objective_list:
            objective_lower = objective.lower()
            
            # Extract keywords (simple approach)
            interp_words = set(re.findall(r'\b\w{3,}\b', interpretation_lower))
            obj_words = set(re.findall(r'\b\w{3,}\b', objective_lower))
            
            # Calculate overlap score
            if obj_words:
                overlap = len(interp_words.intersection(obj_words))
                overlap_score = overlap / len(obj_words)
                impact_score += overlap_score
                
                if overlap > 0:
                    relevance_matches.append({
                        'objective': objective,
                        'overlap_words': list(interp_words.intersection(obj_words)),
                        'overlap_score': overlap_score
                    })
        
        # Normalize impact score
        if objective_list:
            impact_score = impact_score / len(objective_list)
        
        # Determine impact level
        if impact_score >= 0.7:
            impact_level = 'HIGH'
        elif impact_score >= 0.4:
            impact_level = 'MEDIUM'
        elif impact_score >= 0.1:
            impact_level = 'LOW'
        else:
            impact_level = 'MINIMAL'
        
        impact_results.append({
            'interpretation': interpretation,
            'impact_score': round(impact_score, 3),
            'impact_level': impact_level,
            'relevance_matches': relevance_matches,
            'rank': i + 1
        })
    
    # Sort by impact score (highest first)
    impact_results.sort(key=lambda x: x['impact_score'], reverse=True)
    
    # Update ranks after sorting
    for i, result in enumerate(impact_results):
        result['rank'] = i + 1
    
    # Create summary
    summary = {
        'total_interpretations': len(interpretation_list),
        'highest_impact': impact_results[0] if impact_results else None,
        'average_impact_score': round(sum(r['impact_score'] for r in impact_results) / len(impact_results), 3) if impact_results else 0.0
    }
    
    # Create final output dictionary
    output = {
        'impact_analysis': impact_results,
        'summary': summary,
        'recommendations': {
            'top_interpretation': impact_results[0]['interpretation'] if impact_results else None,
            'reasoning': f"Selected based on highest impact score of {impact_results[0]['impact_score']}" if impact_results else "No interpretations provided"
        }
    }
    
    # Return as JSON string since return type is str
    return json.dumps(output, indent=2)