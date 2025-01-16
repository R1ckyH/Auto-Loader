import csv
import json
import os
import pyuac
import shutil
import subprocess
import sys
import time

temp_log = "./temp/procmon_temp.csv"
proc_cmd_base = [
    "Procmon.exe",
    "/Quiet",
    "/AcceptEula",
    "/Minimized"]
proc_cmd_run = [
    "/LoadConfig",
    "./utils/ProcmonConfiguration.pmc",
    "/BackingFile",
    "./temp/out.pml"
]
proc_cmd_save = [
    "/SaveApplyFilter"
    "/OpenLog",
    "./temp/out.pml",
    "/SaveAs",
    temp_log,
]


def check_path(path):
    if not os.path.exists(path):
        print(f"[Error]: {path} not found")
        exit()


def get_exe(path):
    print(f"[info]: Getting exe from {path}")
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if os.path.exists(path):
        shutil.copy(path, "./temp")
        print(f"[info]: Copied {path} to {os.getcwd()}/temp/{os.path.basename(path)}")
    else:
        print(f"[Error]: exe {path} not found")
        exit()
    return os.path.dirname(path), "./temp/" + os.path.basename(path)


def get_fail_dll(log_path, exe_name):
    dll_failures = set()
    with open(log_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if ".dll" in row.get('Path', '') and exe_name == row.get('Process Name', ''):
                path = row.get('Path', '')
                if path.lower().endswith('.dll'):
                    dll_failures.add(path)
    return dll_failures


def get_dlls(exe_path, exe_args):
    check_path(exe_path)
    check_path("./Procmon.exe")
    subprocess.run(["Procmon.exe", "/Terminate"])

    if os.path.exists("temp"):
        shutil.rmtree("temp")
        print("[info]: Removed Temp directory")

    original_path, exe_path = get_exe(exe_path)

    print("[info]: Starting Procmon.exe......")
    cmd = proc_cmd_base + proc_cmd_run
    subprocess.Popen(cmd)
    time.sleep(4)

    print(f"[info]: Starting {exe_path} with args: {exe_args}")
    target = subprocess.Popen([exe_path] + exe_args)
    time.sleep(2)
    target.terminate()

    print(f"[info]: Terminate Procmon.exe")
    subprocess.run(["Procmon.exe", "/Terminate"])
    time.sleep(0.5)
    print(f"[info]: Extracting the Log......")
    cmd = proc_cmd_base + proc_cmd_save
    subprocess.run(cmd)

    print(f"[info]: Finding dll from Log")
    dll_failures = get_fail_dll(temp_log, os.path.basename(exe_path))

    if not dll_failures:
        print("No missing DLLs found, check the procmon run correctly or change the time for waiting the exe run")
        return

    print("\nMissing DLLs:")
    for dll in sorted(dll_failures):
        print(f"- {os.path.basename(dll)}")

    dlls_copied = []
    for dll in sorted(dll_failures):
        try:
            shutil.copy(original_path + "\\" + os.path.basename(dll), dll)
            dlls_copied.append(os.path.basename(dll))
            print(f"[info]: Copying {original_path}\\{os.path.basename(dll)} to {dll}")
        except FileNotFoundError:
            print(f"[Error]: Failed to copy {original_path}\\{os.path.basename(dll)} to {dll}")
    return dlls_copied


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
        exit()
    try:
        with open("config.json", "r") as f:
            data = json.load(f)
        get_dlls(data["exe_path"], data["vcvar_bat"])
    except Exception:
        import traceback

        traceback.print_exc()
    input("Press enter to end the program......")
