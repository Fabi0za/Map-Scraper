import json
import argparse
import random
import threading
import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from workbook import create_workbook, write_data_row
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# Constants and settings
SETTINGS = {
    'SEARCH_BOX_CLASS': 'searchboxinput',
    'SEARCH_BUTTON_CLASS': 'searchbox-searchbutton',
    'BOX_CLASS': 'Nv2PK',
    'LINK_CLASS': 'hfpxzc',
    'NAME_CLASS': 'qBF1Pd',
    'ADDRESS_CLASS': 'W4Efsd',
    'RATING_CLASS': 'MW4etd',
    'REVIEW_COUNT_CLASS': 'UY7F9',
    'PHONE_CLASS': 'UsdlK',
    'WEBSITE_CLASS': 'lcr4fd',
    
    # Review-specific classes
    'REVIEW_TAB_CLASS': 'hh2c6',
    'REVIEW_CONTAINER_CLASS': 'jftiEf',
    'REVIEWER_NAME_CLASS': 'd4r55',
    'REVIEW_TEXT_CLASS': 'wiI7pd',
    'REVIEW_DATE_CLASS': 'rsqaWe',
    'REVIEW_RATING_CONTAINER_CLASS': 'kvMYJc',
    'REVIEW_STAR_CLASS': 'hCCjke'
}

def extract_reviews(driver, verbose=False):
    """Extract all reviews for a business"""
    reviews = []
    try:
        # Find and click the Reviews tab
        review_tabs = driver.find_elements(By.CSS_SELECTOR, "button[role='tab']")
        review_tab_clicked = False
        
        for tab in review_tabs:
            if 'Reviews' in tab.text:
                driver.execute_script("arguments[0].click();", tab)
                time.sleep(1)  # Reduced wait time
                review_tab_clicked = True
                break
        
        if not review_tab_clicked:
            if verbose:
                print("No reviews tab found")
            return reviews
        
        # Wait for reviews to be visible - reduced timeout
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, SETTINGS['REVIEW_CONTAINER_CLASS']))
            )
        except:
            if verbose:
                print("No reviews found")
            return reviews
        
        # Extract reviews - limit to first 3 reviews to speed things up
        review_elements = driver.find_elements(By.CLASS_NAME, SETTINGS['REVIEW_CONTAINER_CLASS'])[:3]
        
        for review in review_elements:
            try:
                # Check for and click "More" button if present
                more_buttons = review.find_elements(By.CSS_SELECTOR, "button.w8nwRe.kyuRq")
                if more_buttons:
                    try:
                        driver.execute_script("arguments[0].click();", more_buttons[0])
                        time.sleep(0.3)  # Reduced wait time
                    except:
                        pass  # Continue even if clicking fails
                
                # Get review text and date
                try:
                    text = review.find_element(By.CLASS_NAME, SETTINGS['REVIEW_TEXT_CLASS']).text
                except:
                    text = ""
                
                try:
                    date = review.find_element(By.CLASS_NAME, SETTINGS['REVIEW_DATE_CLASS']).text
                except:
                    date = ""
                
                # Get rating
                try:
                    rating_container = review.find_element(By.CLASS_NAME, SETTINGS['REVIEW_RATING_CONTAINER_CLASS'])
                    rating = int(rating_container.get_attribute('aria-label').split()[0])
                except:
                    rating = 0
                
                # Skip extracting points and services to save time
                reviews.append({
                    'text': text,
                    'date': date,
                    'rating': rating,
                    'positive_points': [],
                    'negative_points': [],
                    'services': []
                })
                
            except Exception as e:
                if verbose:
                    print(f"Error extracting individual review: {str(e)}")
                continue
                
    except Exception as e:
        if verbose:
            print(f"Error in review extraction: {str(e)}")
    
    # Click back to the main info tab to ensure we're ready to navigate back
    try:
        info_tabs = driver.find_elements(By.CSS_SELECTOR, "button[role='tab']")
        for tab in info_tabs:
            if 'About' in tab.text or 'Overview' in tab.text:
                driver.execute_script("arguments[0].click();", tab)
                time.sleep(0.5)  # Reduced wait time
                break
    except:
        pass
    
    return reviews

def handle_consent_popup(driver, verbose=False):
    """Handle the Google consent popup if it appears"""
    try:
        # Look for the consent button using various selectors
        consent_button = None
        selectors = [
            "button[aria-label='Accept all']",  # English version
            "button[aria-label='Tout accepter']",  # French version
            "button[aria-label='Alle akzeptieren']",  # German version
            "button[jsname='tWT92d']",  # Generic selector
            "button.tHlp8d"  # Class-based selector
        ]
        
        for selector in selectors:
            try:
                consent_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                if consent_button:
                    break
            except:
                continue
        
        if consent_button:
            if verbose:
                print("Found consent popup, clicking 'Accept all'")
            driver.execute_script("arguments[0].click();", consent_button)
            time.sleep(2)  # Wait for popup to close
            return True
    except Exception as e:
        if verbose:
            print(f"Error handling consent popup: {str(e)}")
    return False

def extract_data_from_card(card, driver, args, verbose=False):
    """Extract business data directly from the search results card"""
    data = {}
    original_window = driver.current_window_handle
    new_tab_opened = False
    
    try:
        # Get business name
        try:
            name_element = card.find_element(By.CSS_SELECTOR, ".qBF1Pd")
            data['name'] = name_element.text.strip()
        except:
            data['name'] = ''
            
        # Get rating and review count
        try:
            rating_element = card.find_element(By.CLASS_NAME, SETTINGS['RATING_CLASS'])
            data['rating'] = rating_element.text.strip()
            
            review_count_element = card.find_element(By.CLASS_NAME, SETTINGS['REVIEW_COUNT_CLASS'])
            data['review_count'] = review_count_element.text.strip('()')
        except:
            data['rating'] = ''
            data['review_count'] = ''
            
        # Get address from the card
        try:
            address_elements = card.find_elements(By.CSS_SELECTOR, ".W4Efsd > div:nth-child(1) > span")
            if address_elements:
                data['address'] = address_elements[0].text.strip()
            else:
                data['address'] = ''
        except:
            data['address'] = ''
            
        # Get phone and website - these usually require clicking into the business
        data['phone'] = ''
        data['website'] = ''
        data['reviews'] = []
        
        # If we need reviews or more detailed info, we'll need to click into the business
        if args.scrape_reviews or args.scrape_website:
            # Get the link to the business page
            try:
                link_element = card.find_element(By.CLASS_NAME, SETTINGS['LINK_CLASS'])
                link_href = link_element.get_attribute('href')
                
                # Store current window handle before opening new tab
                original_window = driver.current_window_handle
                
                # Open in a new tab
                driver.execute_script("window.open(arguments[0], '_blank');", link_href)
                new_tab_opened = True
                
                # Wait for new tab to open and switch to it - reduced timeout
                WebDriverWait(driver, 3).until(lambda d: len(d.window_handles) > 1)
                driver.switch_to.window(driver.window_handles[1])
                
                # Wait for the page to load - reduced timeout
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1.DUwDvf"))
                )
                
                # Get phone - reduced timeout
                try:
                    phone_element = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-item-id='phone:tel']"))
                    )
                    data['phone'] = phone_element.text.strip()
                except:
                    if verbose:
                        print(f"Could not find phone for {data['name']}")
                
                # Get website - reduced timeout
                try:
                    website_element = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-item-id='authority']"))
                    )
                    data['website'] = website_element.get_attribute('href')
                except:
                    if verbose:
                        print(f"Could not find website for {data['name']}")
