import os
import shutil
import subprocess
import sys

from lxml.isoschematron import extract_xsd


def gen_code(functions, dll, hack_function="", hack_lib=""):
    dll_name = dll[:-4]
    print(f"[info]: Creating {dll_name}.cpp for dll compiling")
    with open("utils/base.cpp", "r") as f:
        code = f.read()
    if hack_function != "":
        code = f'#include "{os.path.basename(hack_lib)}"\n{code}'
    for function in functions:
        if function == hack_function:
            code += f'extern "C" __declspec(dllexport) VOID _cdecl {function}(void)' + '{ hack();}\n'
        else:
            code += f'extern "C" __declspec(dllexport) VOID _cdecl {function}(void)' + '{ printString("' + function + '");}\n'

    with open(f"temp/{dll_name}.cpp", "w") as f:
        f.write(code)
    return f"temp/{dll_name}.cpp"


def gen_dll(functions, dll, vcvar_bat):
    cpp_path = gen_code(functions, dll)
    os.chdir("temp")
    # ["g++", "-shared", "-o", f"./temp/{dll}", cpp_path, "-O2", "-static-libgcc", "-static-libstdc++"]
    command = [vcvar_bat, "&&", "cl", "/std:c++20", "/EHsc", "/LD", os.path.basename(cpp_path), "/link",
               f"/OUT:./{dll}"]
    subprocess.run(command)
    print(f"[info]: Compiled new dll to /temp/{dll}")
    os.chdir("../")
    return cpp_path


def gen_hacked_dll(functions, dll, hack_function, hack_entry, hack_lib, vcvar_bat, template):
    if not os.path.exists(f"out/{template}"):
        os.mkdir(f"out/{template}")

    hack_lib.append(hack_entry)
    for file in hack_lib:
        print(f"[info]: Copying {file} to /temp/{os.path.basename(file)}")
        shutil.copy(file, f"./temp/{os.path.basename(file)}")
    print(f"[info]: Creating new dll to /out/{dll}")
    cpp_path = gen_code(functions, dll, hack_function, hack_entry)
    os.chdir("temp")
    command = [vcvar_bat, "&&", "cl", "/std:c++20", "/EHsc", "/LD", os.path.basename(cpp_path), "/link",
               f"/OUT:../out/{template}/{dll}"]
    print(f"[info]: Compiling with command: {' '.join(command)}")
    subprocess.run(command, shell=True)
    print(f"[info]: Compiled new dll to /out/{template}/{dll}")
    os.chdir("../")
    return cpp_path


def export_out(extra_files, files, template):
    extra_files += files
    for file in extra_files:
        if os.path.isdir(file):
            shutil.copytree(file, f"out/{template}/", dirs_exist_ok=True)
        else:
            shutil.copy(file, f"out/{template}/{os.path.basename(file)}")
        print(f"[info]: Exported /out/{template}/{os.path.basename(file)}")


if __name__ == "__main__":
    gen_hacked_dll(["WPRCFormatError"], "WindowsPerformanceRecorderControl.dll", "WPRCFormatError",
                   "D:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat")
