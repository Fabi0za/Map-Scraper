import logging
from typing import Optional
import sys

def setup_logger(verbose: bool = False) -> logging.Logger:
    """Setup and configure logger."""
    logger = logging.getLogger('map_scraper')
    
    # Set logging level
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    
    logger.addHandler(handler)
    return logger

def print_colored(text: str, color: str, file: Optional[str] = None) -> None:
    """Print colored text to console."""
    if file is None:
        file = sys.stdout
    print(f'{color}{text}\033[0m', file=file)

def parse_address(address: str) -> tuple:
    """Parse address string into components."""
    parts = address.split(',')
    
    if len(parts) < 2:
        raise ValueError('Invalid address format')
    
    street = parts[0].strip()
    location_parts = parts[-1].strip().split(' ')
    
    if len(location_parts) < 2:
        raise ValueError('Invalid postal code or city format')
    
    postal_code = location_parts[0]
    city = ' '.join(location_parts[1:])
    
    return street, postal_code, city

def clean_phone_number(phone: str) -> str:
    """Clean and format phone number."""
    # Remove all non-numeric characters except '+'
    cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
    
    # Ensure it starts with country code
    if not cleaned.startswith('+'):
        if cleaned.startswith('0'):
            cleaned = '+49' + cleaned[1:]
        else:
            cleaned = '+49' + cleaned
    
    return cleaned

def format_review_points(points: list) -> list:
    """Format review points for better readability."""
    if not points:
        return []
    
    formatted = []
    for point in points:
        # Remove any prefix indicators
        point = point.replace('👍 ', '')
        point = point.replace('👎 ', '')
        point = point.replace('✓ ', '')
        
        # Capitalize first letter
        if point:
            point = point[0].upper() + point[1:]
            formatted.append(point)
    
    return formatted

def validate_rating(rating: float) -> float:
    """Validate and normalize rating value."""
    try:
        rating_float = float(rating)
    except ValueError:
        raise ValueError('Rating must be a number')
    
    if not 0 <= rating_float <= 5:
        raise ValueError('Rating must be between 0 and 5')
    
    return round(rating_float, 1)

def truncate_text(text: str, max_length: int = 32000) -> str:
    """Truncate text to maximum length while preserving words."""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space != -1:
        truncated = truncated[:last_space]
    
    return truncated + '...'