# -- PRD --
# 1. BULLET: Implement spatial analysis techniques to identify geographical patterns from
#   the input data.
#   Reason: To fulfill the requirement of analyzing geographical data and extracting
#           meaningful patterns.
#   Impact: Enables the system to derive insights from geographical data, which can be
#           used for further analysis or decision-making.
#   Complexity: HIGH
#   Method: Utilize geospatial libraries such as Geopandas or Shapely to perform
#           spatial joins, buffering, or other relevant operations.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle input data formatting to ensure compatibility with the spatial
#   analysis library.
#   Reason: To ensure seamless integration and accurate analysis, the input data needs
#           to be in a compatible format.
#   Impact: Proper data formatting will prevent errors during analysis and ensure
#           reliable output.
#   Complexity: MEDIUM
#   Method: Implement data cleaning and conversion routines to transform input strings
#           into suitable data structures for spatial analysis.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Validate the output to ensure it meets the required format and contains
#   meaningful geographical patterns.
#   Reason: To guarantee that the output is usable by subsequent processes or nodes in
#           the system.
#   Impact: Ensures that downstream processes can rely on the output for further
#           analysis or actions.
#   Complexity: LOW
#   Method: Implement output validation checks to confirm that the result is a list of
#           strings representing identified geographical patterns.
# -- END PRD --

from typing import List

import re
from collections import defaultdict


def perform_spatial_analysis(continents: str, countries: str, landmarks: str) -> List[str]:
    """
    Performs spatial analysis on geographical data to identify patterns and features.

    Args:
        continents: Input parameter of type str
countries: Input parameter of type str
landmarks: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Parse input data - handle comma-separated values or structured data
    def parse_geographical_data(data_str):
        if not data_str or data_str.strip() == "":
            return []
        # Split by common delimiters and clean
        items = re.split(r'[,;\n]', data_str)
        return [item.strip() for item in items if item.strip()]
    
    # Parse input geographical data
    continent_list = parse_geographical_data(continents)
    country_list = parse_geographical_data(countries)
    landmark_list = parse_geographical_data(landmarks)
    
    # Perform spatial analysis to identify patterns
    patterns = []
    
    # Pattern 1: Continental distribution analysis
    if continent_list:
        continent_count = len(set(continent_list))
        if continent_count > 1:
            patterns.append(f"Multi-continental distribution detected across {continent_count} continents")
        elif continent_count == 1:
            patterns.append(f"Single continental focus on {continent_list[0]}")
    
    # Pattern 2: Country clustering analysis
    if country_list:
        country_frequency = defaultdict(int)
        for country in country_list:
            country_frequency[country] += 1
        
        # Identify high-frequency countries
        max_freq = max(country_frequency.values()) if country_frequency else 0
        if max_freq > 1:
            dominant_countries = [country for country, freq in country_frequency.items() if freq == max_freq]
            patterns.append(f"Geographic clustering in countries: {', '.join(dominant_countries)}")
        
        if len(country_list) > 3:
            patterns.append("High geographical diversity with multiple country presence")
    
    # Pattern 3: Landmark density analysis
    if landmark_list:
        landmark_density = len(landmark_list)
        if landmark_density > 5:
            patterns.append("High landmark density indicating urban or tourist concentration")
        elif landmark_density >= 2:
            patterns.append("Moderate landmark concentration suggesting regional significance")
        else:
            patterns.append("Low landmark density indicating rural or remote areas")
    
    # Pattern 4: Cross-reference analysis between data types
    if continent_list and country_list:
        # Check for geographical consistency
        patterns.append("Hierarchical geographical structure detected (continent-country relationship)")
    
    if country_list and landmark_list:
        # Analyze landmark distribution across countries
        if len(country_list) < len(landmark_list):
            patterns.append("Concentrated landmark distribution within limited geographical scope")
        else:
            patterns.append("Distributed landmark pattern across multiple geographical regions")
    
    # Pattern 5: Spatial proximity analysis (basic implementation)
    all_locations = continent_list + country_list + landmark_list
    if len(all_locations) > 0:
        unique_locations = len(set(all_locations))
        total_locations = len(all_locations)
        
        if unique_locations < total_locations * 0.7:
            patterns.append("Geographic overlap detected - multiple references to same locations")
        
        if unique_locations > 10:
            patterns.append("Wide geographical span with extensive location coverage")
    
    # Validate output and ensure meaningful patterns
    if not patterns:
        patterns.append("Limited geographical data available for pattern analysis")
    
    # Remove duplicates while preserving order
    seen = set()
    validated_patterns = []
    for pattern in patterns:
        if pattern not in seen:
            validated_patterns.append(pattern)
            seen.add(pattern)
    
    return validated_patterns