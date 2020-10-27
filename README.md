# python_utils
useful python scripts

# `netget`

## get_zip_and_extract

``` python
get_zip_and_extract(url, save_to, auth=None, skip_first_folder=True)
```
It downloads a `.zip` file to a temporary folder, and extract the contents to the `save_to` folder. The temporary folder will be removed automatically.

When `skip_first_folder` is set to `True`, it mainly for situation `(a)` from below diagram. It copies the `LICENSE, netget.py, README.md` directly into the `save_to` folder. 

For other situations like `(b)` below, we should set `skip_first_folder` to `False`. It copies the structure `first_folder` and `second_folder` to `save_to`.

``` text
(a)
main.zip
|
\---first_folder
        a
        b.py
        c.md

(b)
main.zip
|
+---first_folder
|       a.py
|
\---second_folder
        a
        b.py
        c.md
```

There are additional two features. One is the `retry_on_timeout` nature; the timeout error would be retried for several times after it raise such error, and the other is simple `auth=(username, password)`.

# `psrun`

## run_ps

``` python
def run_ps(cmds, *args, **kwargs)
```

This function mimics the `subprocess.run`, and changes the default `cmd.exe` to the `powershell.exe`. `*args` and `**kwargs` passes the params to `subprocess.run`; the commands `cmds` could be `str` type or `list` type. `cmds` would be written into temporary file as a script and execute. Temporary files itself would be removed after execution.

There is a simple demo of its usage.

``` python
run_ps('''cd c:\Users
Get-ChildItem .''')
# the above could also be as the below
run_ps([
        'cd c:\Users',
        'Get-ChildItem .'
])
```