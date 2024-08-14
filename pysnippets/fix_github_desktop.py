import os

file = r"%LOCALAPPDATA%\GitHubDesktop\app-3.4.3\resources\app\renderer.js"
file = os.path.expandvars(file)
find = 'GIT_CONFIG_VALUE_0:""'
replace = 'GIT_CONFIG_VALUE_0:"null"'
with open(file, encoding="utf8") as f:
    content = f.read()
    content = content.replace(find, replace)
with open(file, "w", encoding="utf8") as f:
    f.write(content)
