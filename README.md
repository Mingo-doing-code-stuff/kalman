### pip install \<name>

`pip install <name> --index-url=https://pypi.org/simple`

### build command

<!-- https://stackoverflow.com/questions/5458048/how-can-i-make-a-python-script-standalone-executable-to-run-without-any-dependen -->

pyinstaller -F yourprogram.py
-> will fail. Then add <import sys ; sys.setrecursionlimit(sys.getrecursionlimit() \* 5)> into yourprogram.spec file
after:
pyinstaller -F yourprogram.spec
