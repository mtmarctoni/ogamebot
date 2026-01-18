from typing import Any, Dict, TypeVar, cast, overload
from config.types import ConfigType

T = TypeVar("T")

class KeyNotFoundError(Exception):
    pass

class SafeTypedConfig:
    def __init__(self, raw: ConfigType):
        self._raw = raw

    @overload
    def get_typed(self, key: str) -> Any: ...
    @overload
    def get_typed(self, key: str, default: T) -> T: ...

    def get_typed(self, key: str, default: Any = None) -> Any:
        if key in self._raw:
            return cast(Any, self._raw[key])
        if default is not None:
            return default
        raise KeyNotFoundError(f"Required config key '{key}' not found and no default was provided.")

    def get_nested_typed(self, key: str, subkey: str, default: Any = None) -> Any:
        if key in self._raw and isinstance(self._raw[key], dict):
            subdict = cast(Dict[str, Any], self._raw[key])
            if subkey in subdict:
                return subdict[subkey]
        if default is not None:
            return default
        raise KeyNotFoundError(f"Required nested config key '{key}.{subkey}' not found and no default was provided.")

    def get_check_interval(self) -> int:
        return cast(int, self.get_typed("check_interval"))

    def get_expedition_planet_id(self) -> str:
        expeditions = self.get_typed("expeditions")
        if "expedition_planet_id" in expeditions:
            return expeditions["expedition_planet_id"]
        return ""

    def get_enable_expeditions(self) -> bool:
        expeditions = self.get_typed("expeditions")
        if "enable_expeditions" in expeditions:
            return expeditions["enable_expeditions"]
        return True

    def get_upgrade_toggles(self) -> Dict[str, bool]:
        upgrades = self.get_typed("upgrades")
        if "toggles" in upgrades:
            return upgrades["toggles"]
        return {}

    # Add more helpers for deeply nested fields as needed!
