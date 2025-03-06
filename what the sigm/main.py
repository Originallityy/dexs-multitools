import os
import sys
import time
import json
import subprocess
import inquirer

choices = [
    "Web Scraping",
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
            return
        if option == "Yes":
            script_path = os.path.join(os.path.dirname(__file__), "utils", "web_scraping.rb")
            try:
                result = subprocess.run(["ruby", script_path], check=True, capture_output=True, text=True)
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Error running script: {e}")
                print(f"stderr: {e.stderr}")

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