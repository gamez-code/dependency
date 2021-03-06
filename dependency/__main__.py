from dependency.main import Dependency
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--console", action="count", default=0, help="Let you write command in the interactive console.")
parser.add_argument("-s", "--script", type=str, default="empty", help="Let you run a script")

args = parser.parse_args()
if args.console:
    lines = []
    _end = True
    while _end:
        line = input("> ")
        if line:
            lines.append(line)
            _end = "end" != line.lower().strip().split()[0]
else:
    try:
        with open(args.script, "r") as file:
            data = file.read()
        lines = data.split("\n")
    except FileNotFoundError:
        print("There is a problem, the file cannot found")
response = Dependency(lines).play()
for r in response:
    print(r)
