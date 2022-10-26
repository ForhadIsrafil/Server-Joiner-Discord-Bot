import sys
import subprocess
import atexit
import config


def cleanup():
    for process in processes:
        process.kill()


tokens = []
with open("./tokens.txt", "r") as f:
    for line in f.readlines():
        if not line or line == "":
            continue
        tokens.append(line.replace('\n', '').strip())

print("Server Joiner Starting...")

processes = []
if config.multiple:
    atexit.register(cleanup)
    while len(tokens) > 0:
        token = tokens[0]
        tokens.pop(0)
        try:
            processes.append(subprocess.Popen([sys.executable, "bot.py", token]))
        except Exception as e:
            pass
    try:
        exit_codes = [p.wait(config.timeout) for p in processes]
    except Exception as e:
        print(f"Could not login with token {e.args[0][2]}")
else:
    while len(tokens) > 0:
        token = tokens[0]
        tokens.pop(0)
        try:
            p = subprocess.Popen([sys.executable, "bot.py", token])
            p.wait(timeout=config.timeout)
            p.kill()
        except subprocess.TimeoutExpired as e:
            print(f"Could not login with token {token}")
        except Exception as e:
            pass


print("All bots finished running")
