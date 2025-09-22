import subprocess
import ctypes
import sys
import time
import os

# ===== Admin Check =====
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1
    )
    sys.exit()

# Base folder
BASE_LOG_FOLDER = os.path.join(os.environ.get("USERPROFILE", "C:\\"), "CFIXER", "logs")

# Create a timestamped subfolder for this run
RUN_TIMESTAMP = time.strftime("%Y-%m-%d_%H-%M-%S")
LOG_FOLDER = os.path.join(BASE_LOG_FOLDER, RUN_TIMESTAMP)

os.makedirs(LOG_FOLDER, exist_ok=True)

# ===== Helper Functions =====
def pause():
    input("\nPress Enter to continue...")

def save_log(command_name, output):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{command_name}_{timestamp}.txt"
    path = os.path.join(LOG_FOLDER, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"📝 Log saved to: {path}")

# ===== Splash Screen =====
def splash():
    os.system('cls')
    print("="*50)
    print (" ██████╗███████╗██╗██╗  ██╗███████╗██████╗ ")
    print ("██╔════╝██╔════╝██║╚██╗██╔╝██╔════╝██╔══██╗ ")
    print ("██║     █████╗  ██║ ╚███╔╝ █████╗  ██████╔╝")
    print ("██║     ██╔══╝  ██║ ██╔██╗ ██╔══╝  ██╔══██╗")
    print ("╚██████╗██║     ██║██╔╝ ██╗███████╗██║  ██║")
    print  ("╚═════╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ")                                          
    print("\n                by CEZEY")
    print("="*50)
    print("\n⚠️  Make sure to run this as Administrator!")
    pause()

# ===== SFC Scan (Reliable Logging) =====
def run_sfc():
    print("\n🔹 Running SFC /scannow...")
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_FOLDER, f"SFC_scannow_{timestamp}.txt")
    try:
        # Redirect output to file to ensure logs are captured
        subprocess.run(f'sfc /scannow > "{log_file}" 2>&1', shell=True, check=True)
        print(f"📝 Log saved to: {log_file}")

        # Read log file to check status
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            out = f.read().lower()

        if "did not find" in out or "no integrity violation" in out or "no integrity violations" in out or "no integrity" in out:
            print("✅ SFC completed: No integrity violations found.")
        elif "successfully repaired" in out or ("found" in out and ("repair" in out or "repaired" in out)) or "repaired" in out:
            print("✅ SFC completed: Corrupt files were found and repaired.")
        elif "unable" in out or "could not" in out or "not repaired" in out or "unable to fix" in out:
            print("❌ SFC completed: Some corrupt files could not be repaired.")
        else:
            print("⚠️ SFC completed: Status unknown. Check log for details.")
    except subprocess.CalledProcessError:
        print("❌ SFC failed to run!")
    pause()

# ===== DISM Tools =====
def run_dism(option):
    commands = {
        "CheckHealth": "DISM /Online /Cleanup-Image /CheckHealth",
        "ScanHealth": "DISM /Online /Cleanup-Image /ScanHealth",
        "RestoreHealth": "DISM /Online /Cleanup-Image /RestoreHealth"
    }

    if option not in commands:
        print("❌ Invalid DISM option.")
        pause()
        return

    cmd = commands[option]
    print(f"\n🔹 Running {cmd} ...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = (result.stdout or "") + (result.stderr or "")
        save_log(f"DISM_{option}", output)
        out = output.lower()

        if "no component store corruption detected" in out or "no error" in out:
            print(f"✅ {option} completed: No corruption detected.")
        elif "the component store is repairable" in out or "operation completed successfully" in out or "store corruption" in out or "corruption was repaired" in out:
            print(f"✅ {option} completed: Corruption found and repaired (if needed).")
        else:
            print(f"⚠️ {option} completed: Check log for details.")
    except subprocess.CalledProcessError:
        print(f"❌ {option} failed to run!")
    pause()

# ===== Other Command Runner =====
def run_command(cmd, description=None):
    if description:
        print(f"\n🔹 {description}...")
    else:
        print(f"\n🔹 Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        save_log(cmd.replace(" ", "_"), result.stdout + result.stderr)
        print("✅ Done!")
    except subprocess.CalledProcessError:
        print("❌ Failed!")
    pause()

# ===== Menus =====
def main_menu():
    while True:
        os.system('cls')
        print("="*50)
        print("CFIXER MENU")
        print("="*50)
        print("1. Network Fixes")
        print("2. DISM Tools")
        print("3. SFC Scan")
        print("4. Windows Update Fixes")
        print("5. Disk & Performance Tools")
        print("6. System Tools")
        print("7. Run All Fixes (Recommended)")
        print("8. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            network_menu()
        elif choice == "2":
            dism_menu()
        elif choice == "3":
            run_sfc()
        elif choice == "4":
            update_menu()
        elif choice == "5":
            disk_menu()
        elif choice == "6":
            system_menu()
        elif choice == "7":
            run_all()
        elif choice == "8":
            print("\nExiting CFIXER. Goodbye!")
            break
        else:
            print("❌ Invalid choice!")
            pause()

# ===== Network Menu =====
def network_menu():
    while True:
        os.system('cls')
        print("=== Network Fixes ===")
        print("1. Reset Winsock")
        print("2. Reset IP Stack")
        print("3. Flush DNS Cache")
        print("4. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            run_command("netsh winsock reset", "Resetting Winsock")
        elif choice == "2":
            run_command("netsh int ip reset", "Resetting IP stack")
        elif choice == "3":
            run_command("ipconfig /flushdns", "Flushing DNS cache")
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice!")
            pause()

# ===== DISM Menu =====
def dism_menu():
    while True:
        os.system('cls')
        print("=== DISM Tools ===")
        print("1. CheckHealth")
        print("2. ScanHealth")
        print("3. RestoreHealth")
        print("4. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            run_dism("CheckHealth")
        elif choice == "2":
            run_dism("ScanHealth")
        elif choice == "3":
            run_dism("RestoreHealth")
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice!")
            pause()

# ===== Windows Update Menu =====
def update_menu():
    while True:
        os.system('cls')
        print("=== Windows Update Fixes ===")
        print("1. Stop Windows Update Service")
        print("2. Start Windows Update Service")
        print("3. Clear SoftwareDistribution Cache")
        print("4. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            run_command("net stop wuauserv", "Stopping Windows Update Service")
        elif choice == "2":
            run_command("net start wuauserv", "Starting Windows Update Service")
        elif choice == "3":
            run_command("net stop wuauserv", "Stopping Windows Update Service")
            run_command(f"rd /s /q %windir%\\SoftwareDistribution", "Clearing SoftwareDistribution")
            run_command("net start wuauserv", "Starting Windows Update Service")
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice!")
            pause()

# ===== Disk & Performance Menu =====
def disk_menu():
    while True:
        os.system('cls')
        print("=== Disk & Performance Tools ===")
        print("1. Check Disk (C:)")
        print("2. Optimize Drives (Defrag)")
        print("3. Resource Monitor")
        print("4. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            run_command("chkdsk C:", "Checking Disk")
        elif choice == "2":
            run_command("defrag C: /O", "Optimizing Drives")
        elif choice == "3":
            run_command("start resmon", "Opening Resource Monitor")
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice!")
            pause()

# ===== System Menu =====
def system_menu():
    while True:
        os.system('cls')
        print("=== System Tools ===")
        print("1. Open System Information")
        print("2. Open Device Manager")
        print("3. Open Task Manager")
        print("4. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            run_command("start msinfo32", "Opening System Information")
        elif choice == "2":
            run_command("start devmgmt.msc", "Opening Device Manager")
        elif choice == "3":
            run_command("start taskmgr", "Opening Task Manager")
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice!")
            pause()

# ===== Run All Recommended Fixes =====
def run_all():
    os.system('cls')
    print("=== Running All Recommended Fixes ===")

    steps = [
        ("Reset Winsock", "netsh winsock reset"),
        ("Reset IP Stack", "netsh int ip reset"),
        ("Flush DNS", "ipconfig /flushdns"),
        ("DISM CheckHealth", lambda: run_dism("CheckHealth")),
        ("DISM ScanHealth", lambda: run_dism("ScanHealth")),
        ("DISM RestoreHealth", lambda: run_dism("RestoreHealth")),
        ("SFC /scannow", run_sfc)
    ]

    for name, action in steps:
        print(f"\n=== Step: {name} ===")
        if callable(action):
            action()
        else:
            run_command(action, name)

    print("\nAll fixes attempted. Please restart your PC.")
    pause()

# ===== Main Execution =====
if __name__ == "__main__":
    splash()
    main_menu()