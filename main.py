import os
from playwright.sync_api import sync_playwright
from config.config import LOBBY_URL, COMPONENT_URL_TEMPLATE, DEFAULT_PLANET_ID
from config.telegram_config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

from core.notifications.telegram_notifier import TelegramNotifier

from core.auth.session_manager import save_session, load_session
from core.navigation.universe import enter_universe
from core.data.snapshot_manager import save_empire_snapshot
from core.upgrade.auto_storage import upgrade_full_storages
from core.upgrade.lifeform_buildings import handle_lifeform_uildings_upgrade
from core.utils.attack_detection import check_for_attack_alert
from core.utils.sleep_utils import sleep_for_minimum_duration
from core.info.empire import extract_empire_info
from core.upgrade.buildings import handle_resources_upgrades

def main() -> None:
    notifier = None
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        notifier = TelegramNotifier(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
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
            url = COMPONENT_URL_TEMPLATE.format(planet_id=DEFAULT_PLANET_ID)
            game_page.goto(url)
            game_page.wait_for_selector('a.menubutton.selected span.textlabel', timeout=10000)
            assert game_page.inner_text('a.menubutton.selected span.textlabel') == "Resources"
        except Exception:
            pass

        try:
            while True:
                print("Entered main game.")

                # --- Attack detection (overview page) ---
                print("\nChecking for attack alerts on Overview page...")
                attack_info = check_for_attack_alert(game_page)
                if attack_info and notifier:
                    notifier.send_message(f"⚠️ ALERT: {attack_info}")

                # --- Get Empire Info ---
                print("\nNavigating to Empire View page and extracting all planets data...")
                empire_data = extract_empire_info(game_page, notifier)

                # Save the empire snapshot to a file
                save_empire_snapshot(empire_data)

                # Check and upgrade resources (metal, crystal, deuterium) on all planets
                resource_upgrade_durations = handle_resources_upgrades(empire_data, game_page, notifier)

                # Always check and upgrade storages if needed (every loop)
                storage_upgrade_durations = upgrade_full_storages(empire_data, game_page, notifier)

                # Check and upgrade lifeform buildings if applicable
                lifeform_upgrade_durations = handle_lifeform_uildings_upgrade(empire_data, game_page, notifier)

                sleep_for_minimum_duration(
                    storage_upgrade_durations + resource_upgrade_durations + lifeform_upgrade_durations,
                    notifier
                )
        except KeyboardInterrupt:
            print("\nBot stopped by user.")
            if notifier:
                notifier.send_message("OGameBot is now INACTIVE.")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
