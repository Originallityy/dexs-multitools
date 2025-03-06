# Integrated requirements and auto-installation
def install_requirements():
    import pkg_resources, subprocess, sys
    with open('requirements.txt') as f:
        required = f.read().splitlines()
    try:
        pkg_resources.require(required)
    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
        print("Installing missing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + required)

install_requirements()

import requests
import json
import socket
import struct
import time
import os
import sys
import select
import platform
import psutil
import ctypes
import webbrowser
import dns.resolver
import speedtest
import mimetypes
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from tqdm import tqdm
try:
    from pytube import YouTube
except ImportError:
    print("Pytube is not installed. Please install it with: pip install pytube")
    input("Press Enter to return...")
    exit()

def patched_title(self):
    try:
        return self.vid_info['videoDetails']['title']
    except KeyError:
        # Option: prompt user for a fallback or simply return a default title
        fallback = input("Unable to fetch title. Enter a title manually or press Enter to use 'Unknown Title': ").strip()
        return fallback if fallback else "Unknown Title"
YouTube.title = property(patched_title)

# Define ANSI color codes and styles
STYLE_GRAY = "\033[90m"    # Bright black (gray)
STYLE_RESET = "\033[0m"    # Reset all styles
STYLE_DIM = "\033[2m"      # Dim text (alternative to gray)

# Define default gradient colors
# Colors

RED = (255, 0, 0)
ORANGE = (255, 165, 0)
ORANGE_YELLOW = (255, 200, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (238, 130, 238)

# Gradient colors
GRADIENT_START_COLOR = (RED)    # Red
GRADIENT_END_COLOR = (ORANGE_YELLOW)    # Orange-Yellow

# New: define gradient colors for unavailable options (dark gray to light gray)
UNAVAILABLE_GRADIENT_START = (64, 64, 64)
UNAVAILABLE_GRADIENT_END   = (211, 211, 211)  # Updated from (128,128,128)

# Global menu state variables
current_menu_page = 0
current_submenu = None  # None indicates we're at the top level menu
COLORS_ENABLED = True                 # Set to False to disable all colors

# Override standard print function with gradient version
original_print = print

def gradient_text(text, start_color=None, end_color=None):
    """Apply a gradient to text from left to right"""
    # If text already contains the gray style, skip gradient processing.
    if STYLE_GRAY in text:
        return text

    if not COLORS_ENABLED or not sys.stdout.isatty():
        return text

    if start_color is None:
        start_color = GRADIENT_START_COLOR
    if end_color is None:
        end_color = GRADIENT_END_COLOR

    result = ""
    text_length = len(text)
    if text_length == 0:
        return text

    i = 0
    while i < text_length:
        char = text[i]
        # Skip ANSI escape sequences
        if char == '\033':
            escape_end = text.find('m', i)
            if escape_end != -1:
                escape_seq = text[i:escape_end+1]
                result += escape_seq
                i = escape_end + 1
                continue
        ratio = i / (text_length - 1) if text_length > 1 else 0
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        result += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        i += 1
    return result

def print(*args, sep=' ', end='\n', file=None, flush=False):
    """Overridden print function that applies gradient to all text"""
    if file is None:
        file = sys.stdout
    
    # If printing to stdout and colors are enabled, apply gradient
    if file is sys.stdout and COLORS_ENABLED and sys.stdout.isatty():
        # Convert all arguments to strings and apply gradient
        colored_args = [gradient_text(str(arg)) for arg in args]
        original_print(*colored_args, sep=sep, end=end, file=file, flush=flush)
    else:
        # Fixed: Use end=end instead of end=sep
        original_print(*args, sep=sep, end=end, file=file, flush=flush)

# Also override input to use gradient for prompts
original_input = input

def input(prompt=''):
    """Overridden input function that applies gradient to prompt"""
    if COLORS_ENABLED and sys.stdout.isatty():
        return original_input(gradient_text(prompt))
    else:
        return original_input(prompt)

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Helper function for placeholder features
def placeholder_feature(feature_name):
    clear_console()
    print(f"===== {feature_name} =====\n")
    print("This feature is coming soon!")
    input("\nPress Enter to return to the main menu...")

# Define feature functions for each menu option

def is_windows():
    """Check if running on Windows"""
    return os.name == 'nt'

def is_admin():
    """Check if the program has admin privileges"""
    try:
        if is_windows():
            return ctypes.windll.shell32.IsUserAnAdmin()
        return False
    except:
        return False

def check_windows_requirement(func):
    """Decorator to check if running on Windows"""
    def wrapper(*args, **kwargs):
        if not is_windows():
            clear_console()
            print("This feature requires Windows.")
            print("Current system:", platform.system())
            input("\nPress Enter to return to the menu...")
            return
        return func(*args, **kwargs)
    return wrapper

@check_windows_requirement
def registry_tweaks():
    """Registry tweaks functionality"""
    if not is_admin():
        print("This feature requires admin privileges.")
        print("Please use [A] to enable admin privileges.")
        input("\nPress Enter to return to the menu...")
        return
    
    if os.name != 'nt':
        clear_console()
        print("===== Registry Tweaks =====\n")
        print("WARNING: Registry tweaks are designed for Windows operating systems.")
        print("Your current operating system is not Windows.")
        print("The commands may not work as expected or could cause errors.\n")
        choice = input("Do you want to continue anyway? (y/n): ").lower()
        if choice != 'y':
            return
    
    # Internal function to apply registry tweaks
    def apply_registry_tweak(key_location, key_name, key_type, key_value, action="add"):
        """Apply a registry tweak based on the provided parameters"""
        if action.lower() == "add":
            cmd = f'reg add "{key_location}" /v {key_name} /t {key_type} /d {key_value} /f'
        elif action.lower() == "delete":
            cmd = f'reg delete "{key_location}" /v {key_name}" /f'
        return cmd
    
    # Registry tweaks organized in a more readable format
    reg_options = {
        "1": {
            "name": "Disable Windows Defender",
            "description": "Disables Windows Defender real-time protection for better performance.",
            "key_location": r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender",
            "key_name": "DisableAntiSpyware",
            "key_type": "REG_DWORD",
            "apply_value": "1",
            "default_value": "0",
            "action": "add"
        },
        "2": {
            "name": "Speed Up Menu Show Delay",
            "description": "Reduces the delay when showing menus for a snappier experience.",
            "key_location": r"HKCU\Control Panel\Desktop",
            "key_name": "MenuShowDelay",
            "key_type": "REG_SZ",
            "apply_value": "100",
            "default_value": "400",
            "action": "add"
        },
        "3": {
            "name": "Disable Startup Delay",
            "description": "Removes the artificial delay when starting applications at Windows boot.",
            "key_location": r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Serialize",
            "key_name": "StartupDelayInMSec",
            "key_type": "REG_DWORD",
            "apply_value": "0",
            "default_value": "3000",
            "action": "add"
        }
    }
    
    while True:
        clear_console()
        print("===== Registry Tweaks =====\n")
        for key, tweak in reg_options.items():
            print(f"[{key}] {tweak['name']}")
        print("\n[B] Back to main menu")
        
        choice = input("\nSelect a registry tweak: ").upper()
        
        if choice == "B":
            break
        elif choice in reg_options:
            tweak = reg_options[choice]
            clear_console()
            print(f"===== {tweak['name']} =====\n")
            print(f"Description: {tweak['description']}")
            print(f"\nRegistry Information:")
            print(f"Key Location: {tweak['key_location']}")
            print(f"Key Name: {tweak['key_name']}")
            print(f"Key Type: {tweak['key_type']}")
            print(f"Tweak Value: {tweak['apply_value']}")
            print(f"Default Value: {tweak['default_value']}")
            print(f"Action: {tweak['action']}")
            
            print("\n[A] Apply tweak")
            print("[U] Undo tweak (restore default)")
            print("[B] Back to tweaks menu")
            
            action = input("\nSelect an action: ").upper()
            
            if action == "A":
                confirm = input(f"Are you sure you want to apply '{tweak['name']}'? (y/n): ").lower()
                if confirm == "y":
                    print(f"\nApplying {tweak['name']}...")
                    cmd = apply_registry_tweak(
                        tweak['key_location'],
                        tweak['key_name'],
                        tweak['key_type'],
                        tweak['apply_value'],
                        tweak['action']
                    )
                    os.system(cmd)
                    print("Tweak applied successfully!")
                    input("\nPress Enter to continue...")
            elif action == "U":
                confirm = input(f"Are you sure you want to restore the default setting for '{tweak['name']}'? (y/n): ").lower()
                if confirm == "y":
                    print(f"\nRestoring default setting for {tweak['name']}...")
                    cmd = apply_registry_tweak(
                        tweak['key_location'],
                        tweak['key_name'],
                        tweak['key_type'],
                        tweak['default_value'],
                        tweak['action']
                    )
                    os.system(cmd)
                    print("Default setting restored successfully!")
                    input("\nPress Enter to continue...")

@check_windows_requirement
def advanced_registry_tweaks():
    """Advanced Registry Tweaks functionality"""
    if not is_admin():
        print("This feature requires admin privileges.")
        print("Please use [A] to enable admin privileges.")
        input("\nPress Enter to return to the menu...")
        return
    
    if os.name != 'nt':
        clear_console()
        print("===== Advanced Registry Tweaks =====\n")
        print("WARNING: Registry tweaks are designed for Windows operating systems.")
        print("Your current operating system is not Windows.")
        print("The commands may not work as expected or could cause errors.\n")
        choice = input("Do you want to continue anyway? (y/n): ").lower()
        if choice != 'y':
            return
    
    # Define advanced registry tweaks
    advanced_tweaks = {
        "1": {
            "name": "Disable Windows Telemetry",
            "description": "Disables Windows data collection and telemetry services.",
            "key_location": r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            "key_name": "AllowTelemetry",
            "key_type": "REG_DWORD",
            "apply_value": "0",
            "default_value": "1",
            "action": "add"
        },
        "2": {
            "name": "Optimize SSD Performance",
            "description": "Disables features that can reduce SSD lifespan.",
            "key_location": r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
            "key_name": "EnableSuperfetch",
            "key_type": "REG_DWORD",
            "apply_value": "0",
            "default_value": "3",
            "action": "add"
        },
        "3": {
            "name": "Accelerate Windows Boot Time",
            "description": "Reduces timeout values to speed up Windows boot process.",
            "key_location": r"HKLM\SYSTEM\CurrentControlSet\Control",
            "key_name": "TimeoutValue",
            "key_type": "REG_DWORD",
            "apply_value": "10",
            "default_value": "30",
            "action": "add"
        },
        "4": {
            "name": "Disable Cortana",
            "description": "Completely turns off the Cortana assistant.",
            "key_location": r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search",
            "key_name": "AllowCortana",
            "key_type": "REG_DWORD",
            "apply_value": "0",
            "default_value": "1",
            "action": "add"
        },
        "5": {
            "name": "Optimize Network Settings",
            "description": "Modifies TCP/IP settings for better network performance.",
            "key_location": r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
            "key_name": "TcpMaxDataRetransmissions",
            "key_type": "REG_DWORD",
            "apply_value": "3",
            "default_value": "5",
            "action": "add"
        },
        "6": {
            "name": "Verbose Messages",
            "description": "Enables detailed status messages during Windows startup and shutdown.",
            "key_location": r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
            "key_name": "VerboseStatus",
            "key_type": "REG_DWORD",
            "apply_value": "1",
            "default_value": "0",
            "action": "add"
        },
        "7": {
            "name": "Disable Windows Updates",
            "description": "Disables automatic Windows updates to prevent unexpected restarts and bandwidth usage.",
            "key_location": r"HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU",
            "key_name": "NoAutoUpdate",
            "key_type": "REG_DWORD",
            "apply_value": "1",
            "default_value": "0",
            "action": "add"
        }
    }
    
    # Internal function to apply registry tweaks
    def apply_registry_tweak(key_location, key_name, key_type, key_value, action="add"):
        """Apply a registry tweak based on the provided parameters"""
        if action.lower() == "add":
            cmd = f'reg add "{key_location}" /v {key_name} /t {key_type} /d {key_value} /f'
        elif action.lower() == "delete":
            cmd = f'reg delete "{key_location}" /v {key_name}" /f'
        return cmd
    
    while True:
        clear_console()
        print("===== Advanced Registry Tweaks =====\n")
        print("These tweaks modify system behavior and performance settings.\n")
        
        for key, tweak in advanced_tweaks.items():
            print(f"[{key}] {tweak['name']}")
        print("\n[B] Back to Registry Tweaks menu")
        
        choice = input("\nSelect an advanced registry tweak: ").upper()
        
        if choice == "B":
            break
        elif choice in advanced_tweaks:
            tweak = advanced_tweaks[choice]
            clear_console()
            print(f"===== {tweak['name']} =====\n")
            print(f"Description: {tweak['description']}")
            print(f"\nRegistry Information:")
            print(f"Key Location: {tweak['key_location']}")
            print(f"Key Name: {tweak['key_name']}")
            print(f"Key Type: {tweak['key_type']}")
            print(f"Tweak Value: {tweak['apply_value']}")
            print(f"Default Value: {tweak['default_value']}")
            print(f"Action: {tweak['action']}")
            
            print("\n[A] Apply tweak")
            print("[U] Undo tweak (restore default)")
            print("[B] Back to advanced tweaks menu")
            
            action = input("\nSelect an action: ").upper()
            
            if action == "A":
                confirm = input(f"Are you sure you want to apply '{tweak['name']}'? (y/n): ").lower()
                if confirm == "y":
                    print(f"\nApplying {tweak['name']}...")
                    cmd = apply_registry_tweak(
                        tweak['key_location'],
                        tweak['key_name'],
                        tweak['key_type'],
                        tweak['apply_value'],
                        tweak['action']
                    )
                    os.system(cmd)
                    print("Tweak applied successfully!")
                    input("\nPress Enter to continue...")
            elif action == "U":
                confirm = input(f"Are you sure you want to restore the default setting for '{tweak['name']}'? (y/n): ").lower()
                if confirm == "y":
                    print(f"\nRestoring default setting for {tweak['name']}...")
                    cmd = apply_registry_tweak(
                        tweak['key_location'],
                        tweak['key_name'],
                        tweak['key_type'],
                        tweak['default_value'],
                        tweak['action']
                    )
                    os.system(cmd)
                    print("Default setting restored successfully!")
                    input("\nPress Enter to continue...")

def download_asset(src, base_url, assets_dir, asset_type, downloaded_assets, proxies=None):
    """Download an asset and save it to the appropriate directory"""
    try:
        # Convert relative URL to absolute
        url = urljoin(base_url, src)
        
        # Skip if already downloaded or if it's a data URL
        if url in downloaded_assets or url.startswith('data:'):
            return
        
        # Add to downloaded set
        downloaded_assets.add(url)
        
        # Get the filename from the URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If no filename or it has no extension, create one based on URL hash
        if not filename or '.' not in filename:
            # Try to guess extension from content type
            guessed_type = mimetypes.guess_type(url)[0]
            if guessed_type:
                ext = mimetypes.guess_extension(guessed_type) or '.bin'
            else:
                ext = '.bin'
            filename = f"asset_{hash(url) % 10000}{ext}"
        
        # Create directory for this asset type if it doesn't exist
        asset_type_dir = os.path.join(assets_dir, asset_type)
        os.makedirs(asset_type_dir, exist_ok=True)
        
        # Download the asset
        response = requests.get(url, proxies=proxies, stream=True)
        response.raise_for_status()
        
        # Save the asset
        filepath = os.path.join(asset_type_dir, filename)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return filepath
    
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def website_scraping():
    """Website scraping functionality"""
    clear_console()
    print("===== Website Scraping =====\n")
    
    # Get proxy information
    proxy = input("Proxy to use (leave blank for none): ").strip()
    proxies = None
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy
        }
    
    # Get website URL
    website_url = input("Website to scrape: ").strip()
    if not website_url.startswith(('http://', 'https://')):
        website_url = 'https://' + website_url
    
    # Check if we should scrape subpages
    scrape_subpages = input("Get every subpage in the website? (y/n): ").lower() == 'y'
    
    # Check if we should download assets
    download_assets = input("Download all assets (images, audio, video)? (y/n): ").lower() == 'y'
    
    # Create a directory for the website
    domain = urlparse(website_url).netloc
    website_dir = os.path.join(os.getcwd(), "scraped_websites", domain)
    assets_dir = os.path.join(website_dir, "assets")
    os.makedirs(website_dir, exist_ok=True)
    if download_assets:
        os.makedirs(assets_dir, exist_ok=True)
    
    # Set to keep track of visited URLs
    visited_urls = set()
    # Set to keep track of downloaded assets
    downloaded_assets = set()
    
    # Stack for URLs to visit
    urls_to_visit = [website_url]
    
    print(f"\nStarting to scrape {website_url}\n")
    
    while urls_to_visit:
        current_url = urls_to_visit.pop(0)
        
        # Skip if already visited
        if current_url in visited_urls:
            continue
        
        # Add to visited set
        visited_urls.add(current_url)
        
        try:
            print(f"Scraping: {current_url}")
            
            # Send request
            response = requests.get(current_url, proxies=proxies)
            response.raise_for_status()
            
            # Get the content type
            content_type = response.headers.get('Content-Type', '')
            
            # Skip if not HTML
            if 'text/html' not in content_type:
                continue
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Save HTML to file
            url_path = urlparse(current_url).path
            if not url_path or url_path == '/':
                filename = 'index.html'
            else:
                # Replace slashes with underscores and remove trailing slash
                filename = url_path.strip('/').replace('/', '_')
                if '.' not in filename:
                    filename += '.html'
            
            filepath = os.path.join(website_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Download assets if requested
            if download_assets:
                # Download images
                for img in soup.find_all('img'):
                    if (img.get('src')):
                        download_asset(img['src'], current_url, assets_dir, 'images', downloaded_assets, proxies)
                
                # Download scripts
                for script in soup.find_all('script'):
                    if (script.get('src')):
                        download_asset(script['src'], current_url, assets_dir, 'scripts', downloaded_assets, proxies)
                
                # Download stylesheets
                for link in soup.find_all('link', rel='stylesheet'):
                    if (link.get('href')):
                        download_asset(link['href'], current_url, assets_dir, 'styles', downloaded_assets, proxies)
                
                # Download audio/video sources
                for source in soup.find_all('source'):
                    if (source.get('src')):
                        download_asset(source['src'], current_url, assets_dir, 'media', downloaded_assets, proxies)
            
            # Add subpages to the queue if requested
            if scrape_subpages:
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and not href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                        absolute_url = urljoin(current_url, href)
                        
                        # Only add if it's from the same domain
                        if urlparse(absolute_url).netloc == urlparse(website_url).netloc:
                            if absolute_url not in visited_urls and absolute_url not in urls_to_visit:
                                urls_to_visit.append(absolute_url)
        
        except Exception as e:
            print(f"Error scraping {current_url}: {e}")
    
    print(f"\nWebsite scraping complete. Files saved to: {website_dir}")
    input("\nPress Enter to return to the main menu...")

def batch_website_scraping():
    """Batch Website Scraping functionality"""
    clear_console()
    print("===== Batch Website Scraping =====\n")
    
    print("Enter URLs to scrape (one per line)")
    print("Press Enter twice when done\n")
    
    # Collect URLs
    urls = []
    while True:
        url = input("URL: ").strip()
        if not url:
            if urls:  # If we have some URLs already, empty line means we're done
                break
            continue  # If no URLs yet, just skip empty line
        urls.append(url)
    
    if not urls:
        print("\nNo URLs provided.")
        input("\nPress Enter to return to the menu...")
        return
    
    # Get proxy information
    proxy = input("\nProxy to use (leave blank for none): ").strip()
    proxies = None
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy
        }
    
    # Get scraping options
    scrape_subpages = input("Get every subpage for each website? (y/n): ").lower() == 'y'
    download_assets = input("Download all assets (images, audio, video)? (y/n): ").lower() == 'y'
    
    # Process each URL
    print("\nStarting batch scraping...\n")
    for i, website_url in enumerate(urls, 1):
        print(f"\nProcessing URL {i}/{len(urls)}: {website_url}")
        
        # Add https:// if no protocol specified
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
        
        try:
            # Create directory for each website
            domain = urlparse(website_url).netloc
            website_dir = os.path.join(os.getcwd(), "scraped_websites", domain)
            assets_dir = os.path.join(website_dir, "assets")
            os.makedirs(website_dir, exist_ok=True)
            if download_assets:
                os.makedirs(assets_dir, exist_ok=True)
            
            # Initialize tracking sets for this website
            visited_urls = set()
            downloaded_assets = set()
            urls_to_visit = [website_url]
            
            with tqdm(desc=f"Scraping {domain}", unit=" pages") as pbar:
                while urls_to_visit:
                    current_url = urls_to_visit.pop(0)
                    
                    # Skip if already visited
                    if current_url in visited_urls:
                        continue
                    
                    visited_urls.add(current_url)
                    
                    try:
                        response = requests.get(current_url, proxies=proxies)
                        response.raise_for_status()
                        
                        # Process page content
                        if 'text/html' in response.headers.get('Content-Type', ''):
                            soup = BeautifulSoup(response.text, 'html.parser')
                            
                            # Save HTML
                            url_path = urlparse(current_url).path
                            filename = 'index.html' if not url_path or url_path == '/' else url_path.strip('/').replace('/', '_')
                            if '.' not in filename:
                                filename += '.html'
                            
                            filepath = os.path.join(website_dir, filename)
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(response.text)
                            
                            # Download assets if requested
                            if download_assets:
                                # Download images
                                for img in soup.find_all('img'):
                                    if img.get('src'):
                                        download_asset(img['src'], current_url, assets_dir, 'images', downloaded_assets, proxies)
                                
                                # Download scripts, styles, and media
                                for script in soup.find_all('script', src=True):
                                    download_asset(script['src'], current_url, assets_dir, 'scripts', downloaded_assets, proxies)
                                for link in soup.find_all('link', rel='stylesheet'):
                                    if link.get('href'):
                                        download_asset(link['href'], current_url, assets_dir, 'styles', downloaded_assets, proxies)
                                for source in soup.find_all('source'):
                                    if source.get('src'):
                                        download_asset(source['src'], current_url, assets_dir, 'media', downloaded_assets, proxies)
                            
                            # Add subpages if requested
                            if scrape_subpages:
                                for link in soup.find_all('a'):
                                    href = link.get('href')
                                    if href and not href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                                        absolute_url = urljoin(current_url, href)
                                        if (urlparse(absolute_url).netloc == urlparse(website_url).netloc and 
                                            absolute_url not in visited_urls and 
                                            absolute_url not in urls_to_visit):
                                            urls_to_visit.append(absolute_url)
                            
                            pbar.update(1)
                    
                    except Exception as e:
                        print(f"\nError processing {current_url}: {str(e)}")
                        continue
            
            print(f"Completed scraping: {website_url}")
            print(f"Files saved to: {website_dir}")
            
        except Exception as e:
            print(f"\nError processing website {website_url}: {str(e)}")
    
    print("\nBatch scraping completed!")
    input("\nPress Enter to return to the menu...")

def color_settings():
    """Color settings functionality"""
    clear_console()
    print("===== Color Settings =====\n")
    
    global COLORS_ENABLED, GRADIENT_START_COLOR, GRADIENT_END_COLOR
    
    # Display current settings
    print(f"Colors enabled: {'Yes' if COLORS_ENABLED else 'No'}")
    print(f"Gradient start color (RGB): {GRADIENT_START_COLOR}")
    print(f"Gradient end color (RGB): {GRADIENT_END_COLOR}")
    print("\nOptions:")
    print("[1] Toggle colors on/off")
    print("[2] Change gradient start color")
    print("[3] Change gradient end color")
    print("[4] Reset to defaults")
    print("[B] Back to main menu")
    
    choice = input("\nSelect an option: ").upper()
    
    if choice == "1":
        COLORS_ENABLED = not COLORS_ENABLED
        print(f"\nColors are now {'enabled' if COLORS_ENABLED else 'disabled'}")
        input("\nPress Enter to continue...")
        color_settings()
    
    elif choice == "2":
        try:
            print("\nEnter RGB values (0-255) for the start color:")
            r = int(input("Red: "))
            g = int(input("Green: "))
            b = int(input("Blue: "))
            
            # Validate input
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            GRADIENT_START_COLOR = (r, g, b)
            print(f"\nGradient start color set to: {GRADIENT_START_COLOR}")
        except ValueError:
            print("\nInvalid input. Please enter numbers between 0-255.")
        
        input("\nPress Enter to continue...")
        color_settings()
    
    elif choice == "3":
        try:
            print("\nEnter RGB values (0-255) for the end color:")
            r = int(input("Red: "))
            g = int(input("Green: "))
            b = int(input("Blue: "))
            
            # Validate input
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            GRADIENT_END_COLOR = (r, g, b)
            print(f"\nGradient end color set to: {GRADIENT_END_COLOR}")
        except ValueError:
            print("\nInvalid input. Please enter numbers between 0-255.")
        
        input("\nPress Enter to continue...")
        color_settings()
    
    elif choice == "4":
        COLORS_ENABLED = True
        GRADIENT_START_COLOR = (255, 0, 0)    # Red
        GRADIENT_END_COLOR = (255, 200, 0)    # Orange-Yellow
        print("\nColors reset to defaults.")
        input("\nPress Enter to continue...")
        color_settings()
    
    # Any other choice returns to main menu

def ip_inspector():
    """IP Inspector functionality"""
    clear_console()
    print("===== IP Inspector =====\n")
    
    try:
        # Ask user for IP address or use their own
        choice = input("Enter 'M' to check your IP or enter an IP address to inspect: ").strip()
        
        # Construct API URL with all possible fields
        # The masks are defined in the API documentation: https://ip-api.com/docs/api:json
        # 0x100FFFFF includes all possible fields in the latest API version
        api_fields = "status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        
        if choice.upper() == 'M':
            print("\nGetting your current IP information...\n")
            api_url = f"http://ip-api.com/json/?fields={api_fields}"
        else:
            print(f"\nGetting information for {choice}...\n")
            api_url = f"http://ip-api.com/json/{choice}?fields={api_fields}"
        
        # Make the request
        response = requests.get(api_url)
        data = response.json()
        
        if data.get('status') == 'fail':
            print(f"Error: {data.get('message', 'Unknown error')}")
        else:
            # Set table dimensions so that total table width is 56 chars.
            # The format line is: "|" + left.ljust(col1_width) + " | " + right.rjust(col2_width) + "|"
            # Total length = col1_width + col2_width + 5 = 56  → choose col1_width=20, col2_width=31.
            term_width = 56
            col1_width = 20
            col2_width = 31

            def draw_header(title):
                print("+" + "-"*(term_width-2) + "+")
                print("|" + title.center(term_width-2) + "|")
                print("+" + "-"*(term_width-2) + "+")

            def draw_subheader():
                # "Field" is left-aligned; "Info" is right-aligned.
                print("|" + "Field".ljust(col1_width) + " | " + "Info".rjust(col2_width) + "|")
                # The separator line here uses col1_width dashes, a plus, then col2_width+2 dashes.
                print("+" + "-"*(col1_width) + "+" + "-"*(col2_width+2) + "+")
            
            def draw_row(key, value):
                key_str = str(key)
                value_str = str(value) if value is not None else "N/A"
                print("|" + key_str.ljust(col1_width) + " | " + value_str.rjust(col2_width) + "|")
            
            # Example: printing the IP Information table.
            draw_header("IP Information")
            draw_subheader()
            if data.get('query'):
                draw_row("IP Address", data.get('query'))
            if data.get('status'):
                draw_row("Status", data.get('status'))
            print("+" + "-"*(term_width-2) + "+")
            
            # Geographic information section
            draw_header("Geographic Information")
            draw_subheader()
            
            if data.get('continent'):
                draw_row("Continent", f"{data.get('continent')} ({data.get('continentCode', 'N/A')})")
            if data.get('country'):
                draw_row("Country", f"{data.get('country')} ({data.get('countryCode', 'N/A')})")
            if data.get('region'):
                draw_row("Region", f"{data.get('region')} - {data.get('regionName', 'N/A')}")
            if data.get('city'):
                draw_row("City", data.get('city'))
            if data.get('district') and data['district']:
                draw_row("District", data.get('district'))
            if data.get('zip'):
                draw_row("Zip Code", data.get('zip'))
            if 'lat' in data and 'lon' in data:
                draw_row("Coordinates", f"Lat: {data.get('lat')}, Lon: {data.get('lon')}")
                
            # Time and currency information
            draw_header("Time & Currency")
            draw_subheader()
            
            if data.get('timezone'):
                draw_row("Timezone", data.get('timezone'))
            if 'offset' in data:
                draw_row("UTC Offset", f"{data.get('offset')} seconds")
            if data.get('currency'):
                draw_row("Currency", data.get('currency'))
            
            # Network information section
            draw_header("Network Information")
            draw_subheader()
            
            if data.get('isp'):
                draw_row("ISP", data.get('isp'))
            if data.get('org'):
                draw_row("Organization", data.get('org'))
            if data.get('as'):
                draw_row("AS Number", data.get('as'))
            if data.get('asname'):
                draw_row("AS Name", data.get('asname'))
            if data.get('reverse'):
                draw_row("Reverse DNS", data.get('reverse'))
                
            # Security information section
            draw_header("Security Information")
            draw_subheader()
            
            if 'mobile' in data:
                draw_row("Mobile Connection", "Yes" if data.get('mobile') else "No")
            if 'proxy' in data:
                draw_row("Proxy/VPN/Tor", "Yes" if data.get('proxy') else "No")
            if 'hosting' in data:
                draw_row("Hosting Provider", "Yes" if data.get('hosting') else "No")
            
            print("+" + "-"*(term_width-2) + "+")
            
            # Ask if user wants to open location on a map
            if 'lat' in data and 'lon' in data:
                open_map = input("\nDo you want to open this location on a map? (y/n): ").lower()
                if open_map == 'y':
                    # Offer different map providers
                    print("\nChoose a map provider:")
                    print("[1] Google Maps")
                    print("[2] OpenStreetMap")
                    print("[3] Bing Maps")
                    
                    map_choice = input("\nSelect option (default: 1): ").strip() or "1"
                    
                    if map_choice == "1":
                        map_url = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
                    elif map_choice == "2":
                        map_url = f"https://www.openstreetmap.org/?mlat={data['lat']}&mlon={data['lon']}&zoom=12"
                    elif map_choice == "3":
                        map_url = f"https://www.bing.com/maps?cp={data['lat']}~{data['lon']}&lvl=12"
                    else:
                        map_url = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
                        
                    print(f"\nOpening map: {map_url}")
                    webbrowser.open(map_url)
            
            # Ask if user wants to perform additional lookups
            additional_lookup = input("\nDo you want to perform additional lookups on this IP? (y/n): ").lower()
            if additional_lookup == 'y':
                print("\nChoose a lookup service:")
                print("[1] VirusTotal IP reputation")
                print("[2] AbuseIPDB check")
                print("[3] Shodan scan results")
                print("[4] Threat Intelligence lookup")
                
                lookup_choice = input("\nSelect option (default: 1): ").strip() or "1"
                
                ip_address = data.get('query', choice)
                if lookup_choice == "1":
                    vt_url = f"https://www.virustotal.com/gui/ip-address/{ip_address}/detection"
                    webbrowser.open(vt_url)
                elif lookup_choice == "2":
                    abuseipdb_url = f"https://www.abuseipdb.com/check/{ip_address}"
                    webbrowser.open(abuseipdb_url)
                elif lookup_choice == "3":
                    shodan_url = f"https://www.shodan.io/host/{ip_address}"
                    webbrowser.open(shodan_url)
                elif lookup_choice == "4":
                    threatint_url = f"https://threatintelligenceplatform.com/report/{ip_address}"
                    webbrowser.open(threatint_url)
            
            # Ask if user wants to save the IP information to a file
            save_info = input("\nDo you want to save this information to a file? (y/n): ").lower()
            if save_info == 'y':
                # Create directory if it doesn't exist
                ip_dir = os.path.join(os.getcwd(), "ip_logs")
                os.makedirs(ip_dir, exist_ok=True)
                
                # Offer different file formats
                print("\nChoose a file format:")
                print("[1] JSON (all raw data)")
                print("[2] Text (formatted table)")
                print("[3] CSV (comma separated values)")
                
                format_choice = input("\nSelect format (default: 1): ").strip() or "1"
                
                # Generate filename with IP and timestamp
                ip_address = data.get('query', 'unknown')
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                
                if format_choice == "1":  # JSON
                    filename = f"ip_{ip_address}_{timestamp}.json"
                    filepath = os.path.join(ip_dir, filename)
                    
                    with open(filepath, 'w') as f:
                        json.dump(data, f, indent=2)
                
                elif format_choice == "2":  # Text
                    filename = f"ip_{ip_address}_{timestamp}.txt"
                    filepath = os.path.join(ip_dir, filename)
                    
                    with open(filepath, 'w') as f:
                        f.write(f"IP Information for {ip_address}\n")
                        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        
                        f.write("Basic Information:\n")
                        f.write(f"IP Address: {data.get('query', 'N/A')}\n")
                        f.write(f"Status: {data.get('status', 'N/A')}\n\n")
                        
                        f.write("Geographic Information:\n")
                        if data.get('continent'):
                            f.write(f"Continent: {data.get('continent')} ({data.get('continentCode', 'N/A')})\n")
                        if data.get('country'):
                            f.write(f"Country: {data.get('country')} ({data.get('countryCode', 'N/A')})\n")
                        if data.get('region'):
                            f.write(f"Region: {data.get('region')} - {data.get('regionName', 'N/A')}\n")
                        if data.get('city'):
                            f.write(f"City: {data.get('city')}\n")
                        if data.get('district') and data['district']:
                            f.write(f"District: {data.get('district')}\n")
                        if data.get('zip'):
                            f.write(f"Zip Code: {data.get('zip')}\n")
                        if 'lat' in data and 'lon' in data:
                            f.write(f"Coordinates: Lat: {data.get('lat')}, Lon: {data.get('lon')}\n\n")
                        
                        f.write("Time & Currency:\n")
                        if data.get('timezone'):
                            f.write(f"Timezone: {data.get('timezone')}\n")
                        if 'offset' in data:
                            f.write(f"UTC Offset: {data.get('offset')} seconds\n")
                        if data.get('currency'):
                            f.write(f"Currency: {data.get('currency')}\n\n")
                        
                        f.write("Network Information:\n")
                        if data.get('isp'):
                            f.write(f"ISP: {data.get('isp')}\n")
                        if data.get('org'):
                            f.write(f"Organization: {data.get('org')}\n")
                        if data.get('as'):
                            f.write(f"AS Number: {data.get('as')}\n")
                        if data.get('asname'):
                            f.write(f"AS Name: {data.get('asname')}\n")
                        if data.get('reverse'):
                            f.write(f"Reverse DNS: {data.get('reverse')}\n\n")
                        
                        f.write("Security Information:\n")
                        if 'mobile' in data:
                            f.write(f"Mobile Connection: {'Yes' if data.get('mobile') else 'No'}\n")
                        if 'proxy' in data:
                            f.write(f"Proxy/VPN/Tor: {'Yes' if data.get('proxy') else 'No'}\n")
                        if 'hosting' in data:
                            f.write(f"Hosting Provider: {'Yes' if data.get('hosting') else 'No'}\n")
                
                elif format_choice == "3":  # CSV
                    filename = f"ip_{ip_address}_{timestamp}.csv"
                    filepath = os.path.join(ip_dir, filename)
                    
                    with open(filepath, 'w') as f:
                        # Write header
                        f.write("Field,Value\n")
                        
                        # Write all key-value pairs
                        for key, value in data.items():
                            f.write(f"{key},{value}\n")
                
                print(f"\nInformation saved to: {filepath}")
    
    except Exception as e:
        print(f"Error retrieving IP information: {str(e)}")
        print("Try again later or check your internet connection.")
    
    input("\nPress Enter to return to the main menu...")

@check_windows_requirement
def activate_windows():
    """Windows Activation functionality"""
    if not is_admin():
        print("This feature requires admin privileges.")
        print("Please use [A] to enable admin privileges.")
        input("\nPress Enter to return to the menu...")
        return
    
    if os.name != 'nt':
        clear_console()
        print("===== Windows Activation =====\n")
        print("WARNING: Windows activation commands are designed for Windows operating systems.")
        print("Your current operating system is not Windows.")
        print("The commands may not work as expected or could cause errors.\n")
        choice = input("Do you want to continue anyway? (y/n): ").lower()
        if choice != 'y':
            return
    
    clear_console()
    print("===== Windows Activation =====\n")
    print("WARNING: This feature will attempt to activate Windows using an online activation script.")
    print("This should only be used if you have a valid license or for testing purposes.")
    print("The script will run: 'irm https://get.activated.win | iex' via PowerShell.\n")
    
    choice = input("Do you want to proceed with Windows activation? (y/n): ").lower()
    
    if choice != 'y':
        print("\nActivation canceled.")
        input("\nPress Enter to return to the main menu...")
        return
    
    try:
        print("\nLaunching Windows Activation script...")
        
        # Construct the PowerShell command
        ps_command = 'powershell.exe -Command "irm https://get.activated.win | iex"'
        
        # Run the PowerShell command
        subprocess.run(ps_command, shell=True)
        
        print("\nActivation process completed.")
    
    except Exception as e:
        print(f"\nError during activation: {str(e)}")
        print("Make sure PowerShell is available and you have the necessary permissions.")
    
    input("\nPress Enter to return to the main menu...")

@check_windows_requirement
def delete_temp_files():
    """Delete Temporary Files functionality"""
    if os.name != 'nt':
        clear_console()
        print("===== Delete Temporary Files =====\n")
        print("WARNING: This temporary file deletion feature is optimized for Windows.")
        print("Your current operating system is not Windows.")
        print("The feature may not work correctly, or might delete files from unexpected locations.\n")
        choice = input("Do you want to continue anyway? (y/n): ").lower()
        if choice != 'y':
            return
        
        # For non-Windows systems, use appropriate temp directory
        temp_folder = os.environ.get('TMPDIR') or os.environ.get('TMP') or '/tmp'
    else:
        # For Windows, use the standard TEMP environment variable
        temp_folder = os.environ.get('TEMP')
    
    clear_console()
    print("===== Delete Temporary Files =====\n")
    print("This will delete temporary files from your system to free up disk space.")
    print(f"Target directory: {temp_folder}")
    print("WARNING: This operation cannot be undone!\n")
    
    choice = input("Do you want to proceed with deleting temporary files? (y/n): ").lower()
    
    if choice != 'y':
        print("\nOperation canceled.")
        input("\nPress Enter to return to the main menu...")
        return
    
    try:
        if not temp_folder or not os.path.exists(temp_folder):
            print("\nCould not locate temporary folder.")
            input("\nPress Enter to return to the main menu...")
            return
        
        print(f"\nDeleting files from: {temp_folder}")
        
        # Count files before deletion
        total_files = sum([len(files) for _, _, files in os.walk(temp_folder)])
        print(f"Found {total_files} files to process.")
        
        # Set up progress bar
        with tqdm(total=total_files, unit='files') as pbar:
            deleted_count = 0
            error_count = 0
            
            # Iterate through all files in temp directory
            for root, dirs, files in os.walk(temp_folder):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                            deleted_count += 1
                    except Exception:
                        error_count += 1
                    finally:
                        pbar.update(1)
        
        print(f"\nOperation completed: {deleted_count} files deleted, {error_count} files skipped due to errors.")
        
        # Try to remove empty directories
        for root, dirs, files in os.walk(temp_folder, topdown=False):
            for dir in dirs:
                try:
                    dir_path = os.path.join(root, dir)
                    if not os.listdir(dir_path):  # Check if directory is empty
                        os.rmdir(dir_path)
                except:
                    pass
        
    except Exception as e:
        print(f"\nError during operation: {str(e)}")
    
    input("\nPress Enter to return to the main menu...")

def system_info():
    """System Information Viewer functionality"""
    clear_console()
    print("===== System Information =====\n")
    
    def get_size(bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
    
    # System Information
    print("System Information:")
    print("-" * 50)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    
    # CPU Information
    print("\nCPU Information:")
    print("-" * 50)
    print(f"Physical cores: {psutil.cpu_count(logical=False)}")
    print(f"Total cores: {psutil.cpu_count(logical=True)}")
    cpu_freq = psutil.cpu_freq()
    if cpu_freq:
        print(f"Max Frequency: {cpu_freq.max:.2f}Mhz")
        print(f"Min Frequency: {cpu_freq.min:.2f}Mhz")
        print(f"Current Frequency: {cpu_freq.current:.2f}Mhz")
    print(f"CPU Usage: {psutil.cpu_percent()}%")
    
    # Memory Information
    print("\nMemory Information:")
    print("-" * 50)
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    
    # Disk Information
    print("\nDisk Information:")
    print("-" * 50)
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            print(f"\nDevice: {partition.device}")
            print(f"Mountpoint: {partition.mountpoint}")
            print(f"File system type: {partition.fstype}")
            print(f"Total Size: {get_size(partition_usage.total)}")
            print(f"Used: {get_size(partition_usage.used)}")
            print(f"Free: {get_size(partition_usage.free)}")
            print(f"Percentage: {partition_usage.percent}%")
        except Exception as e:
            print(f"Error reading partition {partition.device}: {e}")
    
    input("\nPress Enter to return to the main menu...")

def network_tools():
    """Network Tools functionality"""
    while True:
        clear_console()
        print("===== Network Tools =====\n")
        print("[1] Port Scanner")
        print("[2] DNS Lookup")
        print("[3] Network Speed Test")
        print("[4] IP Inspector")
        print("[5] Ping Tool")
        print("[6] Traceroute")
        print("[B] Back to main menu")
        
        choice = input("\nSelect a tool: ").upper()
        
        if choice == "B":
            break
        elif choice == "1":
            port_scanner()
        elif choice == "2":
            dns_lookup()
        elif choice == "3":
            speed_test()
        elif choice == "4":
            ip_inspector()
        elif choice == "5":
            ping_tool()
        elif choice == "6":
            traceroute()

def port_scanner():
    """Port Scanner functionality"""
    clear_console()
    print("===== Port Scanner =====\n")
    
    target = input("Enter target IP or hostname: ")
    start_port = int(input("Enter start port (default 1): ") or 1)
    end_port = int(input("Enter end port (default 1024): ") or 1024)
    
    print(f"\nScanning {target} from port {start_port} to {end_port}...")
    
    try:
        target_ip = socket.gethostbyname(target)
        print(f"IP Address: {target_ip}\n")
        
        with tqdm(total=end_port - start_port + 1, unit='port') as pbar:
            for port in range(start_port, end_port + 1):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target_ip, port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    print(f"Port {port}: Open ({service})")
                sock.close()
                pbar.update(1)
    
    except socket.gaierror:
        print("Hostname could not be resolved")
    except socket.error:
        print("Could not connect to server")
    
    input("\nPress Enter to return to Network Tools...")

def dns_lookup():
    """DNS Lookup functionality"""
    clear_console()
    print("===== DNS Lookup =====\n")
    
    domain = input("Enter domain name: ")
    
    try:
        print("\nLooking up DNS records...\n")
        
        # A Record
        print("A Records:")
        try:
            answers = dns.resolver.resolve(domain, 'A')
            for rdata in answers:
                print(f"  {rdata.address}")
        except:
            print("  No A records found")
        
        # AAAA Record
        print("\nAAAA Records:")
        try:
            answers = dns.resolver.resolve(domain, 'AAAA')
            for rdata in answers:
                print(f"  {rdata.address}")
        except:
            print("  No AAAA records found")
        
        # MX Record
        print("\nMX Records:")
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            for rdata in answers:
                print(f"  {rdata.exchange} (priority: {rdata.preference})")
        except:
            print("  No MX records found")
        
        # NS Record
        print("\nNS Records:")
        try:
            answers = dns.resolver.resolve(domain, 'NS')
            for rdata in answers:
                print(f"  {rdata.target}")
        except:
            print("  No NS records found")
        
        # TXT Record
        print("\nTXT Records:")
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            for rdata in answers:
                print(f"  {rdata.strings}")
        except:
            print("  No TXT records found")
        
    except Exception as e:
        print(f"Error performing DNS lookup: {str(e)}")
    
    input("\nPress Enter to return to Network Tools...")

def speed_test():
    """Network Speed Test functionality"""
    clear_console()
    print("===== Network Speed Test =====\n")
    
    print("Testing network speed (this may take a minute)...")
    
    try:
        st = speedtest.Speedtest()
        
        print("\nFinding best server...")
        st.get_best_server()
        
        print("Testing download speed...")
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        print("Testing upload speed...")
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        
        print("Testing ping...")
        ping = st.results.ping
        
        print("\nResults:")
        print(f"Download Speed: {download_speed:.2f} Mbps")
        print(f"Upload Speed: {upload_speed:.2f} Mbps")
        print(f"Ping: {ping:.2f} ms")
        
    except Exception as e:
        print(f"Error during speed test: {str(e)}")
    
    input("\nPress Enter to return to Network Tools...")

def ping_tool():
    """Ping Tool functionality"""
    clear_console()
    print("===== Ping Tool =====\n")
    
    host = input("Enter hostname or IP to ping: ")
    count = int(input("Enter number of pings (default 4): ") or "4")
    
    def create_packet():
        """Create a new echo request packet"""
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        my_checksum = 0
        my_id = os.getpid() & 0xFFFF
        header = struct.pack('!BBHHH', 8, 0, my_checksum, my_id, 1)
        data = struct.pack('!Q', time.time_ns())  # 8 bytes of time data
        my_checksum = calculate_checksum(header + data)
        header = struct.pack('!BBHHH', 8, 0, my_checksum, my_id, 1)
        return header + data
    
    def calculate_checksum(data):
        """Calculate the checksum of the packet"""
        if len(data) % 2 == 1:
            data += b'\0'
        words = struct.unpack('!%dH' % (len(data) // 2), data)
        checksum = sum(words)
        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum += checksum >> 16
        return ~checksum & 0xffff
    
    try:
        ip = socket.gethostbyname(host)
        print(f"\nPinging {host} [{ip}] with 32 bytes of data:\n")
        
        successful = 0
        failed = 0
        times = []
        
        # Create raw socket
        try:
            if os.name == 'nt':  # Windows requires admin privileges for raw sockets
                raise Exception("Windows requires admin privileges for raw sockets")
                
            with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
                for i in range(count):
                    try:
                        packet = create_packet()
                        sock.sendto(packet, (ip, 0))
                        start_time = time.time()
                        
                        # Wait for response with timeout
                        ready = select.select([sock], [], [], 2)
                        if ready[0]:  # Data received
                            data, addr = sock.recvfrom(1024)
                            end_time = time.time()
                            duration = (end_time - start_time) * 1000  # Convert to ms
                            
                            icmp_header = data[20:28]
                            type, code, checksum, p_id, sequence = struct.unpack('!BBHHH', icmp_header)
                            
                            if type == 0:  # ICMP Echo Reply
                                print(f"Reply from {ip}: bytes=32 time={duration:.0f}ms")
                                successful += 1
                                times.append(duration)
                            else:
                                print(f"Error: Received ICMP type {type}, code {code}")
                                failed += 1
                        else:
                            print("Request timed out")
                            failed += 1
                            
                        if i < count - 1:
                            time.sleep(1)  # Wait between pings
                            
                    except Exception as e:
                        print(f"Error: {str(e)}")
                        failed += 1
                        
        except Exception:
            # Fallback to TCP connection test
            print("Falling back to TCP connection test...")
            for i in range(count):
                try:
                    start_time = time.time()
                    
                    # Try common ports
                    for port in [80, 443, 22, 21]:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(2)
                        
                        if sock.connect_ex((ip, port)) == 0:
                            end_time = time.time()
                            duration = (end_time - start_time) * 1000
                            print(f"Reply from {ip}: time={duration:.0f}ms (TCP port {port})")
                            successful += 1
                            times.append(duration)
                            sock.close()
                            break
                    else:
                        print("Request timed out")
                        failed += 1
                    
                    time.sleep(1)  # Wait between attempts
                    
                except Exception as e:
                    print(f"Request timed out")
                    failed += 1
        
        # Print statistics
        if count > 0:
            print(f"\nPing statistics for {ip}:")
            print(f"    Packets: Sent = {count}, Received = {successful}, Lost = {failed} ({(failed/count)*100:.0f}% loss)")
            if times:
                print(f"Approximate round trip times in milli-seconds:")
                print(f"    Minimum = {min(times):.0f}ms, Maximum = {max(times):.0f}ms, Average = {sum(times)/len(times):.0f}ms")
    
    except socket.gaierror:
        print(f"Could not resolve hostname {host}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    input("\nPress Enter to return to Network Tools...")

def traceroute():
    """Traceroute functionality"""
    clear_console()
    print("===== Traceroute =====\n")
    
    host = input("Enter hostname or IP to trace: ")
    
    try:
        if os.name == 'nt':  # Windows
            command = f"tracert {host}"
        else:  # Linux/Unix
            command = f"traceroute {host}"
        
        print(f"\nTracing route to {host}...\n")
        subprocess.run(command, shell=True)
        
    except Exception as e:
        print(f"Error during traceroute: {str(e)}")
    
    input("\nPress Enter to return to Network Tools...")

def is_windows():
    """Check if running on Windows"""
    return os.name == 'nt'

def is_admin():
    """Check if the program has admin privileges"""
    try:
        if is_windows():
            return ctypes.windll.shell32.IsUserAnAdmin()
        return False
    except:
        return False

def request_admin():
    """Request admin privileges on Windows"""
    if is_windows() and not is_admin():
        try:
            # Re-run the program with admin rights using PowerShell
            # This method provides a better UAC experience
            admin_cmd = f'powershell.exe -Command "Start-Process -Verb RunAs \'{sys.executable}\' \'{" ".join(sys.argv)}\'"'
            subprocess.run(admin_cmd, shell=True)
            sys.exit()
        except Exception as e:
            print(f"Error requesting admin privileges: {e}")
            input("\nPress Enter to continue...")
    else:
        print("This feature requires Windows and admin privileges.")
        input("\nPress Enter to continue...")

def showMainOptionsAndBanner(ignoreOptions):
    version = "0.1.0"
    
    # Banner text as a list of lines
    banner_lines = [
        "    ____           _                                                ",
        "   / __ \\___  _  _( )_____  Version " + version + "                                        ",
        "  / / / / _ \\| |/_/// ___/_  ___      ____  _ __              __    ",
        " / /_/ /  __/>  <  (__  )  |/  /_  __/ / /_(_) /_____  ____  / /____",
        "/_____/\\___/_/|_| /____/ /|_/ / / / / / __/ / __/ __ \\/ __ \\/ / ___/",
        "                      / /  / / /_/ / / /_/ / /_/ /_/ / /_/ / (__  ) ",
        "                     /_/  /_/\\__,_/_/\\__/_/\\__/\\____/\\____/_/____/  ",
        "                                                                    "
    ]
    
    # Print banner
    for line in banner_lines:
        print(line)
    
    # Show Windows and admin status
    if is_windows():
        admin_status = "Admin" if is_admin() else "User"
        windows_version = platform.platform()
        print(f"\nWindows Version: {windows_version}")
        print(f"Running as: {admin_status}")
        if not is_admin():
            print("[A] Enable Admin Privileges (Required for some features)")
    else:
        print("\nWarning: This tool is designed for Windows.")
        print("Some features may not work on your system.")
    
    print()  # Extra line after banner
    
    if ignoreOptions:
        return
    
    # Show different menu based on whether we're in main menu or submenu
    if current_submenu is None:
        # We're in the main menu - show page indicator and page options
        total_pages = len(MENU_OPTIONS)
        print(f"Page {current_menu_page + 1}/{total_pages}")
        print()
        
        # Display options for the current page
        current_options = MENU_OPTIONS[current_menu_page]
        for key, option in current_options.items():
            has_suboptions = "suboptions" in option and option["suboptions"]
            windows_only = option.get("windows_only", False)
            submenu_indicator = "►" if has_suboptions else " "
            text = f"[{key}] {option['name']} {submenu_indicator}"
            if windows_only and not is_windows():
                # Pre-color using the unavailable gradient and print using original_print
                colored_text = gradient_text(text, start_color=UNAVAILABLE_GRADIENT_START, end_color=UNAVAILABLE_GRADIENT_END)
                original_print(f"    {colored_text}")
            else:
                print(f"    {text}")
        
        # Display navigation options
        print()
        if current_menu_page > 0:  # If not on the first page
            print("    [<] Previous page")
        if current_menu_page < total_pages - 1:  # If not on the last page
            print("    [>] Next page")
    else:
        # We're in a submenu - show the submenu options
        parent_option = MENU_OPTIONS[current_menu_page][current_submenu]
        print(f"===== {parent_option['name']} Suboptions =====")
        print()
        
        for key, suboption in parent_option["suboptions"].items():
            windows_only = suboption.get("windows_only", False)
            text = f"[{key}] {suboption['name']}"
            if windows_only and not is_windows():
                colored_text = gradient_text(text, start_color=UNAVAILABLE_GRADIENT_START, end_color=UNAVAILABLE_GRADIENT_END)
                original_print(f"    {colored_text}")
            else:
                print(f"    {text}")
        print("\n    [B] Back to main menu")
    
    print()
    print("    [X] Exit")
    print()

def isMenuNavigationOption(option):
    """Check if the option is for menu navigation"""
    if option == 'B' and current_submenu is not None:
        return True
    if option == '<' and current_menu_page > 0 and current_submenu is None:
        return True
    if option == '>' and current_menu_page < len(MENU_OPTIONS) - 1 and current_submenu is None:
        return True
    return False

def handleMenuNavigation(option):
    """Handle menu navigation options"""
    global current_menu_page, current_submenu
    if option == 'B':
        current_submenu = None
    elif option == '<':
        current_menu_page = max(0, current_menu_page - 1)
    elif option == '>':
        current_menu_page = min(len(MENU_OPTIONS) - 1, current_menu_page + 1)

def runOption(option):
    """Run the selected option based on user input."""
    global current_submenu

    # Check if this is a menu navigation option
    if isMenuNavigationOption(option):
        handleMenuNavigation(option)
        return

    # If in main menu, get the selected option object
    if current_submenu is None:
        current_page_options = MENU_OPTIONS[current_menu_page]
        if option not in current_page_options:
            clear_console()
            print(f"Option '{option}' is not available on the current page.")
            input("\nPress Enter to return to the main menu...")
            return
        
        selected_option = current_page_options[option]
        # If option is Windows-only and user is not on Windows, disallow selection.
        if selected_option.get("windows_only", False) and not is_windows():
            clear_console()
            print("This option is only available on Windows. Press Enter to return to the main menu.")
            input()
            return

        # Check if the option has suboptions
        if "suboptions" in selected_option and selected_option["suboptions"]:
            current_submenu = option
        else:
            # Execute the function
            selected_option["function"]()
    else:
        # In a submenu, check the selected suboption.
        parent_option = MENU_OPTIONS[current_menu_page][current_submenu]
        if option not in parent_option["suboptions"]:
            clear_console()
            print(f"Option '{option}' is not available in the current submenu.")
            input("\nPress Enter to return to the submenu...")
            return
        selected_suboption = parent_option["suboptions"][option]
        if selected_suboption.get("windows_only", False) and not is_windows():
            clear_console()
            print("This suboption is only available on Windows. Press Enter to return to the submenu.")
            input()
            return
        selected_suboption["function"]()

# Update the menu structure to indicate Windows-only features
MENU_OPTIONS = [
    {
        "S": {
            "name": "System Information",
            "description": "View detailed system information",
            "function": lambda: system_info(),  # Use lambda to avoid forward reference
            "windows_only": False
        },
        "N": {
            "name": "Network Tools",
            "description": "Network utilities and diagnostics",
            "function": lambda: network_tools(),
            "windows_only": False
        },
        "R": {
            "name": "Registry Tweaks (Windows)",
            "description": "Modify Windows registry settings",
            "function": lambda: registry_tweaks(),
            "windows_only": True,
            "suboptions": {
                "R1": {"name": "Basic Registry Tweaks", "description": "Common Windows registry tweaks", "function": lambda: registry_tweaks()},
                "R2": {"name": "Advanced Registry Tweaks", "description": "Advanced system modifications", "function": lambda: advanced_registry_tweaks()},
                "R3": {"name": "Registry Browser", "description": "Browse and edit registry directly", "function": lambda: placeholder_feature("Registry Browser")}
            }
        },
        "W": {
            "name": "Website Scraping",
            "description": "Download content from websites",
            "function": lambda: website_scraping(),
            "windows_only": False,
            "suboptions": {
                "W1": {"name": "Single Website Scraping", "description": "Scrape a single website", "function": lambda: website_scraping()},
                "W2": {"name": "Batch Website Scraping", "description": "Scrape multiple websites from a list", "function": lambda: batch_website_scraping()}
            }
        },
        "Y": {
            "name": "YT Video Downloader",
            "description": "Download YouTube videos",
            "function": lambda: youtube_downloader(),
            "windows_only": False
        }  # <-- new option
    },
    {
        "T": {
            "name": "Delete Temporary Files (Windows)",
            "description": "Clean temporary files from your system",
            "function": lambda: delete_temp_files(),
            "windows_only": True
        },
        "V": {
            "name": "Activate Windows",
            "description": "Activate Windows using various methods",
            "function": lambda: activate_windows(),
            "windows_only": True
        },
        "C": {
            "name": "Color Settings",
            "description": "Customize the colors used in the application",
            "function": lambda: color_settings(),
            "windows_only": False
        }
    }
]

COLORS_ENABLED = True                 # Set to False to disable all colors

# Define ANSI color codes and styles
STYLE_GRAY = "\033[90m"    # Bright black (gray)
STYLE_RESET = "\033[0m"    # Reset all styles

def youtube_downloader():
    clear_console()
    print("===== YouTube Video Downloader =====\n")
    video_url = input("Enter YouTube video URL: ")
    try:
        yt = YouTube(video_url)
    except Exception as e:
        print(f"Error creating YouTube instance with pytube: {e}")
        choice = input("Use alternative downloader (yt_dlp) instead? (y/n): ").lower()
        if choice == "y":
            youtube_downloader_ydl()
        else:
            input("\nPress Enter to return to the main menu...")
        return

    # Attempt to fetch video details separately.
    try:
        title = yt.title
        description = yt.description
        if description is None:
            description = "Unknown Desc"
    except Exception as e:
        print(f"Error accessing video details with pytube: {e}")
        choice = input("Use alternative downloader (yt_dlp) instead? (y/n): ").lower()
        if choice == "y":
            youtube_downloader_ydl()
        else:
            input("\nPress Enter to return to the main menu...")
        return

    print(f"\nTitle: {title}")
    print(f"Description: {description[:500]}")
    confirm = input("\nIs this the correct video? (y/n): ").lower()
    if confirm != "y":
        print("Operation cancelled.")
        input("\nPress Enter to return to the main menu...")
        return

    print("\nSelect download type:")
    print("[1] MP4 with Audio (Progressive)")
    print("[2] Only Video (MP4, adaptive)")
    print("[3] Only Audio")
    dtype = input("Select an option: ").strip()
    download_folder = os.path.join(os.getcwd(), "yt_downloads")
    os.makedirs(download_folder, exist_ok=True)

    if dtype in ["1", "2"]:
        if dtype == "1":
            streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc()
        else:
            streams = yt.streams.filter(only_video=True, file_extension="mp4").order_by('resolution').desc()
        if not streams:
            print("No stream found for selected type.")
            input("Press Enter to return...")
            return
        qualities = sorted({s.resolution for s in streams if s.resolution},
                           key=lambda x: int(x.rstrip('p')), reverse=True)
        print("\nAvailable qualities:")
        for q in qualities:
            print(f"- {q}")
        qual = input("Enter desired quality from the list (e.g., 1080p, 720p): ").strip()
        filtered = streams.filter(res=qual)
        if not filtered:
            print(f"No stream available at {qual}.")
            input("Press Enter to return...")
            return
        print(f"\nAvailable streams for quality {qual}:")
        for idx, s in enumerate(filtered, start=1):
            print(f"[{idx}] Resolution: {s.resolution}, FPS: {s.fps}")
        opt = int(input("Select stream number: "))
        selected = filtered[opt - 1]
    elif dtype == "3":
        streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
        if not streams:
            print("No audio stream found.")
            input("Press Enter to return...")
            return
        print("\nAvailable audio streams:")
        for idx, s in enumerate(streams, start=1):
            print(f"[{idx}] Bitrate: {s.abr}")
        opt = int(input("Select stream number: "))
        selected = streams[opt - 1]
    else:
        print("Invalid option.")
        input("Press Enter to return...")
        return

    print("Downloading...")
    try:
        selected.download(output_path=download_folder)
        print("Download complete!")
    except urllib.error.HTTPError as e:
        print(f"Download failed due to HTTP Error: {e}")
        print("Attempting to extract direct download URL...")
        try:
            url = yt.streams.filter(progressive=True, file_extension="mp4").first().url
            print(f"Direct download URL: {url}")
            print("Please use this URL with a download manager to download the video.")
        except Exception as ex:
            print(f"Failed to extract direct download URL: {ex}")
    except Exception as e:
        print(f"Error during download: {e}")
    input("\nPress Enter to return to the main menu...")

def youtube_downloader_ydl():
    clear_console()
    print("===== Alternative YouTube Video Downloader (yt_dlp) =====\n")
    video_url = input("Enter YouTube video URL: ")
    download_folder = os.path.join(os.getcwd(), "yt_downloads")
    os.makedirs(download_folder, exist_ok=True)
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlp is not installed. Please install it with: pip install yt-dlp")
        input("Press Enter to return...")
        return
    ydl_opts = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
        except Exception as e:
            err_msg = str(e)
            if "Sign in" in err_msg:
                print("It appears YouTube requires confirmation that you're not a bot.")
                use_cookies = input("Would you like to provide a cookies file path? (y/n): ").lower()
                if use_cookies == 'y':
                    cookies_path = input("Enter path to your cookies file: ").strip()
                    ydl_opts["cookiefile"] = cookies_path
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
                        try:
                            info = ydl2.extract_info(video_url, download=False)
                        except Exception as e2:
                            print(f"Failed again: {e2}")
                            input("Press Enter to return...")
                            return
                else:
                    print("Cannot retrieve video info without cookies.")
                    input("Press Enter to return...")
                    return
            else:
                print(f"Failed to retrieve video info: {e}")
                input("Press Enter to return...")
                return
    print(f"\nTitle: {info.get('title')}")
    desc = info.get('description') or ""
    print(f"Description: {desc[:500]}")
    confirm = input("\nIs this the correct video? (y/n): ").lower()
    if confirm != 'y':
        print("Operation cancelled.")
        input("Press Enter to return...")
        return

    # List available qualities based on format_note information.
    formats = info.get('formats', [])
    quality_set = {fmt.get('format_note') for fmt in formats if fmt.get('format_note')}
    qualities = sorted(list(quality_set))
    print("\nAvailable qualities:")
    for q in qualities:
        print(f"- {q}")
    desired_quality = input("Enter desired quality from the list: ").strip()
    chosen_fmt = None
    for fmt in formats:
        if desired_quality in (fmt.get('format_note') or ""):
            chosen_fmt = fmt
            break
    if not chosen_fmt:
        print(f"No format found for quality {desired_quality}.")
        input("Press Enter to return...")
        return
    ydl_opts_dl = {'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s')}
    print("Downloading using alternative downloader...")
    with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
        try:
            ydl.download([video_url])
        except Exception as e:
            print(f"Error during download: {e}")
            input("Press Enter to return...")
            return
    print("Download complete!")
    input("Press Enter to return to the main menu...")

# Main program loop
if __name__ == "__main__":
    while True:
        clear_console()
        showMainOptionsAndBanner(False)
        option = input("Select an option: ").upper()
        
        # Exit option
        if option == 'X':
            clear_console()
            print("Exiting the program...")
            break
        # Call runOption for all other options
        else:
            runOption(option)
