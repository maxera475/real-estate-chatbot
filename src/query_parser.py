import re
from typing import Dict, Any

def _normalize_price(value_str: str, unit: str) -> float:
    """Converts price string to a numeric value."""
    value = float(value_str)
    if unit == 'cr':
        return value * 1_00_00_000
    elif unit in ['lakh', 'l']:
        return value * 1_00_000
    return value

def parse_query(query: str) -> Dict[str, Any]:
    """
    Parses a natural language query to extract structured search filters.
    """
    filters = {}
    query_lower = query.lower()
    price_match = re.search(r'(?:under|below|max|upto|less than|for|in)?\s*₹?\s*([\d\.]+)\s*(cr|lakh|l)', query_lower)
    if price_match:
        value_group = price_match.group(1)
        unit_group = price_match.group(2)
        filters['max_price'] = _normalize_price(value_group, unit_group)

    bhk_match = re.search(r'(\d|one|two|three|four|five)\s*(bhk|bed\s*room)', query_lower)
    if bhk_match:
        bhk_map = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5"}
        bhk_num = bhk_map.get(bhk_match.group(1), bhk_match.group(1))
        filters['bhk'] = f"{bhk_num} BHK"

    city_match = re.search(r'\bin\s+(pune|mumbai)\b', query_lower)
    if city_match:
        filters['city'] = city_match.group(1).capitalize()

    if 'ready to move' in query_lower or 'ready possession' in query_lower:
        filters['status'] = 'READY_TO_MOVE'
    elif 'under construction' in query_lower:
        filters['status'] = 'UNDER_CONSTRUCTION'
        
    locality_match = re.search(r'\b(in|at|near)\s+([a-zA-Z\s,]+?)(?=\s+in\s+(pune|mumbai)|$|\s+under\s+₹)', query_lower)
    if locality_match:
        locality = locality_match.group(2).strip()
        if locality not in ['pune', 'mumbai'] and not locality.endswith(('cr', 'lakh', 'l')):
            filters['locality'] = locality.title()
            
    return filters