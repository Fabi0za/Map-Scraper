from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import List, Optional
import sys
import time

from .scraper import GoogleMapsScraper
from .workbook import create_workbook
from .cliargs import parse_arguments
from .helpers import setup_logger, print_colored
from .const.colors import Colors

def setup_driver(headless: bool = False) -> webdriver.Chrome:
    """Setup and configure Chrome WebDriver."""
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    return webdriver.Chrome(options=options)

def main():
    """Main entry point for the scraper."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logger(args.verbose)
    
    try:
        # Initialize driver
        print_colored('Initializing Chrome WebDriver...', Colors.BLUE)
        driver = setup_driver(args.headless)
        
        # Create scraper instance
        scraper = GoogleMapsScraper(driver)
        
        # Build search query
        query = f'{args.location} {args.business_type}'
        print_colored(f'Searching for: {query}', Colors.BLUE)
        
        # Perform scraping
        businesses = scraper.scrape_businesses(query, args.max_results)
        
        if not businesses:
            print_colored('No businesses found!', Colors.RED)
            sys.exit(1)
            
        print_colored(f'Found {len(businesses)} businesses', Colors.GREEN)
        
        # Create Excel workbook
        if args.output:
            output_file = args.output
        else:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_file = f'businesses_{timestamp}.xlsx'
            
        print_colored(f'Creating Excel workbook: {output_file}', Colors.BLUE)
        create_workbook(businesses, output_file)
        
        print_colored('Scraping completed successfully!', Colors.GREEN)
        
    except Exception as e:
        print_colored(f'Error: {str(e)}', Colors.RED)
        sys.exit(1)
        
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == '__main__':
    main()