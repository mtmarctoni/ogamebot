import os
import traceback
from typing import Optional, cast
from playwright.sync_api import Browser, sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

from config.config import LOBBY_URL, COMPONENT_URL_TEMPLATE, DEFAULT_PLANET_ID  
from config.types import ConfigType, ExpeditionConfig, DiscoveriesConfig
from constants.general import COMPONENTS
from core.auth.session_manager import save_session, load_session
from core.navigation.universe import enter_universe
from core.data.snapshot_manager import save_empire_snapshot
from core.utils.attack_detection import check_for_attack_alert
from core.utils.sleep_utils import sleep_for_minimum_duration
from core.info.empire import extract_empire_info
from core.upgrade.handle_upgrades import handle_upgrades
from core.upgrade.defense import ensure_schedule_state_file, handle_scheduled_defense_build
from core.expeditions.handle_expeditions import handle_expeditions
from core.transport.handle_transports import handle_transports
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.discoveries.handle_discoveries import handle_discoveries
from services.manage_config import reload_config
from core.utils.cookie_banner import handle_cookie_banner

def run_bot_session(notifier: Optional[TelegramNotifier]) -> bool:
    """
    Runs a single bot session. Returns True if it should restart, False if stopped by user.
    """
    browser: Optional[Browser] = None
    try:
        with sync_playwright() as p:
            ensure_schedule_state_file()
            session_exists = os.path.exists("fb_session.json")
            browser, context = load_session(p)
            page = context.new_page()
            page.goto(LOBBY_URL)
            handle_cookie_banner(page)
            if not session_exists:
                print("[INFO] No session found. Please log in with Facebook manually.")
                input("Press Enter after you have logged in and see the lobby...")
                handle_cookie_banner(page)
                save_session(context)
                print("[INFO] FB session saved.")
            else:
                 print("[INFO] Existing FB session found. Logging in automatically.")
            print("[INFO] Navigating to main game universe...")
            game_page = enter_universe(page)
            handle_cookie_banner(game_page)
            # After entering, optionally go directly to overview using config
            try:
                url = COMPONENT_URL_TEMPLATE.format(
                    component=COMPONENTS.OVERVIEW.value,
                    planet_id=DEFAULT_PLANET_ID,
                )
                game_page.goto(url)
                handle_cookie_banner(game_page)
                game_page.wait_for_selector('a.menubutton.selected span.textlabel', timeout=10000)
                assert game_page.inner_text('a.menubutton.selected span.textlabel') == "Overview"
            except Exception:
                pass

            while True:
                # Reload configuration dynamically
                config = cast(ConfigType, reload_config())

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

                # Handle expeditions based on dynamic config
                if config["expeditions"]["enable_expeditions"]:
                    expedition_config: ExpeditionConfig = {
                        "target_id": config["expeditions"]["expedition_planet_id"],
                    }
                    expedition_duration = handle_expeditions(
                        game_page,
                        empire_data,
                        notifier,
                        expedition_config,
                    )
                else:
                    print("[INFO] Expeditions are disabled in the configuration.")
                    expedition_duration = 0

                # Handle transports based on dynamic config
                if config["transports"]["enable_transports"]:
                    transport_duration = handle_transports(
                        game_page,
                        empire_data,
                        notifier,
                        config["transports"],
                        config["expeditions"]["expedition_planet_id"],
                    )
                else:
                    print("[INFO] Transports are disabled in the configuration.")
                    transport_duration = 0

                # Handle all upgrades for the empire
                upgrade_duration = handle_upgrades(empire_data, game_page, notifier, config)

                defense_duration = handle_scheduled_defense_build(game_page, empire_data, notifier, config)
                
                # Handle discoveries based on dynamic config
                if config["discoveries"]["enable_discoveries"]:
                    discovery_config: DiscoveriesConfig = {
                        "target_id": config["discoveries"]["discovery_planet_id"],
                    }
                    discovery_duration = handle_discoveries(
                        game_page,
                        empire_data,
                        notifier,
                        discovery_config,
                    )
                else:
                    print("[INFO] Discoveries are disabled in the configuration.")
                    discovery_duration = 0
                
                durations: list[int] = [
                    duration
                    for duration in [upgrade_duration, expedition_duration, transport_duration, defense_duration, discovery_duration]
                    if duration > 0
                ]

                check_interval = config["check_interval"]
                heartbeat_seconds = check_interval * 60 if check_interval > 0 else 0
                next_action_duration = min(durations) if durations else heartbeat_seconds

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
