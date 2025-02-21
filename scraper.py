from playwright.async_api import async_playwright
import json
from datetime import datetime
import os
import pytz  # Using pytz instead of zoneinfo for better Windows support
import asyncio
import time

async def scrape_fallen_patriots(browser):
    start_time = time.time()
    print("Navigating to Fallen Patriots page...")
    page = await browser.new_page()
    amount = 0
    
    try:
        await page.goto("https://donate.fallenpatriots.org/campaign/2025-chaotic-good/c660862")
        # More specific selector targeting the amount directly
        selector = '[class*="progress_raised"][class*="ng-binding"]'
        
        try:
            print(f"Waiting for selector: {selector}")
            # Reduce timeout and add state option for faster response
            await page.wait_for_selector(selector, timeout=15000, state='attached')
            # Use evaluate for faster direct access
            amount_text = await page.evaluate(f'''
                () => {{
                    const el = document.querySelector('{selector}');
                    return el ? el.textContent.trim() : null;
                }}
            ''')
            
            if amount_text:
                print(f"Found amount: {amount_text}")
                amount_str = ''.join(c for c in amount_text if c.isdigit() or c == '.')
                amount = float(amount_str)
            else:
                print("Could not find element after waiting")
        except Exception as e:
            print(f"Error finding element: {str(e)}")
    finally:
        await page.close()
        print(f"Fallen Patriots scraping took {time.time() - start_time:.2f} seconds")
    
    return amount

async def scrape_youtube(browser):
    start_time = time.time()
    print("Navigating to YouTube page...")
    page = await browser.new_page()
    amount = 0
    
    try:
        youtube_url = "https://www.youtube.com/live/B1UEoOK0Psc?si=Cigp_PVGoHf1ibCG"
        await page.goto(youtube_url)
        
        print("Waiting for YouTube amount element...")
        
        # Wait for any donation shelf content to load
        base_selector = 'ytd-donation-shelf-renderer'
        await page.wait_for_selector(base_selector, timeout=15000, state='attached')
        
        # Use JavaScript to find the amount, being more specific about the text pattern
        amount_text = await page.evaluate('''
            () => {
                const shelf = document.querySelector('ytd-donation-shelf-renderer');
                if (!shelf) return null;
                
                // Find any text that matches currency pattern
                const walker = document.createTreeWalker(
                    shelf,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                
                let node;
                let bestMatch = null;
                
                while (node = walker.nextNode()) {
                    const text = node.textContent.trim();
                    // Specifically look for text containing "Total raised" and a dollar amount
                    if (text.toLowerCase().includes('total raised')) {
                        console.log('Found text:', text);
                        const match = text.match(/\\$[\\d,]+(\\.[\\d]{2})?/);
                        if (match) {
                            bestMatch = match[0];
                            // If we found "Total raised" text with amount, prioritize this
                            break;
                        }
                    }
                }
                
                return bestMatch;
            }
        ''')
        
        if amount_text:
            print(f"Found YouTube amount: {amount_text}")
            amount_str = ''.join(c for c in amount_text if c.isdigit() or c == '.')
            if amount_str:
                amount = float(amount_str)
        else:
            print("Could not find YouTube amount")
    finally:
        await page.close()
        print(f"YouTube scraping took {time.time() - start_time:.2f} seconds")
    
    return amount

async def scrape_donations():
    total_start_time = time.time()
    async with async_playwright() as p:
        # Launch browser with specific options for GitHub Actions
        browser = await p.chromium.launch(
            args=['--no-sandbox', '--disable-setuid-sandbox'],
            headless=True
        )
        
        try:
            # Scrape both sites in parallel
            fallen_patriots_amount, youtube_amount = await asyncio.gather(
                scrape_fallen_patriots(browser),
                scrape_youtube(browser)
            )
            
            # Prepare donation data
            donations = {
                "fallenPatriots": fallen_patriots_amount,
                "youtube": youtube_amount,
                "total": fallen_patriots_amount + youtube_amount,
                "lastUpdated": datetime.now(pytz.timezone('US/Eastern')).isoformat()
            }
            
            # Save to file
            os.makedirs("data", exist_ok=True)
            with open('data/donations.json', 'w') as f:
                json.dump(donations, f, indent=2)
                
            print(f"Updated donations: {donations}")
            print(f"Total scraping time: {time.time() - total_start_time:.2f} seconds")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_donations())
