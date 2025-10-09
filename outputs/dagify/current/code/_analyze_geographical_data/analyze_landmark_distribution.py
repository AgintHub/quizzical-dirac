# -- PRD --
# 1. BULLET: Parse input strings into usable data structures for analysis.
#   Reason: The input parameters are strings and need to be converted into lists for
#           processing.
#   Impact: Enables the analysis function to work with the input data.
#   Complexity: LOW
#   Method: Use JSON parsing or string manipulation to convert input strings into
#           lists.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement a distribution analysis algorithm to identify geographical
#   patterns.
#   Reason: The core functionality of the shim is to analyze landmark distribution.
#   Impact: Provides the necessary insights into how landmarks are distributed across
#           different geographical regions.
#   Complexity: MEDIUM
#   Method: Utilize statistical analysis or machine learning techniques to identify
#           patterns in landmark distribution.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Format the analysis results into a list of patterns or features as output.
#   Reason: The output needs to be in a specific format (List[str]) as per the output
#           structure.
#   Impact: Ensures that the output is compatible with the expected output structure.
#   Complexity: LOW
#   Method: Use string formatting to compile the analysis results into a list of
#           strings.
# -- END PRD --

from typing import List

import json
from collections import Counter


def analyze_landmark_distribution(landmarks: str, continents: str, countries: str) -> List[str]:
    """
    Analyzes the distribution of major landmarks across continents and countries to identify patterns.

    Args:
        landmarks: Input parameter of type str
continents: Input parameter of type str
countries: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Parse input strings into usable data structures
    try:
        # Try JSON parsing first
        landmarks_list = json.loads(landmarks) if landmarks.strip().startswith('[') else landmarks.split(',')
        continents_list = json.loads(continents) if continents.strip().startswith('[') else continents.split(',')
        countries_list = json.loads(countries) if countries.strip().startswith('[') else countries.split(',')
    except json.JSONDecodeError:
        # Fallback to string splitting
        landmarks_list = [item.strip() for item in landmarks.split(',')]
        continents_list = [item.strip() for item in continents.split(',')]
        countries_list = [item.strip() for item in countries.split(',')]
    
    # Clean the data
    landmarks_list = [landmark.strip() for landmark in landmarks_list if landmark.strip()]
    continents_list = [continent.strip() for continent in continents_list if continent.strip()]
    countries_list = [country.strip() for country in countries_list if country.strip()]
    
    patterns = []
    
    # Implement distribution analysis algorithm
    
    # 1. Analyze landmark count distribution
    total_landmarks = len(landmarks_list)
    total_countries = len(countries_list)
    total_continents = len(continents_list)
    
    if total_landmarks > 0 and total_countries > 0:
        avg_landmarks_per_country = total_landmarks / total_countries
        patterns.append(f"Average landmarks per country: {avg_landmarks_per_country:.2f}")
    
    if total_landmarks > 0 and total_continents > 0:
        avg_landmarks_per_continent = total_landmarks / total_continents
        patterns.append(f"Average landmarks per continent: {avg_landmarks_per_continent:.2f}")
    
    # 2. Analyze geographical concentration
    continent_counter = Counter(continents_list)
    country_counter = Counter(countries_list)
    
    # Identify most concentrated areas
    if continent_counter:
        most_common_continent = continent_counter.most_common(1)[0]
        patterns.append(f"Most landmark-rich continent: {most_common_continent[0]} ({most_common_continent[1]} landmarks)")
    
    if country_counter:
        most_common_country = country_counter.most_common(1)[0]
        patterns.append(f"Most landmark-rich country: {most_common_country[0]} ({most_common_country[1]} landmarks)")
    
    # 3. Analyze distribution evenness
    if len(continent_counter) > 1:
        continent_values = list(continent_counter.values())
        continent_std = (sum((x - sum(continent_values)/len(continent_values))**2 for x in continent_values) / len(continent_values))**0.5
        if continent_std < 1.0:
            patterns.append("Distribution pattern: Even distribution across continents")
        else:
            patterns.append("Distribution pattern: Uneven distribution across continents")
    
    if len(country_counter) > 1:
        country_values = list(country_counter.values())
        country_std = (sum((x - sum(country_values)/len(country_values))**2 for x in country_values) / len(country_values))**0.5
        if country_std < 1.0:
            patterns.append("Distribution pattern: Even distribution across countries")
        else:
            patterns.append("Distribution pattern: Uneven distribution across countries")
    
    # 4. Identify diversity patterns
    if total_continents > 0 and total_countries > 0:
        diversity_ratio = total_countries / total_continents
        if diversity_ratio > 3:
            patterns.append("Diversity pattern: High country diversity per continent")
        elif diversity_ratio > 1.5:
            patterns.append("Diversity pattern: Moderate country diversity per continent")
        else:
            patterns.append("Diversity pattern: Low country diversity per continent")
    
    # 5. Statistical summary
    patterns.append(f"Total landmarks analyzed: {total_landmarks}")
    patterns.append(f"Geographic scope: {total_continents} continents, {total_countries} countries")
    
    # Return formatted results
    return patterns if patterns else ["No significant distribution patterns identified"]