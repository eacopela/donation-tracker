from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import os

def scrape_donations():
    with sync_playwright() as p:
        # Launch browser with specific options for GitHub Actions
        browser = p.chromium.launch(
            args=['--no-sandbox', '--disable-setuid-sandbox'],
            headless=True
        )
        donations = {
            "fallenPatriots": 0,
            "youtube": 0,
            "total": 0,
            "lastUpdated": datetime.now().isoformat()
        }
        
        try:
            # Scrape Fallen Patriots
            page = browser.new_page()
            print("Navigating to Fallen Patriots page...")
            page.goto("https://donate.fallenpatriots.org/campaign/2025-chaotic-good/c660862")
            
            # Wait for and get the donation amount using exact class name
            print("Waiting for donation amount element...")
            # Try to find the element with the exact class combination
            selector = '[class="sc-campaign-progress_raised ng-binding"]'
            
            try:
                print(f"Waiting for selector: {selector}")
                # Wait longer for the element to appear
                page.wait_for_selector(selector, timeout=30000)
                amount_element = page.query_selector(selector)
                
                if amount_element:
                    fallen_patriots_amount = amount_element.text_content()
                    print(f"Found amount: {fallen_patriots_amount}")
                    # Remove any non-numeric characters except decimal point
                    amount_str = ''.join(c for c in fallen_patriots_amount if c.isdigit() or c == '.')
                    donations["fallenPatriots"] = float(amount_str)
                else:
                    print("Could not find element after waiting")
                    # Try evaluating JavaScript to find the element
                    amount_element = page.evaluate('''
                        () => {
                            const elements = document.getElementsByClassName('sc-campaign-progress_raised ng-binding');
                            return elements.length > 0 ? elements[0].textContent : null;
                        }
                    ''')
                    if amount_element:
                        print(f"Found amount via JavaScript: {amount_element}")
                        amount_str = ''.join(c for c in amount_element if c.isdigit() or c == '.')
                        donations["fallenPatriots"] = float(amount_str)
                    else:
                        print("Could not find element via JavaScript either")
                        print("Page content:", page.content())
            except Exception as e:
                print(f"Error finding element: {str(e)}")
                print("Trying alternative method...")
                # Try one last time with evaluate
                try:
                    amount_element = page.evaluate('''
                        () => {
                            const elements = Array.from(document.getElementsByClassName('sc-campaign-progress_raised'));
                            return elements.find(el => el.classList.contains('ng-binding'))?.textContent;
                        }
                    ''')
                    if amount_element:
                        print(f"Found amount via alternative JavaScript: {amount_element}")
                        amount_str = ''.join(c for c in amount_element if c.isdigit() or c == '.')
                        donations["fallenPatriots"] = float(amount_str)
                    else:
                        print("Could not find element via alternative method")
                except Exception as e2:
                    print(f"Error in alternative method: {str(e2)}")
            
            page.close()
            
            # Scrape YouTube
            page = browser.new_page()
            print("Navigating to YouTube page...")
            page.goto("https://www.youtube.com/live/1xhV_xJU9Z8")
            
            # Wait for and get the YouTube amount using XPath
            print("Waiting for YouTube amount element...")
            youtube_xpath = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[3]/ytd-donation-shelf-renderer/div[2]/div[2]"
            page.wait_for_selector(f"xpath={youtube_xpath}", timeout=30000)
            
            amount_element = page.query_selector(f"xpath={youtube_xpath}")
            if amount_element:
                youtube_amount = amount_element.text_content()
                print(f"Found YouTube amount: {youtube_amount}")
                # Remove any non-numeric characters except decimal point
                amount_str = ''.join(c for c in youtube_amount if c.isdigit() or c == '.')
                donations["youtube"] = float(amount_str)
            else:
                print("Could not find YouTube amount element")
                print("Page content:", page.content())
            
            page.close()
            
            donations["total"] = donations["fallenPatriots"] + donations["youtube"]
            
            # Save to file
            os.makedirs("data", exist_ok=True)
            with open("data/donations.json", "w") as f:
                json.dump(donations, f, indent=2)
                
            print("Successfully updated donation data:", donations)
            
        except Exception as e:
            print("Error scraping donations:", str(e))
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    scrape_donations()
