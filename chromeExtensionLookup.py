#!/usr/bin/env python3
"""
Chrome Extension Lookup Tool
Enumerates installed Chrome extensions and looks up their names on the Chrome Web Store.
"""

import sys
import time
import argparse
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Chrome Web Store base URL
CHROME_WEBSTORE_URL = "https://chromewebstore.google.com/detail/"

def get_chrome_base_path(username: str | None = None) -> Path:
    """Return the Chrome user data directory for the current platform."""
    if sys.platform == "win32":
        home = Path("C:/Users") / username if username else Path.home()
        return home / "AppData" / "Local" / "Google" / "Chrome" / "User Data"

    if sys.platform == "darwin":
        home = Path("/Users") / username if username else Path.home()
        return home / "Library" / "Application Support" / "Google" / "Chrome"

    raise RuntimeError(f"Unsupported platform: {sys.platform}")

def get_chrome_extensions(username: str | None = None) -> list[tuple[str, str]]:
    """Find all installed Chrome extensions for a user."""
    chrome_base = get_chrome_base_path(username)

    if not chrome_base.exists():
        print(f"❌ Chrome profile directory not found: {chrome_base}")
        sys.exit(1)

    extensions = []

    # Look in Default and all Profile folders
    for profile_dir in chrome_base.iterdir():
        ext_dir = profile_dir / "Extensions"
        if ext_dir.is_dir():
            print(f"📂 Scanning profile: {profile_dir.name}")
            for ext_id in ext_dir.iterdir():
                if ext_id.is_dir() and not ext_id.name.startswith('.'):
                    extensions.append((profile_dir.name, ext_id.name))

    return extensions


def lookup_extension_name(ext_id: str, delay: float = 1.0) -> str:
    """Lookup extension name from Chrome Web Store."""
    if ext_id == "pkedcjkdefgpdelpbcmbmeomcjbeemfm":
        return "Google Cast (Chromecast)"

    url = CHROME_WEBSTORE_URL + ext_id

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Try multiple ways to get the title
        title_tag = soup.find("meta", property="og:title")
        if title_tag and title_tag.get("content"):
            return title_tag["content"].strip()

        # Fallback: look for h1 title
        h1 = soup.find("h1")
        if h1:
            return h1.get_text().strip()

        return "Unknown (title not found)"

    except requests.exceptions.RequestException as e:
        return f"Error looking up: {str(e)[:80]}"
    except Exception:
        return "Unknown (parsing failed)"
    finally:
        time.sleep(delay)  # Be nice to Google's servers


def main():
    parser = argparse.ArgumentParser(description="Enumerate and lookup Chrome extensions")
    parser.add_argument("-u", "--user", default=None,
                        help="Local username to inspect (default: current user)")
    parser.add_argument("-d", "--delay", type=float, default=1.2,
                        help="Delay between requests in seconds (default: 1.2)")
    args = parser.parse_args()

    print("🔍 Chrome Extension Lookup Tool")
    print("=" * 50)

    extensions = get_chrome_extensions(args.user)

    if not extensions:
        print("No extensions found.")
        return

    print(f"Found {len(extensions)} extension(s)\n")

    for profile, ext_id in extensions:
        print(f"[{profile}] {ext_id} → ", end="")
        name = lookup_extension_name(ext_id, args.delay)
        print(name)

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
