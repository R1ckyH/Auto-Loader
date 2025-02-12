# Auto-Loader
A automation tools for dll side-loading 

## Credit
Thx [bott0n](https://github.com/bott0n) for the initial idea and supporting

## Templates

- [shellcodeLoader.c](https://gist.github.com/mgeeky/5897962546ce80a630edc89f382f6439) by [mgeeky](https://github.com/mgeeky)


# Install
`pip install -r requirements.txt`

# Usage

## Config

### root directory
edit `config.json` in root directory

| config    | type      | details                                                                |
|-----------|-----------|------------------------------------------------------------------------|
| vcvar_bat | str       | Path of vcvar32.bat or vcvar64.bat for msvc compile                    |
| exe_path  | str       | Path of the target executable                                          |
| exe_args  | list[str] | params of the executable to run                                        |
| template  | list[str] | directory of the loader template to use (e.g ./template/simple_loader) |
| payload   | list[str] | directory of the payload template (e.g ./payload/calculator)           |
| run       | bool      | run the output executable                                              |

### template directory
edit `config.json` in template directory

| config      | type      | details                                                                                   |
|-------------|-----------|-------------------------------------------------------------------------------------------|
| hack_entry  | str       | Path of the target hack() function entry point (e.g shellcodeLoader.c with `void hack()`) |
| hack_lib    | list[str] | Path of the other library called by hack_entry (will compile with hack_entry)             |
| extra_files | list[str] | Path of the extra files need to put with hack_entry                                       |

### run
`python auto_loader.py`
