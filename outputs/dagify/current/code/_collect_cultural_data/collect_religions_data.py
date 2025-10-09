# -- PRD --
# 1. BULLET: Implement data collection from various sources such as databases, APIs, or
#   files based on the provided world context and sources.
#   Reason: To gather accurate and relevant data about major religions in the defined
#           world context.
#   Impact: This will enable the system to provide a list of major religions, enhancing
#           the cultural data collection capability.
#   Complexity: MEDIUM
#   Method: Utilize existing data access libraries or APIs to fetch data from the
#           identified sources, and then process the data to extract the
#           required information.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle different data formats and structures from various sources, ensuring
#   consistency in the output.
#   Reason: To ensure that the collected data is processed uniformly and presented in a
#           standardized format.
#   Impact: This will improve the overall quality and reliability of the collected
#           data, making it more usable for further processing.
#   Complexity: HIGH
#   Method: Implement data normalization techniques and utilize data transformation
#           libraries to achieve consistency in the output.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Implement error handling and logging mechanisms to track any issues during
#   data collection.
#   Reason: To ensure that any problems encountered during data collection are properly
#           logged and addressed.
#   Impact: This will enhance the robustness and maintainability of the data collection
#           process.
#   Complexity: LOW
#   Method: Use try-except blocks to catch exceptions, and utilize logging libraries to
#           log errors and important events.
# -- END PRD --

from typing import List

import json
import logging
import requests
from pathlib import Path


def collect_religions_data(world_context: str, sources: str) -> List[str]:
    """
    A shim function that collects major religions data for a given world context.

    Args:
        world_context: Input parameter of type str
sources: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    religions_list = []
    
    try:
        # Parse sources to determine data collection strategy
        source_list = [s.strip() for s in sources.split(',')]
        
        for source in source_list:
            try:
                logger.info(f"Collecting data from source: {source}")
                
                # Handle API sources
                if source.startswith('http'):
                    try:
                        params = {'context': world_context, 'type': 'religions'}
                        response = requests.get(source, params=params, timeout=30)
                        response.raise_for_status()
                        data = response.json()
                        
                        # Normalize API response data
                        if isinstance(data, list):
                            religions_list.extend([str(item) for item in data])
                        elif isinstance(data, dict):
                            if 'religions' in data:
                                religions_list.extend([str(item) for item in data['religions']])
                            elif 'data' in data:
                                religions_list.extend([str(item) for item in data['data']])
                        
                        logger.info(f"Successfully collected {len(data) if isinstance(data, list) else len(data.get('religions', []))} religions from API")
                    
                    except requests.exceptions.RequestException as e:
                        logger.error(f"Failed to fetch data from API {source}: {e}")
                        continue
                
                # Handle file sources
                elif source.endswith(('.json', '.txt', '.csv')):
                    file_path = Path(source)
                    if file_path.exists():
                        try:
                            if source.endswith('.json'):
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    file_data = json.load(f)
                                    
                                # Normalize JSON file data
                                if isinstance(file_data, list):
                                    religions_list.extend([str(item) for item in file_data])
                                elif isinstance(file_data, dict):
                                    context_data = file_data.get(world_context, file_data.get('religions', []))
                                    if isinstance(context_data, list):
                                        religions_list.extend([str(item) for item in context_data])
                            
                            elif source.endswith('.txt'):
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    lines = f.readlines()
                                    religions_list.extend([line.strip() for line in lines if line.strip()])
                            
                            elif source.endswith('.csv'):
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    lines = f.readlines()
                                    for line in lines[1:]:  # Skip header
                                        parts = line.strip().split(',')
                                        if parts:
                                            religions_list.append(parts[0].strip())
                            
                            logger.info(f"Successfully collected data from file {source}")
                        
                        except (json.JSONDecodeError, IOError) as e:
                            logger.error(f"Failed to read file {source}: {e}")
                            continue
                    else:
                        logger.error(f"File not found: {source}")
                        continue
                
                # Handle database-like sources (simplified)
                elif source.startswith('db://'):
                    # Simulate database connection and query
                    logger.info(f"Database source {source} detected, using fallback data")
                    # In a real implementation, this would connect to actual database
                    fallback_religions = ['Christianity', 'Islam', 'Judaism', 'Buddhism', 'Hinduism']
                    religions_list.extend(fallback_religions)
                
                else:
                    logger.warning(f"Unknown source type: {source}")
                    
            except Exception as e:
                logger.error(f"Error processing source {source}: {e}")
                continue
        
        # Data normalization and deduplication
        normalized_religions = []
        seen = set()
        
        for religion in religions_list:
            # Normalize format: capitalize first letter, remove extra spaces
            normalized = ' '.join(religion.strip().split()).title()
            if normalized and normalized.lower() not in seen:
                normalized_religions.append(normalized)
                seen.add(normalized.lower())
        
        # Filter based on world context if specific context provided
        if world_context and world_context.lower() not in ['global', 'world', 'all']:
            # Simple context filtering - in real implementation this would be more sophisticated
            context_keywords = world_context.lower().split()
            filtered_religions = []
            for religion in normalized_religions:
                # Include major world religions by default, or those matching context
                if any(keyword in religion.lower() for keyword in context_keywords) or \
                   religion.lower() in ['christianity', 'islam', 'judaism', 'buddhism', 'hinduism', 'sikhism']:
                    filtered_religions.append(religion)
            normalized_religions = filtered_religions if filtered_religions else normalized_religions
        
        logger.info(f"Successfully collected {len(normalized_religions)} unique religions")
        return normalized_religions
    
    except Exception as e:
        logger.error(f"Critical error in collect_religions_data: {e}")
        # Return basic fallback data in case of complete failure
        return ['Christianity', 'Islam', 'Judaism', 'Buddhism', 'Hinduism']