from playwright.sync_api import Page
import re
from bs4 import BeautifulSoup

from typing import Dict, Any, List, cast, Match
from config.config import OGAME_BASE_URL

from config.types import PlanetResources, PlanetStorage
from constants.resources import ResourceClass, ResourceStorageClass


def extract_empire_view_from_page(page: Page) -> Dict[str, List[Dict[str, Any]]]:
    """
    Navigates to the Empire View page and extracts planet data.
    """
    empire_url = f"{OGAME_BASE_URL}/game/index.php?page=standalone&component=empire"
    page.goto(empire_url)
    page.wait_for_selector("div.planet")  # Wait for at least one planet to load
    html = page.content()
    return extract_empire_view(html)


# --- Empire View Extraction ---
def extract_empire_view(html: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extracts all relevant planet data from the OGame Empire View page HTML.
    Returns a dict with all planets and their info.

    Usage:
        html = page.content()  # Playwright Page
        data = extract_empire_view(html)
    Or:
        data = extract_empire_view_from_page(page)
    """
    soup = BeautifulSoup(html, 'html.parser')
    planets: List[Dict[str, Any]] = []
    for planet_div in soup.select('div.planet'):
        # Defensive: get('class') can be None or list[str]
        planet_classes = planet_div.get('class')
        if (isinstance(planet_classes, list) and 'summary' in planet_classes) or planet_div.get('id') == 'planet0':
            continue

        # Planet ID
        planet_id = cast(str, planet_div.get('id', ''))
        # We cast the result to ensure Pylance stops adding "Unknown"
        
        m: Match[str] | None = re.match(r'planet(\d+)', planet_id)

        if m:
            # Now Pylance knows for sure m is a Match object
            planet_id = int(m.group(1))

        # Name
        name_tag = planet_div.select_one('.planetname')
        if name_tag:
            name = name_tag.get('data-tooltip-title') or name_tag.get_text(strip=True)
        else:
            name = None

        # Coords
        coords = None
        coords_tag = planet_div.select_one('.planetDataTop ul li.coords.textLeft a')
        if coords_tag:
            coords = coords_tag.get_text(strip=True)
        else:
            # fallback: sometimes not a link
            coords_tag = planet_div.select_one('.planetDataTop ul li.coords.textLeft')
            coords = coords_tag.get_text(strip=True) if coords_tag else None

        # Fields
        fields = None
        fields_tag = planet_div.select_one('.planetDataTop ul li.fields.textRight')
        if fields_tag:
            fields = fields_tag.get_text(strip=True)

        # Temperature
        temp = None
        temp_tag = planet_div.select_one('.planetDataBottom ul li.fields.textCenter')
        if temp_tag:
            temp = temp_tag.get_text(strip=True)

        # Energy
        energy = None
        energy_tag = planet_div.select_one('.planetDataTop ul li.coords.textRight .undermark')
        if energy_tag:
            energy = energy_tag.get_text(strip=True)

        # Resources
        resources: PlanetResources = {}
        for res in ResourceClass.allResources():
            tag = planet_div.select_one(f'.values.resources .{res} span')
            if tag:
                val = tag.get_text(strip=True).replace(',', '')
                try:
                    resources[res] = int(val)
                except ValueError:
                    resources[res] = val
            else:
                # Sometimes no <span>
                tag = planet_div.select_one(f'.values.resources .{res}')
                if tag:
                    val = tag.get_text(strip=True).replace(',', '')
                    try:
                        resources[res] = int(val)
                    except ValueError:
                        resources[res] = val

        # Storage
        storage: PlanetStorage = {}
        for res in ResourceStorageClass.allStorages():
            tag = planet_div.select_one(f'.values.storage .{res}')
            if tag:
                val = tag.get_text(strip=True).replace(',', '')
                try:
                    storage[res] = int(val)
                except ValueError:
                    storage[res] = val
            else:
                print(f"[DEBUG] Storage extraction: tag for '{res}' not found in planet {planet_id} ({name})")

        # Helper to extract building/ship/defense/research/lifeform levels
        def escape_class(cls: str) -> str:
            # Escape class selectors starting with a digit for SoupSieve/CSS
            if cls and cls[0].isdigit():
                return f'.\\3{cls[0]} {cls[1:]}' if len(cls) > 1 else f'.\\3{cls[0]} '
            return f'.{cls}'

        def extract_group(group: str, ids: List[str]) -> Dict[str, Dict[str, Any]]:
            result: Dict[str, Dict[str, Any]] = {}
            for id_ in ids:
                sel = f'.values.{group} {escape_class(id_)}'
                tag = planet_div.select_one(sel)
                if tag:
                    if group in ['ships', 'defence']:
                        # Extract only the first direct text node from the div
                        val = next((content.strip() for content in tag.contents if isinstance(content, str)), '')
                        try:
                            level = int(val)
                        except ValueError:
                            level = val

                        upgradable = False
                        upgrade_js = None
                    else:
                        # For other groups (e.g., buildings), check for <span> or <a> tags
                        level_tag = tag.find(['span', 'a'])
                        if not level_tag:
                            # Sometimes just text
                            val = tag.get_text(strip=True).replace(',', '')
                            try:
                                level = int(val)
                            except ValueError:
                                level = val
                            upgradable = False
                            upgrade_js = None
                        else:
                            val = level_tag.get_text(strip=True).replace(',', '')
                            try:
                                level = int(val)
                            except ValueError:
                                level = val
                            upgradable = (level_tag.name == 'a')
                            upgrade_js = level_tag.get('onclick') if upgradable else None

                    result[str(id_)] = {
                        'level': level,
                        'upgradable': upgradable,
                        'upgrade_js': upgrade_js
                    }
            return result

        # Building/ship/defense/research/lifeform IDs (from config or hardcoded)
        supply_ids = ['1', '2', '3', '4', '12', '22', '23', '24']
        station_ids = ['14', '15', '21', '31', '33', '34', '44', '36']
        defense_ids = ['401', '402', '403', '404', '405', '406', '407', '408', '502', '503']
        ship_ids = ['204', '205', '206', '207', '215', '211', '213', '214', '218', '219', '202', '203', '208', '209', '210', '212', '217']
        research_ids = ['113', '120', '121', '114', '122', '106', '108', '124', '123', '199', '115', '117', '118', '109', '110', '111']
        lifeform_building_ids = [str(11101 + i) for i in range(18)]
        lifeform_research_ids = [str(11201 + i) for i in range(18)]

        buildings = extract_group('supply', supply_ids)
        station = extract_group('station', station_ids)
        defense = extract_group('defence', defense_ids)
        ships = extract_group('ships', ship_ids)
        research = extract_group('research', research_ids)
        lifeform_buildings = extract_group('lifeform1buildings', lifeform_building_ids)
        lifeform_research = extract_group('lifeform1research', lifeform_research_ids)

        planets.append({
            'id': planet_id,
            'name': name,
            'coords': coords,
            'fields': fields,
            'temperature': temp,
            'energy': energy,
            'resources': resources,
            'storage': storage,
            'buildings': buildings,
            'station': station,
            'defense': defense,
            'ships': ships,
            'research': research,
            'lifeform_buildings': lifeform_buildings,
            'lifeform_research': lifeform_research
        })

    return {'planets': planets}
