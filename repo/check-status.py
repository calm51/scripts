import os

cwd = os.getcwd()

ol1 = []

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
    else:
        ol1.append(abspath)

print()
print()
print("====================================")
print("不是仓库:")
print("\n".join(ol1))
