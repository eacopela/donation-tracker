const { chromium } = require('playwright');
const fs = require('fs').promises;
const path = require('path');

async function scrapeDonations() {
    const browser = await chromium.launch({
        args: ['--no-sandbox']
    });
    try {
        // Get current time in Eastern Time
        const now = new Date();
        const etTime = new Date(now.toLocaleString('en-US', { timeZone: 'America/New_York' }));

        const donations = {
            fallenPatriots: 0,
            youtube: 0,
            total: 0,
            lastUpdated: etTime.toISOString()
        };

        // Scrape Fallen Patriots
        const fallenPatriotsPage = await browser.newPage();
        await fallenPatriotsPage.goto('https://donate.fallenpatriots.org/campaign/2025-chaotic-good/c660862', {
            waitUntil: 'networkidle'
        });
        const fallenPatriotsAmount = await fallenPatriotsPage.locator('.sc-campaign-progress_raised').textContent();
        donations.fallenPatriots = parseFloat(fallenPatriotsAmount.replace(/[$,]/g, ''));

        // Scrape YouTube
        const youtubePage = await browser.newPage();
        await youtubePage.goto('https://www.youtube.com/live/HFtyL3RedQE?si=YeC4zridcQeN-IRC', {
            waitUntil: 'networkidle'
        });
        const youtubeAmount = await youtubePage.locator('#amount-raised > yt-formatted-string').textContent();
        donations.youtube = parseFloat(youtubeAmount.replace(/[$,]/g, ''));

        donations.total = donations.fallenPatriots + donations.youtube;

        // Ensure data directory exists
        const dataDir = path.join(__dirname, 'data');
        await fs.mkdir(dataDir, { recursive: true });

        // Write to JSON file
        await fs.writeFile(
            path.join(dataDir, 'donations.json'),
            JSON.stringify(donations, null, 2)
        );

        console.log('Successfully updated donation data:', donations);
    } catch (error) {
        console.error('Error scraping donations:', error);
        throw error;
    } finally {
        await browser.close();
    }
}

scrapeDonations();
