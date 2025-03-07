import os
import sys
import time
import json
import subprocess
import inquirer
import time

def printheader(text):
    print(f"=== {text} ===")

def printheader(text):
    print(f"=== {text} ===")

choices = [
    "Web Scraping",
    "Windows Tweaks",
    "YT Downloader",
    "Exit"
    "Windows Tweaks",
    "YT Downloader",
    "Exit"
]
windowstweaks = [
    "Compact OS Mode",
    "Clean Temporary Files",
    "Edge Browser",
    "Search indexing",
    "Verbose Messages",
    "Recommended apps/start menu",

]

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