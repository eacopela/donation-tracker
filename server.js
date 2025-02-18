const express = require('express');
const puppeteer = require('puppeteer');
const cors = require('cors');

const app = express();
const port = 3001;

app.use(cors());

async function scrapeDonations() {
    const browser = await puppeteer.launch();
    try {
        const donations = {
            fallenPatriots: 0,
            youtube: 0,
            total: 0
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
        return donations;
    } catch (error) {
        console.error('Error scraping donations:', error);
        throw error;
    } finally {
        await browser.close();
    }
}

app.get('/api/donations', async (req, res) => {
    try {
        const donations = await scrapeDonations();
        res.json(donations);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch donations' });
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
