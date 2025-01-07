import json
import os
import pyuac
import subprocess

from utils.exe_analyzer import scan_exe_functions, behavior_analyze
from utils.dll_finder import get_dlls
from utils.generator import gen_dll, gen_hacked_dll, export_out


def main():
    with open("config.json", "r") as f:
        data = json.load(f)
    dlls = get_dlls(data["exe_path"], data["exe_args"])
    functions = scan_exe_functions(data["exe_path"], dlls[0])
    gen_dll(functions, dlls[0])
    called_functions = behavior_analyze(f"./temp/{os.path.basename(data['exe_path'])}", data["exe_args"], functions)
    gen_hacked_dll(functions, dlls[0], called_functions[0], data["hack_lib"], data["vcvar_bat"])
    export_out(data["hack_extra_files"], f"./temp/{os.path.basename(data['exe_path'])}")
    if data["run"]:
        os.chdir("./out")
        p = subprocess.run([f"{os.path.basename(data['exe_path'])}"] + data["exe_args"], capture_output=True, text=True)
        print(p.stdout)


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
