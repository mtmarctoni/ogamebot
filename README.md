# OGameBot

A sophisticated Python-based automation bot for the browser game OGame. This bot uses Playwright to interact with the game interface, simulating human behavior to manage your empire, perform upgrades, and monitor for attacks.

## 🚀 Features

- **Automated Login**: Handles login via the OGame Lobby (supports Facebook login).
- **Empire Management**: Automatically gathers data from all planets in your empire.
- **Smart Upgrades**:
  - **Resources**: Upgrades Metal, Crystal, and Deuterium mines.
  - **Energy**: Manages Solar Plants and Fusion Reactors.
  - **Storage**: Automatically upgrades storage when capacity is near full.
  - **Research**: Prioritized research upgrades based on configuration.
  - **Lifeforms**: Manages Lifeform buildings with customizable priority.
- **Attack Detection**: Monitors the overview page for incoming attacks and sends alerts.
- **Notifications**: Integrated Telegram notifications for status updates, upgrades, and alerts.
- **Human-like Behavior**: Implements randomized sleep intervals and "night mode" to avoid detection.
- **Resilience**: Automatic restart mechanism for handling browser errors or connection issues.
- **State Tracking**: Saves empire snapshots to JSON for analysis and debugging.

## 🛠️ Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd ogamebot
    ```

2.  **Set up a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    playwright install
    ```

4.  **Configuration:**
    - Edit `config/config.py` to set your server ID, language, and upgrade priorities.
    - Edit `config/telegram_config.py` (create if missing) to add your Telegram Bot Token and Chat ID.

## ▶️ Usage

Run the bot using the main script:

```bash
python main.py
```

**First Run:**
On the first run, the bot may ask you to log in manually to the OGame Lobby to establish a session. Once logged in, press Enter in the terminal to save the session cookies (`fb_session.json`). Subsequent runs will use this session for auto-login.

## 📂 Project Structure

```
ogamebot/
├── main.py                 # Entry point of the application
├── config/                 # Configuration files
│   ├── config.py           # General settings (server, priorities, sleep times)
│   ├── telegram_config.py  # Telegram credentials
│   └── types.py            # Type definitions
├── constants/              # Game constants (IDs, names, requirements)
├── core/                   # Core application logic
│   ├── auth/               # Session and login management
│   ├── data/               # Data persistence (snapshots)
│   ├── info/               # Parsing empire data
│   ├── navigation/         # Navigation logic (universe, planets)
│   ├── notifications/      # Telegram notifier implementation
│   ├── start/              # Main loop and session orchestration
│   ├── upgrade/            # Upgrade logic (buildings, research, etc.)
│   └── utils/              # Utilities (sleep, attack detection)
├── database/               # JSON snapshots of empire state
└── requirements.txt        # Python dependencies
```

## ⚙️ Configuration

Key settings in `config/config.py`:

- `SERVER_ID`, `LANG`: Target OGame server.
- `PLANET_IDS`: Dictionary of your planet IDs (used for direct navigation).
- `RESEARCH_PRIORITY`: List of research technologies in order of priority.
- `HUMAN_LIFEFORM_BUILDING_PRIORITY`: Priority list for Lifeform buildings.
- `STORAGE_WARNING_THRESHOLD`: Percentage full to trigger a warning.
- `STORAGE_UPGRADE_THRESHOLD`: Percentage full to trigger an upgrade.

## 🤝 Contributing

1.  Fork the repository.
2.  Create a feature branch.
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

## ⚠️ Disclaimer

This bot is for educational purposes only. Using bots in OGame violates the Terms of Service and can lead to account bans. Use at your own risk.
