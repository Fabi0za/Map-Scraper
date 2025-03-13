from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Optional
import time

from .const.settings import SELECTORS, SCRAPER_CONFIG, Business, Review

class GoogleMapsScraper:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, SCRAPER_CONFIG['page_load_timeout'])
    
    def search(self, query: str) -> None:
        """Search for businesses on Google Maps."""
        try:
            # Navigate to Google Maps
            self.driver.get('https://www.google.com/maps')
            
            # Handle cookie consent if present
            try:
                consent_button = self.driver.find_element(By.XPATH, '//button[contains(., "Accept all")]')
                consent_button.click()
            except NoSuchElementException:
                pass
            
            # Find and fill search box
            search_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS['search_box'])))
            search_box.clear()
            search_box.send_keys(query)
            
            # Click search button
            search_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS['search_button'])))
            search_button.click()
            
            # Wait for results to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS['business_list'])))
            
        except TimeoutException as e:
            raise Exception(f'Search operation timed out: {str(e)}')
        except Exception as e:
            raise Exception(f'Error during search: {str(e)}')
    
    def scroll_results(self, max_results: int) -> None:
        """Scroll through results until max_results is reached or end of list."""
        scrolled_items = 0
        last_height = 0
        
        while scrolled_items < max_results:
            # Scroll to bottom of results
            self.driver.execute_script(
                'document.querySelector(arguments[0]).scrollTop += 1000;', 
                SELECTORS['business_list']
            )
            
            # Wait for scroll
            time.sleep(SCRAPER_CONFIG['scroll_delay'])
            
            # Check if we've reached the end
            new_height = self.driver.execute_script(
                'return document.querySelector(arguments[0]).scrollHeight;',
                SELECTORS['business_list']
            )
            
            if new_height == last_height:
                break
                
            last_height = new_height
            scrolled_items = len(self.driver.find_elements(By.CSS_SELECTOR, SELECTORS['business_cards']))
    
    def extract_business_data(self, card_element) -> Business:
        """Extract business data from a card element."""
        try:
            # Extract basic info
            name = card_element.find_element(By.CSS_SELECTOR, SELECTORS['name']).text
            address_elem = card_element.find_element(By.CSS_SELECTOR, SELECTORS['address'])
            full_address = address_elem.text.split(',')
            
            # Parse address
            street_address = full_address[0].strip()
            postal_and_city = full_address[-1].strip().split(' ')
            postal_code = postal_and_city[0]
            city = ' '.join(postal_and_city[1:])
            
            # Get optional fields
            try:
                phone = card_element.find_element(By.CSS_SELECTOR, SELECTORS['phone']).text
            except NoSuchElementException:
                phone = None
                
            try:
                website = card_element.find_element(By.CSS_SELECTOR, SELECTORS['website']).get_attribute('href')
            except NoSuchElementException:
                website = None
                
            # Get rating info
            rating = float(card_element.find_element(By.CSS_SELECTOR, SELECTORS['rating']).text)
            review_count_text = card_element.find_element(By.CSS_SELECTOR, SELECTORS['review_count']).text
            num_ratings = int(''.join(filter(str.isdigit, review_count_text)))
            
            return Business(
                name=name,
                street_address=street_address,
                postal_code=postal_code,
                city=city,
                phone=phone,
                website=website,
                avg_rating=rating,
                num_ratings=num_ratings,
                reviews=[]
            )
            
        except Exception as e:
            raise Exception(f'Error extracting business data: {str(e)}')
    
    def get_reviews(self, business_card) -> List[Review]:
        """Get reviews for a business."""
        reviews = []
        try:
            # Click reviews tab
            reviews_tab = business_card.find_element(By.CSS_SELECTOR, SELECTORS['reviews_tab'])
            reviews_tab.click()
            
            # Wait for reviews to load
            time.sleep(1)
            
            # Extract reviews
            review_elements = business_card.find_elements(By.CSS_SELECTOR, SELECTORS['review_items'])
            
            for review_elem in review_elements:
                text = review_elem.find_element(By.CSS_SELECTOR, SELECTORS['review_text']).text
                rating = float(review_elem.find_element(By.CSS_SELECTOR, SELECTORS['review_rating']).get_attribute('aria-label').split()[0])
                time_posted = review_elem.find_element(By.CSS_SELECTOR, SELECTORS['review_time']).text
                
                # Get optional points
                try:
                    points_elem = review_elem.find_element(By.CSS_SELECTOR, SELECTORS['review_points'])
                    points_text = points_elem.text.split('\n')
                    positive_points = [p for p in points_text if 'Positive' in p]
                    negative_points = [p for p in points_text if 'Negative' in p]
                    services = review_elem.find_elements(By.CSS_SELECTOR, SELECTORS['review_services'])
                    services_used = [s.text for s in services]
                except NoSuchElementException:
                    positive_points = None
                    negative_points = None
                    services_used = None
                
                reviews.append(Review(
                    text=text,
                    rating=rating,
                    time_posted=time_posted,
                    positive_points=positive_points,
                    negative_points=negative_points,
                    services_used=services_used
                ))
                
        except Exception as e:
            print(f'Error getting reviews: {str(e)}')
            
        return reviews
    
    def scrape_businesses(self, query: str, max_results: int = 20) -> List[Business]:
        """Main method to scrape businesses."""
        businesses = []
        retry_count = 0
        
        while retry_count < SCRAPER_CONFIG['max_retries']:
            try:
                # Perform search
                self.search(query)
                
                # Scroll to load desired number of results
                self.scroll_results(max_results)
                
                # Get all business cards
                cards = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS['business_cards'])
                
                # Process each business
                for card in cards[:max_results]:
                    business = self.extract_business_data(card)
                    business.reviews = self.get_reviews(card)
                    businesses.append(business)
                    
                break  # Success, exit retry loop
                
            except Exception as e:
                retry_count += 1
                if retry_count >= SCRAPER_CONFIG['max_retries']:
                    raise Exception(f'Failed to scrape after {retry_count} retries: {str(e)}')
                print(f'Retry {retry_count}: {str(e)}')
                time.sleep(1)
                
        return businesses