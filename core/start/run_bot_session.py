import os
import traceback
from typing import Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

from config.config import LOBBY_URL, COMPONENT_URL_TEMPLATE, DEFAULT_PLANET_ID  
from config.types import ConfigType, ExpeditionConfig, DiscoveriesConfig
from core.auth.session_manager import save_session, load_session
from core.navigation.universe import enter_universe
from core.data.snapshot_manager import save_empire_snapshot
from core.utils.attack_detection import check_for_attack_alert
from core.utils.sleep_utils import sleep_for_minimum_duration
from core.info.empire import extract_empire_info
from core.upgrade.handle_upgrades import handle_upgrades
from core.expeditions.handle_expeditions import handle_expeditions
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.discoveries.handle_discoveries import handle_discoveries
from services.manage_config import reload_config
from services.typed_config import SafeTypedConfig

def run_bot_session(notifier: Optional[TelegramNotifier]) -> bool:
    """
    Runs a single bot session. Returns True if it should restart, False if stopped by user.
    """
    browser = None
    try:
        with sync_playwright() as p:
            session_exists = os.path.exists("fb_session.json")
            browser, context = load_session(p)
            page = context.new_page()
            page.goto(LOBBY_URL)
            if not session_exists:
                print("[INFO] No session found. Please log in with Facebook manually.")
                input("Press Enter after you have logged in and see the lobby...")
                save_session(context)
                print("[INFO] FB session saved.")
            else:
                 print("[INFO] Existing FB session found. Logging in automatically.")
            print("[INFO] Navigating to main game universe...")
            game_page = enter_universe(page)
            # After entering, optionally go directly to overview using config
            try:
                url = COMPONENT_URL_TEMPLATE.format(planet_id=DEFAULT_PLANET_ID)
                game_page.goto(url)
                game_page.wait_for_selector('a.menubutton.selected span.textlabel', timeout=10000)
                assert game_page.inner_text('a.menubutton.selected span.textlabel') == "Resources"
            except Exception:
                pass

            while True:
                # Reload configuration dynamically
                config: ConfigType = reload_config()
                safe_config = SafeTypedConfig(config)

                print("[INFO] Entered main game.")

                # --- Attack detection (overview page) ---
                print("[INFO] Checking for attack alerts on Overview page...")
                attack_info = check_for_attack_alert(game_page)
                if attack_info and notifier:
                    safe_notify(notifier, f"⚠️ ALERT: {attack_info}")

                # --- Get Empire Info ---
                print("[INFO] Navigating to Empire View and extracting all planet and moon data...")
                empire_data = extract_empire_info(game_page, notifier)

                # Save the empire snapshot to a file
                save_empire_snapshot(empire_data)

                # Handle all upgrades for the empire
                upgrade_duration = handle_upgrades(empire_data, game_page, notifier, config)

                # Handle expeditions based on dynamic config
                if safe_config.get_enable_expeditions():
                    handle_expeditions(game_page, empire_data, notifier, ExpeditionConfig(target_id=safe_config.get_expedition_planet_id()))
                else:
                     print("[INFO] Expeditions are disabled in the configuration.")
                
                # Handle discoveries based on dynamic config
                if safe_config.get_enable_discoveries():
                    handle_discoveries(game_page, empire_data, notifier, DiscoveriesConfig(target_id=safe_config.get_discovery_planet_id()))
                else:
                    print("[INFO] Discoveries are disabled in the configuration.")
                
                next_action_duration = max(1, upgrade_duration)
                # Sleep for the minimum duration across all planets
                check_interval = safe_config.get_check_interval()
                if check_interval > 0:
                    sleep_for_minimum_duration(next_action_duration, notifier, check_interval)
                else:
                    sleep_for_minimum_duration(next_action_duration, notifier, None)


    except KeyboardInterrupt:
        print("[WARN] Bot stopped by user.")
        if notifier:
            safe_notify(notifier, "OGameBot is now INACTIVE.")
        return False  # Don't restart on user interrupt
    except (PlaywrightTimeoutError, PlaywrightError) as e:
        error_msg = f"Playwright error (page likely stale): {type(e).__name__}: {e}"
        print(f"\n❌ {error_msg}")
        print(traceback.format_exc())
        if notifier:
            safe_notify(notifier, f"⚠️ Bot encountered an error and will restart:\n{error_msg}")
        return True  # Request restart
    except Exception as e:
        error_msg = f"Unexpected error: {type(e).__name__}: {e}"
        print(f"\n❌ {error_msg}")
        print(traceback.format_exc())
        if notifier:
            safe_notify(notifier, f"⚠️ Bot encountered an unexpected error and will restart:\n{error_msg}")
        return True  # Request restart
    finally:
        if browser:
            try:
                browser.close()
                print("[INFO] Browser closed.")
            except Exception:
                pass  # Ignore errors when closing browser

    return False