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
            
            # Wait for the specific element and print page content for debugging
            print("Waiting for donation amount element...")
            page.wait_for_selector(".sc-campaign-progress_raised", timeout=30000)
            
            # Try multiple potential selectors
            amount_element = (
                page.query_selector(".sc-campaign-progress_raised") or 
                page.query_selector("[data-qa='progress-raised']") or
                page.query_selector(".campaign-progress_raised")
            )
            
            if amount_element:
                fallen_patriots_amount = amount_element.text_content()
                print(f"Found amount: {fallen_patriots_amount}")
                donations["fallenPatriots"] = float(fallen_patriots_amount.replace("$", "").replace(",", ""))
            else:
                print("Could not find donation amount element")
                # For debugging, let's print the page content
                print("Page content:", page.content())
            
            page.close()
            
            # Scrape YouTube
            page = browser.new_page()
            print("Navigating to YouTube page...")
            page.goto("https://www.youtube.com/live/1xhV_xJU9Z8")
            
            # Wait for the specific element
            print("Waiting for YouTube amount element...")
            page.wait_for_selector("#amount-raised", timeout=30000)
            
            amount_element = page.query_selector("#amount-raised > yt-formatted-string")
            if amount_element:
                youtube_amount = amount_element.text_content()
                print(f"Found YouTube amount: {youtube_amount}")
                donations["youtube"] = float(youtube_amount.replace("$", "").replace(",", ""))
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
