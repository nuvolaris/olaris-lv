When requested to function or an action  deduct the <name> and optionally the <package> (assume <package> = 'default' if not specified). 

Use the command:

  ops lv new <action> <package> 

NEVER use `pip import` or a `requirements.txt`, assume you have the required libraries.

It should generate the files:

- packages/<package>/<name>/__main__.py
- packages/<package>/<name>/<name>.py
- tests/<package>/test_<name>.py
- tests/<package>/test_<name>_int.py
