import argparse

def parse_arguments():
    """Parse command line arguments for the scraper."""
    parser = argparse.ArgumentParser(
        description='Scrape business information from Google Maps'
    )
    
    parser.add_argument(
        'location',
        help='Location to search in (e.g., "Ansbach")',
        type=str
    )
    
    parser.add_argument(
        'business_type',
        help='Type of business to search for (e.g., "electrician")',
        type=str
    )
    
    parser.add_argument(
        '--max-results',
        help='Maximum number of results to scrape (default: 20)',
        type=int,
        default=20
    )
    
    parser.add_argument(
        '--output',
        help='Output Excel file path (default: businesses_TIMESTAMP.xlsx)',
        type=str
    )
    
    parser.add_argument(
        '--headless',
        help='Run Chrome in headless mode',
        action='store_true'
    )
    
    parser.add_argument(
        '--verbose',
        help='Enable verbose logging',
        action='store_true'
    )
    
    return parser.parse_args()