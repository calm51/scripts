import os

cwd = os.getcwd()

for i in os.listdir(cwd):
    abspath = os.path.join(cwd, i)
    if os.path.isdir(os.path.join(abspath, ".git")):
        print()
        print()
        print("====================================")
        print("位置:", abspath)
        os.chdir(abspath)
        os.system("git status")
        os.chdir(cwd)
