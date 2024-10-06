import shutil
from colorama import init, Fore, Style
import sqlite3

init(autoreset=True)

def store_data_in_db(path, email, app_password, report_sent_to_email, user_interval_run):
    connect = sqlite3.connect(path)
    c = connect.cursor()
    c.execute('INSERT INTO user (email, app_password, report_sent_to_email, user_interval_run) VALUES (?,?,?,?)',(email, app_password, report_sent_to_email, user_interval_run))
    connect.commit()
    connect.close()


def collect_user_data(pathDb):
    terminal_width = shutil.get_terminal_size().columns
    
    print(Fore.GREEN + Style.BRIGHT + "=" * terminal_width)
    print(" ".center(terminal_width))
    welcome_message = "Welcome to the CalmEmail" + Fore.CYAN + " Terminal Setup!"
    print(welcome_message.center(terminal_width))
    print(" ".center(terminal_width))
    print("✦ The steps below will guide you on how to get this app running ✦".center(terminal_width))
    print(" ".center(terminal_width))
    print(Fore.GREEN + Style.BRIGHT + "=" * terminal_width)
    print(" ".center(terminal_width))
    

    print(Fore.LIGHTWHITE_EX + "Steps:\n")
    print(Fore.GREEN + "   1. ensure that you've app password of the email that u'll use to login available")
    print("\n      if you dont have one, go get it here: \n\tfor gmail (https://myaccount.google.com/apppasswords),\n\tfor outlook (https://account.microsoft.com/security)".center(terminal_width))
    print(" ".center(terminal_width))
    print(Fore.YELLOW + "   2. make sure the email address youre using has 2FA enabled")
    print(Fore.RED + "   3. and you must be connected to the internet")
    print(" ".center(terminal_width))
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "=" * terminal_width)
    print(" ".center(terminal_width))
    print(Fore.LIGHTWHITE_EX + "After you've completed above steps, drop your email & app password below ⬇️\n")
    print(" ".center(terminal_width))

    email = input(Fore.BLUE + "Enter your email: " + Style.RESET_ALL)
    app_password = input(Fore.BLUE + "Enter your App password: " + Style.RESET_ALL)
    report_sent_to_email = input(Fore.BLUE + f"On which email do you want the report of [{email}] to be sent: " + Style.RESET_ALL)
    user_interval_run = float(input(Fore.BLUE + "Just one last one: how frequently do you need email reports? (like after how many hours): " + Style.RESET_ALL))
    print(" ".center(terminal_width))
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "=" * terminal_width)
    
    store_data_in_db(path=pathDb, email=email,app_password=app_password,report_sent_to_email= report_sent_to_email, user_interval_run = user_interval_run)
    
    return email
