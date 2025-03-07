import os
import sys
import time
import subprocess
import inquirer
import time

def printheader(text):
    print(f"=== {text} ===")


choices = [
    "Web Scraping",
    "Windows Tweaks",
    "Weather Forecast",
    "Exit"
]
windowstweaks = [
    "Compact OS Mode",
    "Clean Temporary Files",
    "Edge Browser",
    "Search indexing",
    "Verbose Messages",
    "Recommended apps/start menu"
]

def placeholder():
    print("This is a unfinished feature.")

banner = rf"""

██████╗ ███████╗██╗  ██╗███████╗                                                                                    
██╔══██╗██╔════╝╚██╗██╔╝██╔════╝                                                                                    
██║  ██║█████╗   ╚███╔╝ ███████╗                                                                                    
██║  ██║██╔══╝   ██╔██╗ ╚════██║                                                                                    
██████╔╝███████╗██╔╝ ██╗███████║                                                                                    
╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝                                                                                    
                            ███╗   ███╗██╗   ██╗██╗  ████████╗██╗████████╗ ██████╗  ██████╗ ██╗     ███████╗        
                            ████╗ ████║██║   ██║██║  ╚══██╔══╝██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝        
                            ██╔████╔██║██║   ██║██║     ██║   ██║   ██║   ██║   ██║██║   ██║██║     ███████╗        
                            ██║╚██╔╝██║██║   ██║██║     ██║   ██║   ██║   ██║   ██║██║   ██║██║     ╚════██║        
                            ██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║   ██║   ╚██████╔╝╚██████╔╝███████╗███████║███████╗
                            ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝
                                                                                                                    

"""

def run(option):
    if option == "Web Scraping":
        option = inquirer.list_input("This will run a .rb file in the utils directory. Are you sure?", choices=["Yes", "No/Exit"])
        if option == "No/Exit":
            print("Exiting...")
            time.sleep(1)
            return
        if option == "Yes":
            url = input("Enter a URL to scrape: ")
            script_path = os.path.join(os.path.dirname(__file__), "utils", "web-scraping.rb")
            try:
                # Execute Ruby script and display output in real-time
                process = subprocess.Popen(
                    ["ruby", script_path, "--url", url],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Stream output in real-time
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(output.strip())
                        
                # Check return code
                return_code = process.poll()
                if return_code != 0:
                    print("Ruby script exited with error code:", return_code)
                    for line in process.stderr.readlines():
                        print(line.strip())
            except Exception as e:
                print(f"Error executing Ruby script: {e}")

        os.system("cls" if os.name == "nt" else "clear")
        print("=== YouTube Video Downloader ===")
        url = input("Enter YouTube URL: ")
        format_choice = inquirer.list_input("Choose format to download:", choices=["mp4", "mp3"])
        
        # Get the default downloads folder
        if os.name == "nt":  # Windows
            download_path = os.path.join(os.environ["USERPROFILE"], "Downloads")
        else:  # Unix-based systems
            download_path = os.path.join(os.environ["HOME"], "Downloads")
        
        # Ask if user wants to use default download location
        use_default = inquirer.list_input(f"Save to default downloads folder ({download_path})?", 
                                         choices=["Yes", "No"])
        
        if use_default == "No":
            custom_path = input("Enter full path to save downloads: ")
            if os.path.exists(custom_path) and os.path.isdir(custom_path):
                download_path = custom_path
            else:
                print(f"Invalid path. Using default: {download_path}")
        
        print(f"Downloading {url} in {format_choice} format to {download_path}...")
        
        # Check if Node.js is installed
        try:
            subprocess.run(["node", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            print("Error: Node.js is not installed. Please install Node.js to use this feature.")
            return
            
        # Check if node_modules exists, if not install dependencies
        node_modules_path = os.path.join(os.path.dirname(__file__), "utils", "node_modules")
        if not os.path.exists(node_modules_path):
            print("Installing required dependencies (this may take a moment)...")
            try:
                subprocess.run(
                    ["npm", "install"], 
                    cwd=os.path.join(os.path.dirname(__file__), "utils"),
                    check=True
                )
            except subprocess.SubprocessError as e:
                print(f"Error installing dependencies: {e}")
                return
        
        # Run the YouTube downloader script
        try:
            script_path = os.path.join(os.path.dirname(__file__), "utils", "youtube-downloader.js")
            process = subprocess.Popen(
                ["node", script_path, url, format_choice, download_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Stream output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    
            # Check return code
            return_code = process.poll()
            if return_code != 0:
                print("JavaScript script exited with error code:", return_code)
                for line in process.stderr.readlines():
                    print(line.strip())
        except Exception as e:
            print(f"Error executing YouTube downloader: {e}")
    elif option == "Windows Tweaks":
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Windows Tweaks ===")
        selected = inquirer.list_input("Select a tweak. (Selecting them will give options, and info.) : ", choices=windowstweaks)
        if selected == "Compact OS Mode":
            way = inquirer.list_input("Select a option:", choices=["CompactOS enabler", "CompactOS disabler"])
            if way == "CompactOS enabler":
                print("This will enable Compact OS mode on your Windows system.")
                print("This will reduce the size of the Windows installation.")
                print("This will take a few minutes to complete.")
                print("Are you sure you want to continue?")
                option = inquirer.list_input("Select an option:", choices=["Yes", "No/Exit"])
                if option == "No/Exit":
                    print("Exiting...")
                    time.sleep(1)
                    return
                elif option == "Yes":
                    script_path = os.path.join(os.path.dirname(__file__), "utils", "tweaks", "bat", "CompactOS", "CompactOS", "CompactOSRunner.vbs")
                    try:
                        subprocess.run([script_path], check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"Error executing VBS script: {e}")
            elif way == "CompactOS disabler":
                print("This will disable Compact OS mode on your Windows system.")
                print("This will increase the size of the Windows installation.")
                print("This will take a few minutes to complete.")
                print("Are you sure you want to continue?")
                option = inquirer.list_input("Select an option:", choices=["Yes", "No/Exit"])
                if option == "No/Exit":
                    print("Exiting...")
                    time.sleep(1)
                    return
                elif option == "Yes":
                    script_path = os.path.join(os.path.dirname(__file__), "utils", "tweaks", "bat", "CompactOS", "UncompactOS", "UncompactOSRunner.vbs")
                    try:
                        subprocess.run([script_path], check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"Error executing VBS script: {e}")
        elif selected == "Clean Temporary Files":
            print("This will clean temporary files on your Windows system.")
            print("This will take a few minutes to complete.")
            print("Are you sure you want to continue?")
            option = inquirer.list_input("Select an option:", choices=["Yes", "No/Exit"])
            if option == "No/Exit":
                print("Exiting...")
                time.sleep(1)
                return
            elif option == "Yes":
                script_path = os.path.join(os.path.dirname(__file__), "utils", "tweaks", "bat", "CleanTemp","CleanTempRunner.vbs")
                try:
                    subprocess.run([script_path], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error executing VBS script: {e}")
    elif option == "Weather Forecast":
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Weather Forecast ===")
        location = input("Enter location (City, State/Country): ")
        
        # Path to the weather script
        script_path = os.path.join(os.path.dirname(__file__), "utils", "weather.py")
        
        try:
            # Execute the weather script with the location as an argument
            process = subprocess.Popen(
                [sys.executable, script_path, location],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Stream output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            # Check for errors
            return_code = process.poll()
            if return_code != 0:
                print("Weather script exited with error code:", return_code)
                for line in process.stderr.readlines():
                    print(line.strip())
        except Exception as e:
            print(f"Error executing weather script: {e}")
    else:
        print("Invalid option.")
    print("Press any key to continue...")
    input()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


while True: 
    os.system("cls" if os.name == "nt" else "clear")
    print(banner)
    option = inquirer.list_input("Select an option", choices=choices)
    os.system("cls" if os.name == "nt" else "clear")
    if option != "Exit":
        run(option)
    elif option == "Exit":
        print("Exiting...")
        break