import json
import os
import pyuac
import subprocess

from utils.exe_analyzer import scan_exe_functions, behavior_analyze, select_scanned_dlls
from utils.dll_finder import get_dlls
from utils.generator import gen_dll, gen_hacked_dll, export_out


def main():
    with open("config.json", "r") as f:
        data = json.load(f)

    dlls = get_dlls(data["exe_path"], data["exe_args"])
    called_functions = []
    functions = ""
    dll = ""
    while not called_functions:
        if len(dlls) == 0:
            print(f"[Error]: No dll can be used")
            return
        dll = select_scanned_dlls(dlls)
        functions = scan_exe_functions(data["exe_path"], dll)
        gen_dll(functions, dll, data["vcvar_bat"])

        called_functions = behavior_analyze(f"./temp/{os.path.basename(data['exe_path'])}", data["exe_args"], functions)
        dlls.remove(dll)
        if not called_functions:
            print(f"[Error]: {dll} cannot be used")

    with open(f"{data['template']}/config.json", "r") as f:
        template_config = json.load(f)

    if not data["template"].endswith("/") or data["template"].endswith("\\"):
        data["template"] += "/"

    gen_hacked_dll(functions, dll, called_functions[0], data["template"] + template_config["hack_lib"], data["vcvar_bat"])

    files = [f"./temp/{os.path.basename(data['exe_path'])}"] + data["payload"]
    export_out(template_config["extra_files"], files, data["template"])

    if data["run"]:
        os.chdir("./out")
        p = subprocess.run([f"{os.path.basename(data['exe_path'])}"] + data["exe_args"], capture_output=True, text=True)
        print(p.stdout)

    print(f"Done All!!!!!!!!!")


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
        exit()
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
    input("Press enter to end the program......")
