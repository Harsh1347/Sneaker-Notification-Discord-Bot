# Premium Sneakers Discord Bot

A Python-based Discord bot designed to monitor and track new and restock updates of premium sneakers from various websites. The bot scrapes data and sends real-time notifications to a Discord channel, providing timely updates to sneaker enthusiasts. This project was developed as part of a freelance project for a client.

## Monitored Websites
- ADIDAS
- AJIO
- MYNTRA
- NIKE
- SUPERKICKS
- VEGNONVEG

## Results
- Contributed to generating $300K for a client by creating a Discord bot for a community of 1,200+ members.
- Facilitated the sale of 1,000+ premium sneakers through real-time tracking and notifications across 6 websites.

## How It Works
1. The bot scrapes the listed websites for sneaker data such as name, sizes available, and cost.
2. Data is stored in a MongoDB database.
3. Every 120 seconds, the scraped data is compared with databaseto check for new or restocked sneakers.
4. Notifications are sent to a Discord channel using Discord webhooks.

## Technologies Used
- Python: Main programming language.
- BeautifulSoup & Selenium: For web scraping.
- MongoDB: Database for storing scraped data.
- Discord Webhook: For discord bot and sending notifications.
- Heroku: Deployment platform.