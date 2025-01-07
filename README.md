# Auto-Loader
A automation tools for dll side-loading 

### Credit
Thx [bott0n](https://github.com/bott0n) for the initial idea and supporting

### Templates

- [shellcodeLoader.c](https://gist.github.com/mgeeky/5897962546ce80a630edc89f382f6439) by [mgeeky](https://github.com/mgeeky)


## Install
`pip install -r requirements.txt`

## Usage

### Config
edit `config.json`

| config           | type      | details                                                 |
|------------------|-----------|---------------------------------------------------------|
| vcvar_bat        | str       | Path of vcvar32.bat or vcvar64.bat for msvc compile     |
| exe_path         | str       | Path of the target executable                           |
| exe_args         | list[str] | params of the executable to run                         |
| hack_lib         | str       | Path of the target hack library (e.g shellcodeLoader.c) |
| hack_extra_files | list[str] | Path of the extra files need to put with hack_lib       |
| run              | bool      | run the output executable                               |

### run
`python auto_loader.py`
