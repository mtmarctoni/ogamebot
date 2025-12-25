# main.py

import os
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright
from typing import cast, List

from config.types import EmpireSnapshotDict, PlanetDict
from config.config import LOBBY_URL, MAIN_PAGE_URL_TEMPLATE, DEFAULT_PLANET_ID
from core.session_manager import save_session, load_session
from core.navigation import enter_universe
from core.info_extractor import extract_empire_view
from core.snapshot_manager import save_empire_snapshot
from core.upgrade.auto_storage import upgrade_full_storages
from core.notifications.telegram_notifier import TelegramNotifier
from config.telegram_config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from core.utils.attack_detection import check_for_attack_alert
from core.utils.sleep_utils import sleep_random_interval


def main() -> None:
    notifier = None
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        notifier = TelegramNotifier(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, verbose=True)
        try:
            notifier.send_message("OGameBot is now ACTIVE.")
        except Exception as e:
            print(f"Failed to send startup notification: {e}")
    else:
        print("Telegram notifications are disabled (missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID).")
    
    with sync_playwright() as p:
        session_exists = os.path.exists("fb_session.json")
        browser, context = load_session(p)
        page = context.new_page()
        page.goto(LOBBY_URL)
        if not session_exists:
            print("No session found. Please log in with Facebook manually.")
            input("Press Enter after you have logged in and see the lobby...")
            save_session(context)
            print("Session saved.")
        else:
            print("Session found. Logging in automatically.")
        print("Navigating to main game...")
        game_page = enter_universe(page)
        # After entering, optionally go directly to overview using config
        try:
            url = MAIN_PAGE_URL_TEMPLATE.format(planet_id=DEFAULT_PLANET_ID)
            game_page.goto(url)
        except Exception:
            pass

        try:
            while True:
                print("Entered main game. Extracting basic info...")

                # --- Empire View Extraction ---
                print("\nNavigating to Empire View page and extracting all planet data...")
                # --- Attack detection (overview page) ---
                attack_info = check_for_attack_alert(game_page)
                if attack_info and notifier:
                    notifier.send_message(f"⚠️ ALERT: {attack_info}")

                # Continue with empire view extraction
                empire_url = "https://s271-en.ogame.gameforge.com/game/index.php?page=standalone&component=empire"
                game_page.goto(empire_url)
                html = game_page.content()
                empire_data = extract_empire_view(html)
                print("Empire View Planets:")
                for planet in empire_data['planets']:
                    print(f"- {planet['name']} (ID: {planet['id']}, Coords: {planet['coords']})")
                    print(f"    Resources: {planet['resources']}")
                    print(f"    Buildings: { {k: v['level'] for k, v in planet['buildings'].items()} }")

                # Save the empire snapshot to a file
                timestamp_str = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                filename = f"empire_snapshot_{timestamp_str.replace(':', '').replace('-', '').replace('.', '')}.json"
                snapshot: EmpireSnapshotDict = {
                    "timestamp": timestamp_str,
                    "planets": cast(List[PlanetDict], empire_data['planets'])
                }
                save_empire_snapshot(snapshot, filename)

                # Always check and upgrade storages if needed (every loop)
                upgrade_full_storages(snapshot, notifier)

                sleep_random_interval()
        except KeyboardInterrupt:
            print("\nBot stopped by user.")
            if notifier:
                notifier.send_message("OGameBot is now INACTIVE.")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
