# Elm Wealth Coin Flip Game Bot

An automated bot for playing the Elm Wealth coin flip game using Selenium WebDriver. This project includes both GUI and headless versions of the bot, along with data visualization tools.

## Overview

This project automates gameplay on the Elm Wealth coin flip game website (https://elmwealth.com/coin-flip/). The bot automatically:
- Selects "heads" for each coin flip
- Bets 20% of current balance
- Continues playing until the game timer runs low
- Records gameplay data and takes screenshots

## Files

- `gameCode.py` - Main bot with GUI Chrome browser
- `gameCodeHeadless.py` - Headless version of the bot (runs in background)
- `randomWalk_Visualizer.py` - Visualizes the gameplay data as a graph
- `CoinFlipGameData.txt` - Game data file containing balance values and timestamps
- `screenshot_*.png` - Screenshots taken at the end of gameplay sessions

## Requirements

```
selenium
matplotlib
```

Install dependencies:
```bash
pip install selenium matplotlib
```

You'll also need Chrome WebDriver installed and accessible in your PATH.

## Usage

### Running the Bot

**With GUI (visible browser):**
```bash
python gameCode.py
```

**Headless mode (background):**
```bash
python gameCodeHeadless.py
```

### Visualizing Results

After running the bot, visualize the balance progression:
```bash
python randomWalk_Visualizer.py
```

## How It Works

1. Opens the Elm Wealth coin flip game website
2. Waits for the game to load and starts a new game
3. Continuously:
   - Selects "heads" 
   - Bets 20% of current balance
   - Waits for game overlay to disappear
   - Records balance and timestamp
4. Stops when game timer reaches 4 seconds remaining
5. Takes a final screenshot
6. Saves all data to `CoinFlipGameData.txt`

## Data Format

The `CoinFlipGameData.txt` file contains alternating lines of:
- Balance amount (float)
- Remaining time (MM:SS format)

## Safety Features

- Stops automatically when timer gets low (4 seconds remaining)
- Takes screenshots for verification
- Uses explicit waits to handle page loading

## Disclaimer

This bot is for educational purposes only. Use responsibly and in accordance with the website's terms of service.
