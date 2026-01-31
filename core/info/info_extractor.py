import re
from bs4 import BeautifulSoup

from typing import Dict, Any, List, cast, Match

from config.config import PLANETS
from constants.lifeforms import LifeformClass, Lifeforms
from config.types import PlanetResources, PlanetStorage, PlanetDict
from constants.resources import ResourceClass, ResourceStorageClass


# --- Empire View Extraction ---
def extract_empire_view(html: str, is_moon: bool = False) -> Dict[str, List[PlanetDict]]:
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
    planets: List[PlanetDict] = []
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

        # Specie
        specie = {
            'id': '0',
            'name': 'Unknown'
        }
        # use PLANETS config to get specie info
        for _, planet_info in PLANETS.items():
            if str(planet_info.get('id')) == str(planet_id):
                specie['name'] = planet_info.get('species', 'human').lower()
                specie['id'] = LifeformClass.get_id_by_name(Lifeforms(specie['name']))
                break   

        # Resources
        resources: PlanetResources = {
            "metal": 0,
            "crystal": 0,
            "deuterium": 0,
            "energy": 0,
            "food": 0,
            "population": 0
        }
        for res in ResourceClass.get_all_names():
            res_str = str(res)
            tag = planet_div.select_one(f'.values.resources .{res_str} span')
            if tag:
                val = tag.get_text(strip=True).replace(',', '')
                try:
                    resources[res_str] = int(val)
                except ValueError:
                    resources[res_str] = val
            else:
                # Sometimes no <span>
                tag = planet_div.select_one(f'.values.resources .{res_str}')
                if tag:
                    val = tag.get_text(strip=True).replace(',', '')
                    try:
                        resources[res_str] = int(val)
                    except ValueError:
                        resources[res_str] = val

        # Storage
        storage: PlanetStorage = {
            "metalStorage": 0,
            "crystalStorage": 0,
            "deuteriumStorage": 0,
            "foodStorage": 0,
            "populationStorage": 0
        }
        for res in ResourceStorageClass.get_all_names():
            tag = planet_div.select_one(f'.values.storage .{res}')
            if tag:
                val = tag.get_text(strip=True).replace(',', '')
                try:
                    storage[str(res)] = int(val)
                except ValueError:
                    storage[str(res)] = val
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
                        val = val.replace(',', '')  # Remove commas for proper integer conversion
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

        # Generate lifeform building and research IDs dynamically for all species
        lifeform_building_ids = [str((int('1' + specie.get("id", "") + '101') + i)) for i in range(12)]
        lifeform_research_ids = [str((int('1' + specie.get("id", "") + '201') + i)) for i in range(18)]


        buildings = extract_group('supply', supply_ids)
        station = extract_group('station', station_ids)
        defense = extract_group('defence', defense_ids)
        ships = extract_group('ships', ship_ids)
        research = extract_group('research', research_ids)
        # Extract lifeform buildings dynamically
        lifeform_buildings = extract_group(f'lifeform{specie.get("id", "")}buildings', lifeform_building_ids)

        # Extract lifeform research for all species, ignoring moons
        lifeform_research = {}
        if not is_moon:
            for species_id in LifeformClass.get_all_ids():
                lifeform_research_ids = [str((int('1' + species_id + '201') + i)) for i in range(18)]
                group_research = extract_group(f'lifeform{species_id}research', lifeform_research_ids)

                # Add only upgradable entries to the consolidated dictionary
                for research_id, research_data in group_research.items():
                    if research_data.get('upgradable', False):
                        lifeform_research[research_id] = research_data

        plante_to_append: PlanetDict = cast(PlanetDict, {
            'id': planet_id,
            'name': name,
            'coords': coords,
            'fields': fields,
            'temperature': temp,
            'energy': energy,
            'type': 'moon' if is_moon else 'planet',
            'specie': specie['name'],
            'resources': resources,
            'storage': storage,
            'buildings': buildings,
            'facilities': station,
            'defense': defense,
            'ships': ships,
            'research': research,
            'lifeform_buildings': lifeform_buildings,
            'lifeform_research': lifeform_research
        })
        
        planets.append(plante_to_append)

    planets_data: Dict[str, List[PlanetDict]] = {'planets': planets}

    return planets_data
