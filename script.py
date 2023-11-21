import subprocess

import os

import pydig

import pyfiglet

import pathlib

import xml.etree.ElementTree as ET

from colorama import Fore, Style

import warnings

import urllib3

from subprocess import check_call, CalledProcessError

import requests

import nmap



# print ASCII banner

def banner():

    ascii_banner = pyfiglet.figlet_format("PEN-TEST FRAMEWORK")

    print(Fore.GREEN + ascii_banner)

    print("Penetration Testing Framework")

    print("- MANDEEP KUMAR\n")



def check_for_update(repo_owner, repo_name, current_version):

    # GitHub Repository URL

    github_url = f'https://api.github.com/repos/m-cetin/webpwn/releases/latest'



    try:

        # Send a GET request to the GitHub API

        response = requests.get(github_url)

        response.raise_for_status()



        # Parse the JSON response

        release_info = response.json()

        latest_version = release_info['tag_name']



        # Compare versions

        if latest_version != current_version:

            print(f'{Fore.RESET}A newer version ({latest_version}) is available.')

            update_choice = input('Would you like to perform the update? (Y/N): ').strip().lower()



            if update_choice == 'y':

                # Download the latest release

                download_url = release_info['assets'][0]['browser_download_url']

                subprocess.run(['wget', '-O', 'webpwn.py', '-q', download_url])

                print('Update successfully downloaded. Initiating the update...')

                subprocess.run(['python', 'webpwn.py'])

                exit()

            else:

                print('Update declined. The script will not be updated.')



    except Exception as e:

        print(f'Error checking for updates: {str(e)}')



class c:

    PURPLE = '\033[95m'

    BLUE = '\033[94m'

    CYAN = '\033[96m'

    GREEN = '\033[92m'

    YELLOW = '\033[93m'

    RED = '\033[91m'

    END = '\033[0m'

    UNDERLINE = '\033[4m'



# sqlmap mass exploitation

def mass_sql_injection(burp_history_xml):

    # create the "exploitation" directory if it doesn't exist

    if not os.path.exists("exploitation"):

        os.makedirs("exploitation")

    # check if sqlmap is installed

    if not os.path.exists("/usr/bin/sqlmap"):

        install = input("sqlmap is not installed. Do you want to install it? (Y/N) ").lower()

        if install == "y":

            subprocess.run(["apt-get", "install", "sqlmap"])

        else:

            print("sqlmap is required to run this function. Exiting.")

            return



    # parse the burp history xml file

    try:

        tree = ET.parse(burp_history_xml)

        root = tree.getroot()

    except:

        print("Error parsing the burp history xml file. Make sure it is in the correct format and try again.")

        return



    # ask the user for sqlmap options

    risk = input("Enter the risk level for sqlmap (default: 3): ")

    if risk == "":

        risk = "3"

    level = input("Enter the level for sqlmap (default: 5): ")

    if level == "":

        level = "5"

    tamper = input("Enter the tamper scripts for sqlmap (default: space2comment,between): ")

    if tamper == "":

        tamper = "space2comment,between"

    threads = input("Enter the number of threads for sqlmap (default: 10): ")

    if threads == "":

        threads = "10"

    more_flags = input("Do you want to set more flags for sqlmap? (Y/N) ").lower()

    if more_flags == "y":

        flags = input("Enter the flags: ")

    else:

        flags = ""



    # run sqlmap with the options

    command = ["sqlmap", "-r", burp_history_xml, "--risk", risk, "--level", level, "--batch", "--skip", "--dump", "--tamper", tamper, "--threads", threads]

    if flags:

        command += flags.split()

    sqlmap = subprocess.Popen(command, stdout=subprocess.PIPE)

    # print the full output of sqlmap

    with open("exploitation/sqli_full_output.txt", "w") as f:

        for line in sqlmap.stdout:

            print(line.decode("utf-8").strip())

            # save the full output of the scan to a file

            f.write(line.decode("utf-8"))



# Function for Subdomain Enumeration

def subdomain_enumeration():

    print("\nChecking dependencies..")

    try:

        os.popen("chmod +x ./tools/*")

        check_amass = subprocess.Popen(["./tools/amass", "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        check_amass.wait()

        check_amass.poll()

        print(Fore.GREEN + "\n[+] Found Amass!")



        check_assetfinder = subprocess.Popen(["./tools/assetfinder", "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        check_assetfinder.wait()

        check_assetfinder.poll()

        print(Fore.GREEN + "\n[+] Found Assetfinder!")



        check_sublist3r = subprocess.Popen(["python", "./tools/sublist3r.py"], stdout=subprocess.DEVNULL,

                                           stderr=subprocess.STDOUT)

        check_sublist3r.wait()

        check_sublist3r.poll()

        print(Fore.GREEN + "\n[+] Found Sublist3r!")



        check_subfinder = subprocess.Popen(["./tools/subfinder", "-h"], stdout=subprocess.DEVNULL,

                                           stderr=subprocess.STDOUT)

        check_subfinder.wait()

        check_subfinder.poll()

        print(Fore.GREEN + "\n[+] Found Subfinder!")



        check_turbolist3r = subprocess.Popen(["python", "./tools/turbolist3r.py", "-h"], stdout=subprocess.DEVNULL,

                                             stderr=subprocess.STDOUT)

        check_turbolist3r.wait()

        check_turbolist3r.poll()

        print(Fore.GREEN + "\n[+] Found Turbolist3r!")

        print(Fore.RESET)



        try:

            print(Fore.YELLOW + "Be careful! You are actively scanning targets.")

            print(Fore.RESET)

            threads_count = input("How fast do you want to scan? Provide the threads. Press enter for default value (1): ")

            domain_name = input("Which domain do you want to scan? (Example google.com):  ")

            if domain_name == "":

                print("No domain name provided..")

                print(Fore.RED + "Quitting..")

                print(Fore.RESET)

                return

            if threads_count == "":

                threads_count = 1

            else:

                threads_count = int(threads_count)

            answer_of_scan = input("Do you want to scan now? (y/n): ")

            if answer_of_scan.lower() in ["y", "yes", ""]:

                print("######################################################")

                print("Starting. Please be patient! Amass will take a while..")

                print("######################################################")

                pathlib.Path('subdomains').mkdir(parents=True, exist_ok=True)

                amass_args = "./tools/amass enum -v -src -brute -min-for-recursive 2 -d %s -o subdomains/tmp.txt" % (

                domain_name)

                run_amass = check_call(amass_args, shell=True)

                assetfinder_args = "./tools/assetfinder %s | tee -a subdomains/tmp.txt" % (domain_name)

                run_assetfinder = check_call(assetfinder_args, shell=True)

                subfinder_args = "./tools/subfinder -d %s | tee -a subdomains/tmp.txt" % (domain_name)

                run_subfinder = check_call(subfinder_args, shell=True)

                try:

                    sublist_args = "python ./tools/sublist3r.py -d %s -t %s 2>/dev/null | tee -a subdomains/tmp.txt" % (

                    domain_name, threads_count)

                    run_sublist = check_call(sublist_args, shell=True)

                except CalledProcessError:

                    pass

                turbo_args = "python ./tools/turbolist3r.py -d %s -t %s 2>/dev/null | tee -a subdomains/tmp.txt" % (

                domain_name, threads_count)

                try:

                    run_turbo = check_call(turbo_args, shell=True)

                except CalledProcessError:

                    pass

                # clean up wordlist

                print("\n[+] Cleaning up the wordlist.\n")

                run_cleanup = subprocess.getoutput(

                    'cat subdomains/tmp.txt | grep "\." | grep -v "[-]" | grep -v "___" | cut -d "]" -f2 | sed "s/^[ \\\\t]*//" | sort -u > subdomains/domains.txt')

                delete_tmp_file = subprocess.getoutput('rm -rf subdomains/tmp.txt')

                print(Fore.GREEN + "[+] Saved results to subdomains/domains.txt")

                print(Fore.RESET)

                try:

                    print("[+] Now let's try to get live domains, shall we?")

                    print("[+] Checking only ports 80,443,8080,8443,8000.\n")

                    httpx_args = "cat subdomains/domains.txt | httpx -p 80,443,8080,8443,8080 -silent -ip -sc | tee -a /tmp/httpx_output.txt"

                    httpx_args2 = "cat /tmp/httpx_output.txt | cut -d ' ' -f1 > subdomains/live.txt"

                    run_httpx = check_call(httpx_args, shell=True)

                    run_httpx2 = check_call(httpx_args2, shell=True)

                    print(Fore.RESET + "\n[+] Saved results under subdomains/live.txt")

                except:

                    print("[-] Could not run httpx. Did you install it?")

            else:

                print("Okay, see you.")



        except Exception as e:

            print(Fore.RED + "[-] Something went wrong..")

            print(e)

            print(Fore.RESET)

    except:

        print(Fore.RED + "[-] Tools not found. Did you download the tools folder?")

        print("Quitting..")

        print(Fore.RESET)



# Function for network scanning

def nmap_port_scan(target):

    try:

        # Create an Nmap PortScanner object

        nm = nmap.PortScanner()



        # Start scanning the target

        print(f"Initiating Nmap scan for target: {target}")

        nm.scan(target)



        # Iterate through the scanned hosts

        for host in nm.all_hosts():

            print(f"\nNmap scan report for {host}")



            # Get the scanned services and their details

            services = nm[host]['tcp'] if 'tcp' in nm[host] else {}

            

            # Iterate through the services

            for port, service in services.items():

                print(f"\nPORT           STATE           SERVICE")

                print(f"{port}/tcp  {service['state']}  {service['name']}")



    except Exception as e:

        print(f"An error occurred: {e}")



# Main menu for selections

def main_menu():

    while True:

        print(Fore.YELLOW + "--------------------------------------------")

        print("  Main Menu. Please choose your selection!")

        print("--------------------------------------------")

        print(Fore.RESET)

        fields = ('(1) SQL Mass Injection\n'

                  '(2) Subdomain Enumeration\n'

                  '(3) Network Scan\n'  

                  '(q) Quit\n\n'

                  'Your choice: ')

        choice = input(fields)

        print("")

        if choice == "1":

            burp_history_xml = input("Enter the location of the burp history xml file (default: sql.xml): ")

            if not burp_history_xml:

                burp_history_xml = "sql.xml"



            mass_sql_injection(burp_history_xml)

        elif choice == "2":

            subdomain_enumeration()

        elif choice == "3":  

            target = input("Enter the target IP address or hostname: ")

            nmap_port_scan(target)

        elif choice.lower() == "q":

            break

        else:

            print(Fore.RED + "No valid input detected!")

            print(Fore.RESET)



# Start main functions

if __name__ == "__main__":

    banner()

    # current version of script

    current_version = 'stable-version-1.1'

    repo_owner = 'm-cetin'

    repo_name = 'webpwn'



    check_for_update(repo_owner, repo_name, current_version)



    try:

        main_menu()

    except KeyboardInterrupt:

        print(Fore.RED + "\nKey event detected, closing..")

        exit(0)

