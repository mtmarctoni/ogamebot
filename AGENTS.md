# AI Agent Context & Guidelines

This document provides context and instructions for AI agents working on the `ogamebot` codebase. It outlines the architecture, common tasks, and coding conventions to ensure consistency and reliability.

## 🧠 Architecture Overview

The bot operates on a **synchronous loop** using `Playwright` for browser automation.

1.  **Entry Point**: `main.py` initializes the `TelegramNotifier` and enters a restart loop.
2.  **Session Loop**: `core/start/run_bot_session.py` contains the main logic:
    - Loads/Saves session cookies (`core/auth`).
    - Navigates to the game.
    - **Main Loop**:
      - Checks for attacks (`core/utils/attack_detection`).
      - Scrapes Empire View (`core/info/empire`).
      - Saves state (`core/data`).
      - Executes upgrades (`core/upgrade/handle_upgrades`).
      - Sleeps for a calculated duration (`core/utils/sleep_utils`).

## 📂 Key Modules & Responsibilities

| Module         | Path               | Responsibility                                                                                                             |
| :------------- | :----------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **Config**     | `config/`          | Centralized configuration. `config.py` controls behavior, `types.py` defines data structures (TypedDicts).                 |
| **Constants**  | `constants/`       | Static game data (Building IDs, Research IDs, etc.). **Always use these constants** instead of hardcoded strings/IDs.      |
| **Auth**       | `core/auth/`       | `session_manager.py` handles `fb_session.json` and Playwright context creation.                                            |
| **Info**       | `core/info/`       | `empire.py` is critical. It parses the "Empire View" to get the current state of all planets (resources, building levels). |
| **Upgrade**    | `core/upgrade/`    | `handle_upgrades.py` orchestrates the upgrade process. Submodules (`buildings.py`, `research.py`) handle specific logic.   |
| **Navigation** | `core/navigation/` | Helpers to switch planets or views.                                                                                        |
| **Utils**      | `core/utils/`      | `sleep_utils.py` (human-like delays) and `attack_detection.py`.                                                            |

## 🛠️ Common Tasks & Instructions

### 1. Adding a New Upgrade Type

If you need to add a new type of upgrade (e.g., Shipyard queue):

1.  Create a new module in `core/upgrade/` (e.g., `ships.py`).
2.  Define a handler function (e.g., `handle_ship_production(planet, game_page, notifier)`).
3.  This function should:
    - Check resources/requirements.
    - Navigate to the correct page.
    - Interact with the DOM to start production.
    - Return the duration (seconds) until the next action is needed (or 0).
4.  Register the handler in `core/upgrade/handle_upgrades.py`.

### 2. Modifying Selectors

OGame updates may break CSS selectors.

- **Locate**: Check `core/info/empire.py` for scraping selectors or specific upgrade modules for interaction selectors.
- **Update**: Use Playwright's `page.locator()` or `page.query_selector()` with the new CSS/XPath.
- **Verify**: Ensure the selector is unique and robust.

### 3. Handling Errors

- **Do not crash**: The bot is designed to run 24/7.
- **Exceptions**: `run_bot_session.py` catches `PlaywrightTimeoutError` and generic `Exception`.
- **Restart**: If a critical error occurs, raise an exception to trigger the `main.py` restart logic.
- **Notify**: Use `notifier.send_message()` to alert the user of critical failures.

### 4. Working with Data

- **Empire Data**: The `empire_data` dictionary (defined in `config/types.py`) is the source of truth for the current loop.
- **Snapshots**: `database/` contains JSON dumps. Use these to debug parsing issues without running the bot.

## 📝 Coding Conventions

- **Type Hinting**: Use Python type hints (`typing`) for all function arguments and return values.
- **Imports**: Absolute imports are preferred (e.g., `from core.utils import ...`).
- **Logging**: Use `print()` for console logs and `notifier` for user alerts.
- **Playwright**:
  - Use `sync_playwright`.
  - Always pass the `game_page` object to functions that need to interact with the browser.
  - Use `timeout` parameters in `wait_for_selector` to prevent infinite hangs.
- **Constants**: Never hardcode game IDs (e.g., use `Research.PLASMA` instead of `122`).

## 🤖 Agent Workflow

When asked to implement a feature:

1.  **Analyze**: Identify which `core/` modules are involved.
2.  **Plan**: Determine if you need new constants, config settings, or logic.
3.  **Implement**: Write the code, ensuring you handle edge cases (e.g., not enough resources).
4.  **Verify**: Check if the changes integrate well with `handle_upgrades` and the main loop.
