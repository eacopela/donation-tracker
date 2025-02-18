from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import os

def scrape_donations():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        donations = {
            "fallenPatriots": 0,
            "youtube": 0,
            "total": 0,
            "lastUpdated": datetime.now().isoformat()
        }
        
        try:
            # Scrape Fallen Patriots
            page = browser.new_page()
            page.goto("https://donate.fallenpatriots.org/campaign/2025-chaotic-good/c660862", wait_until="networkidle")
            fallen_patriots_amount = page.query_selector(".sc-campaign-progress_raised").text_content()
            donations["fallenPatriots"] = float(fallen_patriots_amount.replace("$", "").replace(",", ""))
            page.close()
            
            # Scrape YouTube
            page = browser.new_page()
            page.goto("https://www.youtube.com/live/1xhV_xJU9Z8", wait_until="networkidle")
            youtube_amount = page.query_selector("#amount-raised > yt-formatted-string").text_content()
            donations["youtube"] = float(youtube_amount.replace("$", "").replace(",", ""))
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
