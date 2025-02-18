const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

async function scrapeDonations() {
    const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    try {
        const donations = {
            fallenPatriots: 0,
            youtube: 0,
            total: 0,
            lastUpdated: new Date().toISOString()
        };

        // Scrape Fallen Patriots
        const fallenPatriotsPage = await browser.newPage();
        await fallenPatriotsPage.goto('https://donate.fallenpatriots.org/campaign/2025-chaotic-good/c660862', {
            waitUntil: 'networkidle0'
        });
        const fallenPatriotsAmount = await fallenPatriotsPage.$eval('.sc-campaign-progress_raised', el => el.textContent);
        donations.fallenPatriots = parseFloat(fallenPatriotsAmount.replace(/[$,]/g, ''));

        // Scrape YouTube
        const youtubePage = await browser.newPage();
        await youtubePage.goto('https://www.youtube.com/live/1xhV_xJU9Z8?si=yZ7o0ckA-Bry-O3b', {
            waitUntil: 'networkidle0'
        });
        const youtubeAmount = await youtubePage.$eval('#amount-raised > yt-formatted-string', el => el.textContent);
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
