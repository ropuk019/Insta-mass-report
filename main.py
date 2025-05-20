# coding=utf-8
#!/usr/bin/env python3

import sys
import time
from os import path, _exit
from sys import exit

def check_modules():
    required_modules = [
        'colorama',
        'requests',
        'bs4',
        'stem',
        'fake_useragent',
        'instagrapi'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"Missing modules: {', '.join(missing_modules)}")
        print("Install them with: pip install " + " ".join(missing_modules))
        exit(1)

check_modules()

from libs.logo import print_logo
from libs.utils import print_success
from libs.utils import print_error
from libs.utils import ask_question
from libs.utils import print_status
from libs.utils import parse_proxy_file
from libs.proxy_harvester import find_proxies
from libs.attack import report_profile_attack

from multiprocessing import Process, Pool
from colorama import Fore, Back, Style
from instagrapi import Client

class InstagramReporter:
    def __init__(self):
        self.cl = Client()
        self.logged_in = False
        self.report_types = [
            "fake_account",
            "spam",
            "inappropriate_content",
            "violence",
            "hate_speech",
            "bullying",
            "self_harm",
            "scam",
            "intellectual_property",
            "nudity"
        ]
    
    def login(self, username, password):
        try:
            print_status("Logging into Instagram...")
            self.cl.login(username, password)
            self.logged_in = True
            print_success("Login successful!")
            return True
        except Exception as e:
            print_error(f"Login failed: {str(e)}")
            return False
    
    def check_target_status(self, target_username):
        try:
            user_id = self.cl.user_id_from_username(target_username)
            user_info = self.cl.user_info(user_id)
            if not user_info:
                return "BANNED"
            return "ACTIVE"
        except:
            return "BANNED"
    
    def get_max_reports(self):
        return len(self.report_types) * 10  # 10 reports per type

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def report_worker(username, report_type, proxy=None):
    try:
        report_profile_attack(username, report_type, proxy)
        return True
    except:
        return False

def mass_report(reporter, proxies, target_username):
    total_reports = reporter.get_max_reports()
    print_status(f"Preparing to send {total_reports} reports...")
    
    if not proxies:
        proxies = [None] * 50  # Use 50 threads without proxies
    
    # Distribute reports across available proxies
    reports_per_proxy = max(1, total_reports // len(proxies))
    
    print_status("Starting mass reporting process...")
    
    with Pool(processes=min(50, len(proxies))) as pool:
        results = []
        report_count = 0
        
        for report_type in reporter.report_types:
            for i in range(10):  # 10 reports per type
                proxy = proxies[report_count % len(proxies)]
                results.append(pool.apply_async(report_worker, 
                                              (target_username, report_type, proxy)))
                report_count += 1
                print_status(f"Queued report {report_count}/{total_reports}")
        
        pool.close()
        pool.join()
    
    print_success(f"Completed {report_count} reports!")
    return report_count

def monitor_target(reporter, target_username):
    print_status("Monitoring target account status...")
    while True:
        status = reporter.check_target_status(target_username)
        if status == "BANNED":
            print_success("TARGET ACCOUNT HAS BEEN BANNED!")
            return True
        print_status("Target still active, waiting...")
        time.sleep(300)  # Check every 5 minutes

def main():
    print_logo()
    
    # Initialize reporter
    reporter = InstagramReporter()
    
    # Login
    while not reporter.logged_in:
        print("\nInstagram Account Login Required")
        print("(Used only to verify report success and target status)")
        username = ask_question("Enter your Instagram username")
        password = ask_question("Enter your Instagram password")
        reporter.login(username, password)
    
    # Get target
    target_username = ask_question("Enter target username to mass report")
    
    # Verify target exists
    initial_status = reporter.check_target_status(target_username)
    if initial_status == "BANNED":
        print_error("Target account is already banned!")
        exit()
    
    # Proxy setup
    proxies = []
    ret = ask_question("Use proxies? (Recommended) [Y/N]").lower()
    
    if ret == "y":
        ret = ask_question("Scrape fresh proxies? [Y/N]").lower()
        
        if ret == "y":
            print_status("Scraping proxies...")
            proxies = find_proxies()
        elif ret == "n":
            file_path = ask_question("Enter path to proxy list file")
            proxies = parse_proxy_file(file_path)
        
        print_success(f"Loaded {len(proxies)} proxies")
    
    # Start mass reporting
    print("\n" + Fore.RED + "WARNING: THIS WILL SEND MAXIMUM REPORTS TO GET TARGET BANNED")
    print(Style.RESET_ALL)
    confirm = ask_question("Confirm mass report? [Y/N]").lower()
    
    if confirm != "y":
        print_error("Operation cancelled")
        exit()
    
    sent_reports = mass_report(reporter, proxies, target_username)
    
    # Monitor target
    if sent_reports > 0:
        monitor_target(reporter, target_username)

if __name__ == "__main__":
    try:
        main()
        print(Style.RESET_ALL)
    except KeyboardInterrupt:
        print("\n\n" + Fore.RED + "[!] Stopping mass reporter")
        print(Style.RESET_ALL)
        _exit(0)
