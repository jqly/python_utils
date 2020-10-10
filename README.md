# python_utils
useful python scripts

# `netget`

## get_zip_and_extract

``` python
get_zip_and_extract(url, save_to, skip_first_folder=True)
```
It downloads a `.zip` file to a temporary folder, and extract the contents to the `save_to` folder. The temporary folder will be removed automatically.

When `skip_first_folder` is set to `True`, it mainly for situation `(a)` from below diagram. It copies the `LICENSE, netget.py, README.md` directly into the `save_to` folder. 

For other situations like `(b)` below, we should set `skip_first_folder` to `False`. It copies the structure `first_folder` and `second_folder` to `save_to`

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
