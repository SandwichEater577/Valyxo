from __future__ import annotations
import json
import os
import core.constants as const


class ThemesManager:
    @staticmethod
    def load_settings() -> dict:
        if os.path.exists(const.CONFIG_PATH):
            try:
                with open(const.CONFIG_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return const.DEFAULT_SETTINGS.copy()
        return const.DEFAULT_SETTINGS.copy()

    @staticmethod
    def save_settings(settings: dict) -> None:
        try:
            os.makedirs(os.path.dirname(const.CONFIG_PATH), exist_ok=True)
            with open(const.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2)
        except Exception:
            pass

    @staticmethod
    def load_themes() -> dict:
        if os.path.exists(const.THEMES_PATH):
            try:
                with open(const.THEMES_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return const.DEFAULT_THEMES.copy()
        return const.DEFAULT_THEMES.copy()

    @staticmethod
    def save_themes(themes: dict) -> None:
        try:
            os.makedirs(os.path.dirname(const.THEMES_PATH), exist_ok=True)
            with open(const.THEMES_PATH, "w", encoding="utf-8") as f:
                json.dump(themes, f, indent=2)
        except Exception:
            pass
