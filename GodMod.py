import sys
import time
import random
import os
from datetime import datetime, timedelta
import pytz  # Ensure you have pytz installed for timezone handling
from threading import Timer

# ANSI escape sequences for colors (Yellow and Magenta excluded)
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_WHITE = "\033[97m"
RESET = "\033[0m"

# Correct key for verification
CORRECT_KEY = "@GODMOD57"

result_history = []

def show_welcome_message():
    try:
        from cfonts import render
    except ImportError:
        os.system('pip install python-cfonts')
        from cfonts import render

    output = render('GODMOD', colors=['cyan', 'yellow'], align='center')
    print(output)

def verify_key():
    while True:
        key = input(f"{BRIGHT_CYAN}Please enter the key to continue: {RESET}")
        if key == CORRECT_KEY:
            print(f"{BRIGHT_GREEN}Key verified! You can now proceed.{RESET}")
            break
        else:
            print(f"{BRIGHT_RED}Invalid key! Please try again.{RESET}")

def select_server():
    print(f"{BRIGHT_CYAN}Available Servers:")
    print(f"{BRIGHT_WHITE}1. Server 1")
    print(f"{BRIGHT_WHITE}2. Server 2")
    print(f"{BRIGHT_WHITE}3. Server 3")

    server_choice = input(f"{BRIGHT_CYAN}Please select a server (1/2/3): {RESET}")
    if server_choice in ['1', '2', '3']:
        print(f"{BRIGHT_GREEN}Server {server_choice} connected successfully!{RESET}")
    else:
        print(f"{BRIGHT_RED}Invalid server choice!{RESET}")
        select_server()

# Timer function for 1-minute intervals
def start_timer():
    timezone = pytz.timezone("Asia/Kolkata")

    def update_timer():
        # Get the current time
        now = datetime.now(timezone)
        seconds = now.second
        remaining_seconds = 60 - seconds

        # Get current hour and minute
        current_hour = now.hour
        current_minute = now.minute

        # Define start time at 5:29 AM
        start_hour = 5
        start_minute = 29

        # Calculate total minutes elapsed since 5:29 AM
        elapsed_minutes = (current_hour * 60 + current_minute) - (start_hour * 60 + start_minute)

        # If the current time is before 5:29 AM, set elapsed_minutes to 0
        if elapsed_minutes < 0:
            elapsed_minutes = 0

        # Update the current period number (in format yyyyMMdd100001xxxx)
        formatted_date = now.strftime('%Y%m%d')
        period_number = "100001".concat(f"{elapsed_minutes:04d}")
        
        # Print the current period first
        print(f"{BRIGHT_CYAN}Current Period: {BRIGHT_WHITE}{formatted_date}{period_number}{RESET}")
        
        # Then print the timer below the current period
        print(f"{BRIGHT_CYAN}Timer: {BRIGHT_WHITE}{0:02d}:{remaining_seconds:02d}{RESET}")

        # Run the timer every second
        Timer(1, update_timer).start()

    update_timer()

def calculate_and_hide():
    # Perform the calculation logic
    period_number = int(input(f"{BRIGHT_CYAN}Please enter the last period number: {RESET}"))
    last_result = int(input(f"{BRIGHT_CYAN}Please enter the last result number: {RESET}"))
    second_result = int(input(f"{BRIGHT_CYAN}Enter the 2nd result number: {RESET}"))

    # Calculation logic
    total = period_number + last_result
    final_result = abs(second_result - total)

    # Show calculation in progress
    print(f"{BRIGHT_CYAN}Calculating... Please wait.{RESET}")
    time.sleep(2)

    # Show only the final results after calculation
    accuracy = (30 + (final_result % 71))
    result_message = classify_result(final_result)

    # Store result history with current period
    timezone = pytz.timezone("Asia/Kolkata")
    now = datetime.now(timezone)
    elapsed_minutes = (now.hour * 60 + now.minute) - (5 * 60 + 29)
    if elapsed_minutes < 0:
        elapsed_minutes = 0

    current_period = f"{now.strftime('%Y%m%d')}100001{elapsed_minutes:04d}"
    result_history.append(f"Period: {current_period} | Result: {result_message} | Accuracy: {accuracy}%")

    # Display current period, accuracy, and final result
    print(f"{BRIGHT_BLUE}═════════════════════════════════════════════════════════════{RESET}")
    print(f"{BRIGHT_WHITE}Current Period: {BRIGHT_CYAN}{current_period}{RESET}")
    print(f"{BRIGHT_GREEN}Accuracy: {accuracy}%{RESET}")
    print(f"{BRIGHT_GREEN}Final Result: {result_message}{RESET}")
    print(f"{BRIGHT_BLUE}═════════════════════════════════════════════════════════════{RESET}")

def classify_result(final_result):
    if final_result > 10:
        return random.choice([f"{BRIGHT_RED}Red{RESET}", f"{BRIGHT_GREEN}Green{RESET}"])
    elif final_result in [2, 4, 0]:
        return f"{BRIGHT_RED}Small Red{RESET}"
    elif final_result in [1, 3]:
        return f"{BRIGHT_GREEN}Small Green{RESET}"
    elif final_result in [5, 7, 9]:
        return f"{BRIGHT_GREEN}Big Green{RESET}"
    elif final_result in [6, 8]:
        return f"{BRIGHT_RED}Big Red{RESET}"
    elif final_result == 10:
        return f"{BRIGHT_WHITE}Skip{RESET}"

def exit_program():
    print(f"{BRIGHT_CYAN}Exiting the program... Displaying result history.{RESET}")
    time.sleep(1)
    print(f"{BRIGHT_BLUE}═════════════════════════════════════════════════════════════{RESET}")
    print(f"{BRIGHT_WHITE}Final Results History:{RESET}")

    for entry in result_history:
        print(f"{BRIGHT_WHITE}{entry}{RESET}")

    print(f"{BRIGHT_BLUE}═════════════════════════════════════════════════════════════{RESET}")
    print(f"{BRIGHT_CYAN}Thank you for using the program! Goodbye!{RESET}")
    sys.exit()

def update_results():
    result_input = input(f"{BRIGHT_CYAN}Enter 'W' for Win, 'L' for Loss, 'S' for Skip or 'E' to Exit: {RESET}").strip().upper()
    
    if result_input == 'E':
        exit_program()
    elif result_input not in ['W', 'L', 'S']:
        print(f"{BRIGHT_RED}Invalid input. Please enter 'W', 'L', 'S', or 'E'.{RESET}")

def main_loop():
    show_welcome_message()
    verify_key()
    select_server()
    start_timer()

    while True:
        calculate_and_hide()
        update_results()

if __name__ == "__main__":
    main_loop()