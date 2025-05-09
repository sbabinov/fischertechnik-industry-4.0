import sys
from src.factory import Factory

def processCommand(cmd, args, factory):
    if cmd == "autoMode":
        factory.sort()
        return "Auto mode started"
    elif cmd == "getData":
        return factory.getStorage(args[0], args[1])
    else:
        return "Unknown command"

if __name__ == "__main__":
    print("Started", flush=True)

    factory = Factory()

    while True:
        inputLine = sys.stdin.readline()

        if not inputLine:
            break

        parts = inputLine.split()
        cmd = parts[0] if parts else ""
        args = parts[1:] if len(parts) > 1 else []

        if cmd.strip() == "exit":
            print("Closing...", flush=True)
            break

        result = processCommand(cmd, args, factory)
        print(result, flush=True)