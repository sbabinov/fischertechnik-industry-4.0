import sys

def processCommand(cmd):
    return "result"



if __name__ == "__main__":
    print("Started", flush=True)
    while True:
        cmd = sys.stdin.readline()

        if not cmd:
            break

        if cmd.strip() == "exit":
            print("Closing...", flush=True)
            break

        result = processCommand(cmd)
        print(result, flush=True)