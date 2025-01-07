import json
import os
import pefile
import pyuac
import shutil
import subprocess

from utils.dll_finder import get_dlls
from utils.generator import gen_dll, gen_hacked_dll, export_out


def scan_exe_functions(path, dll):
    print(f"[info]: Scanning {os.path.basename(path)} with {dll}")
    pe = pefile.PE(path)
    pe.parse_data_directories()
    functions = []
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        if entry.dll.decode() != dll:
            continue
        print("The following Functions is found:")
        for imp in entry.imports:
            functions.append(imp.name.decode())
            print(f" - {imp.name.decode()}")
    return functions


def behavior_analyze(path, args, functions):
    print(f"[info]: Behavior Analyzing of {os.path.basename(path)}")
    p = subprocess.run([path] + args, capture_output=True, text=True)
    called_functions = []
    print(f"The following Functions are called by hijacked dll:")
    for function in functions:
        if function in p.stdout:
            called_functions.append(function)
            print(f" - {function}")
    return called_functions


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
        exit()
    try:
        with open("config.json", "r") as f:
            data = json.load(f)
        dlls = get_dlls(data["exe_path"], data["exe_args"])
        functions = scan_exe_functions(data["exe_path"], dlls[0])
        gen_dll(functions, dlls[0])
        called_functions = behavior_analyze(f"./temp/{os.path.basename(data['exe_path'])}", data["exe_args"], functions)
        print(called_functions)
    except Exception:
        import traceback
        traceback.print_exc()
    input("Press enter to end the program......")
