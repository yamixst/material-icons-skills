"""Offline unit tests for download_icon.py."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills/material-symbols-downloader/scripts/download_icon.py"
spec = importlib.util.spec_from_file_location("download_icon", SCRIPT)
download_icon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(download_icon)

RELEASE = "https://fonts.gstatic.com/s/i/short-term/release"
LEGACY_ONLY = ["Material Symbols Outlined", "Material Symbols Rounded", "Material Symbols Sharp"]

METADATA = {
    "icons": [
        {"name": "delete", "popularity": 70000, "tags": ["bin", "trash", "garbage"], "categories": ["UI actions"]},
        {"name": "restore_from_trash", "popularity": 1000, "tags": ["back", "undo"], "categories": ["UI actions"]},
        {"name": "settings", "popularity": 90000, "tags": ["gear", "options"], "categories": ["UI actions"]},
        {"name": "home", "popularity": 100000, "tags": ["house"], "categories": ["UI actions"]},
        {"name": "home_pin", "popularity": 500, "tags": ["map"], "categories": ["Maps"]},
        {"name": "arrow_back", "popularity": 80000, "tags": ["left"], "categories": ["UI actions"]},
        {"name": "home", "popularity": 9, "tags": ["house"], "unsupported_families": LEGACY_ONLY},
    ]
}


class BuildDownloadUrlTest(unittest.TestCase):
    def test_default_xml(self):
        self.assertEqual(
            download_icon.build_download_url("home"),
            f"{RELEASE}/materialsymbolsoutlined/home/default/24px.xml",
        )

    def test_variant_svg(self):
        self.assertEqual(
            download_icon.build_download_url("home", style="sharp", size=48, output_format="svg", fill=1, weight=700, grade=200),
            f"{RELEASE}/materialsymbolssharp/home/wght700grad200fill1/48px.svg",
        )

    def test_negative_grade(self):
        self.assertEqual(download_icon.build_asset_variant_folder(grade=-25), "gradN25")

    def test_compose(self):
        self.assertEqual(
            download_icon.build_download_url("home", style="rounded", output_format="compose", fill=1),
            "https://fonts.gstatic.com/render/v1/Material+Symbols+Rounded/24dp/home.kt"
            "?var=opsz,wght,FILL,GRAD,ROND@24,400,1,0,50",
        )

    def test_apple_default(self):
        self.assertEqual(
            download_icon.build_download_url("toggle_on", output_format="apple"),
            f"{RELEASE}/materialsymbolsoutlined/toggle_on/default/toggle_on_symbol.svg",
        )

    def test_apple_ignores_weight(self):
        self.assertEqual(
            download_icon.build_download_url("toggle_on", output_format="apple", fill=1, weight=700, grade=200),
            f"{RELEASE}/materialsymbolsoutlined/toggle_on/grad200fill1/toggle_on_grad200fill1_symbol.svg",
        )


class SearchTest(unittest.TestCase):
    def names(self, query):
        return [icon["name"] for icon in download_icon.search_icons(METADATA, query)]

    def test_tag_match_ranks_above_name_substring(self):
        self.assertEqual(self.names("trash"), ["delete", "restore_from_trash"])

    def test_search_by_tag(self):
        self.assertEqual(self.names("gear"), ["settings"])

    def test_multi_word_query(self):
        self.assertEqual(self.names("arrow back"), ["arrow_back"])

    def test_exact_name_first_and_legacy_icons_excluded(self):
        self.assertEqual(self.names("home"), ["home", "home_pin"])

    def test_no_results(self):
        self.assertEqual(self.names("xyzzy"), [])


class SuggestionsTest(unittest.TestCase):
    def test_misspelled_name(self):
        self.assertEqual(download_icon.suggest_icon_names(METADATA, "setings")[0], "settings")

    def test_name_by_meaning(self):
        self.assertEqual(download_icon.suggest_icon_names(METADATA, "trash")[0], "delete")

    def test_check_icon_name(self):
        self.assertTrue(download_icon.check_icon_name(METADATA, "home"))
        self.assertFalse(download_icon.check_icon_name(METADATA, "homee"))
        self.assertTrue(download_icon.check_icon_name(None, "anything"))


class OutputPathTest(unittest.TestCase):
    def test_default_names(self):
        self.assertEqual(download_icon.resolve_output_path("home", None, "xml"), Path("ic_home.xml"))
        self.assertEqual(download_icon.resolve_output_path("arrow_back", None, "compose"), Path("ArrowBack.kt"))

    def test_wrong_extension_is_replaced(self):
        self.assertEqual(download_icon.resolve_output_path("home", "icon.png", "svg"), Path("icon.svg"))

    def test_directory_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(download_icon.resolve_output_path("home", tmp, "xml"), Path(tmp) / "ic_home.xml")
        self.assertEqual(download_icon.resolve_output_path("home", "new_dir/", "svg"), Path("new_dir/ic_home.svg"))


class ComposeTest(unittest.TestCase):
    SOURCE = (
        "package com.example.test\n\n"
        "public val close: ImageVector\n"
        "  get() {\n"
        "    if (_close != null) {\n"
        "      return _close!!\n"
        "    }\n"
        '    _close = ImageVector.Builder(name = "close").apply { close() }\n'
        "  }\n\n"
        "private var _close: ImageVector? = null\n"
    )

    def test_identifier(self):
        self.assertEqual(download_icon.compose_identifier("arrow_back"), "ArrowBack")
        self.assertEqual(download_icon.compose_identifier("10k"), "Icon10k")

    def test_prepare_source_renames_property_but_not_calls(self):
        result = download_icon.prepare_compose_source(self.SOURCE, "close", "com.acme.icons")
        self.assertIn("package com.acme.icons\n", result)
        self.assertIn("public val Close: ImageVector", result)
        self.assertIn("private var _Close", result)
        self.assertIn('name = "Close"', result)
        self.assertIn("close()", result)
        self.assertNotIn("_close", result)

    def test_prepare_source_without_package(self):
        result = download_icon.prepare_compose_source(self.SOURCE, "close", None)
        self.assertNotIn("package", result)

    def test_infer_package(self):
        path = Path("app/src/main/java/com/acme/ui/icons/Close.kt")
        self.assertEqual(download_icon.infer_kotlin_package(path), "com.acme.ui.icons")
        self.assertIsNone(download_icon.infer_kotlin_package(Path("icons/Close.kt")))


if __name__ == "__main__":
    unittest.main()
