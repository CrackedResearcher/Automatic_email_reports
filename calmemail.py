import os
import subprocess
import sys
import platform
import requests


def is_cron_job_set():
    # rich gpu macos and linux guys
    result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    cron_jobs = result.stdout
    log_dir = "~/email_logs"  # Define the log directory
    log_file = f"{log_dir}/logfile_$(date +\\%Y\\%m\\%d_\\%H\\%M\\%S).log"
    cron_command = f"*/15 * * * * {sys.executable} {os.path.join(os.path.dirname(sys.executable), 'calmemail.py')} >> {log_file} 2>&1"
    return cron_command in cron_jobs


def is_task_set():
    # window buddy
    task_name = "CalmEmail CronJob"
    result = subprocess.run(['schtasks', '/query', '/tn', task_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return task_name in result.stdout


def setup_cron_job():
    log_dir = "~/email_logs"  # Define the log directory
    os.makedirs(os.path.expanduser(log_dir), exist_ok=True)  # Create the log directory if it doesn't exist
    log_file = f"{log_dir}/logfile_$(date +\\%Y\\%m\\%d_\\%H\\%M\\%S).log"
    cron_command = f"*/15 * * * * {sys.executable} {os.path.join(os.path.dirname(sys.executable), 'calmemail.py')} >> {log_file} 2>&1"
    new_cron_jobs = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout + '\n' + cron_command + '\n'
    with subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE) as proc:
        proc.communicate(new_cron_jobs.encode())
    print("Thank you for giving permission ❤️")


def is_module_installed(module_name):
    try: 
        import importlib.util
        importlib.util.find_spec(module_name)
        return True 
    except ImportError:
        return False
    

def install_module(module_name):
    subprocess.run([sys.executable, "-m", "pip", "install", module_name], check=True)


def setup_task():
    task_name = "CalmEmail CronJob"
    log_dir = os.path.expanduser("~/email_logs")
    os.makedirs(log_dir, exist_ok=True)

    # Create the PowerShell script
    powershell_script_path = os.path.join(log_dir, "run_emailHunt.ps1")
    with open(powershell_script_path, 'w') as ps_script:
        ps_script.write(f"""
$logFile = "{log_dir}\\logfile_$(Get-Date -Format 'ddMMMyyyy-HH:mm:ss').log"
{sys.executable} {os.path.join(os.path.dirname(sys.executable), 'calmemail.py')} >> $logFile 2>&1
""")

    if platform.system() == "Windows" and not is_module_installed("win32com.client"):
        install_module("pywin32")

    if platform.system() == "Windows":
        try:
            import win32com.client
            scheduler = win32com.client.Dispatch("Schedule.Service")
            scheduler.Connect()
            rootFolder = scheduler.GetFolder("\\")
            taskDef = scheduler.NewTask(0)

            trigger = taskDef.Triggers.Create(1)  # 1 == daily trigger
            trigger.StartBoundary = "2022-01-01T00:00:00"
            trigger.Repetition.Interval = "PT15M"  # Repeat every 12 minutes

            action = taskDef.Actions.Create(0)  # 0 == execute action
            action.Path = "powershell.exe"
            action.Arguments = f"-File \"{powershell_script_path}\""

            taskDef.RegistrationInfo.Description = "Calm Email Cron Job Service"
            taskDef.Settings.Enabled = True
            taskDef.Settings.StopIfGoingOnBatteries = False

            rootFolder.RegisterTaskDefinition(
                task_name,
                taskDef,
                6,  # TASK_CREATE_OR_UPDATE
                None,
                None,
                3  # TASK_LOGON_INTERACTIVE_TOKEN
            )
            print("Task is set, thank you for giving permission ❤️")
        except Exception as e:
            print(f"Failed to set up scheduled task: {e}")


def is_connected_internet():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    
    except requests.ConnectionError:
        return False


def run_email_hunt():

    if is_connected_internet():
        import emailHunt
        emailHunt.main()

    else:
       print("device not connected to internet. skip running this time")


def calm_email():

    if platform.system() == "Windows":
        cron_job_set = is_task_set()
        if not cron_job_set:
            print("Click on agree to give the permission for CalmEmail to run in background\n")
            setup_task()
        else: 
            print("Running the job as specified by the user")
           
    else:
        cron_job_set = is_cron_job_set()
        if not cron_job_set:
            print("Click on agree to give the permission for CalmEmail to run in background\n")
            setup_cron_job()
        else: 
            print("Running the job as specified by the user")

 
    run_email_hunt()

if __name__ == "__main__":
    calm_email()
