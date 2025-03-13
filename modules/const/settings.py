from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Review:
    text: str
    rating: float
    time_posted: str
    positive_points: Optional[List[str]] = None
    negative_points: Optional[List[str]] = None
    services_used: Optional[List[str]] = None

@dataclass
class Business:
    name: str
    street_address: str
    postal_code: str
    city: str
    phone: Optional[str]
    website: Optional[str]
    avg_rating: float
    num_ratings: int
    reviews: List[Review]

# CSS Selectors for Google Maps elements
SELECTORS = {
    # Search elements
    'search_box': 'input[name="q"]',
    'search_button': 'button[jsaction*="search"]',
    
    # Business list elements
    'business_list': '[role="feed"]',
    'business_cards': '[role="article"]',
    'end_of_list': '.section-loading-spinner',
    
    # Business details
    'name': '[jstcache*=""] .fontHeadlineSmall',
    'address': '[data-item-id*="address"]',
    'phone': '[data-item-id*="phone"]',
    'website': '[data-item-id*="authority"]',
    'rating': '[jstcache*=""] .fontDisplayLarge',
    'review_count': '[jstcache*=""] .fontBodyMedium span',
    
    # Review elements
    'reviews_tab': '[data-tab-index="1"]',
    'review_items': '.jftiEf',
    'review_text': '.wiI7pd',
    'review_rating': '.kvMYJc',
    'review_time': '.rsqaWe',
    'review_points': '.k8MTF',
    'review_services': '.k8MTF span:first-child'
}

# Basic scraper configuration
SCRAPER_CONFIG = {
    'scroll_delay': 1.5,  # Delay between scrolls in seconds
    'page_load_timeout': 30,  # Maximum time to wait for page load in seconds
    'max_retries': 3  # Maximum number of retry attempts for failed operations
}