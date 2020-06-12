# Karnataka COVID19 Stats - Telegram Bot

This repository contains the Python (v3.7) code for the 

## Using the bot
1. Search for the bot in Telegram using either **Karnataka COVID19 Stats** or **@karcovidbot**
2. Click **START** to begin conversing with the bot
3. To retrieve the latest COVID 19 stats for Karnataka, send either **/karcovid** or **/karcorona**

## Creating a local setup
1. Clone the current repository - `git clone https://github.com/AbhishekPednekar84/covid19-kar-bot`
2. Create a virtual environment - `python -m venv venv`
3. Activate the virtual environment - `venv\Sctipts\activate.bar` (Windows), `source venv/bin/activate` (OSx / Linux)
4. Install the project dependencies - `pip install -r requirements.txt`
5. Create a `.env` file and add an environment variable called `TELEGRAM_TOKEN` (refer to `.env.example`)
6. Run the code - `python bot/server.py` or `python3 bot/server.py`
