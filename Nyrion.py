import os
import sys
import time
import shutil

# Optional: colored output (works if you have colorama installed)
try:
    from colorama import init, Fore, Style
    init()
except ImportError:
    class Fore:
        RED = ''
        GREEN = ''
        CYAN = ''
        YELLOW = ''
        WHITE = ''
        RESET = ''
    class Style:
        BRIGHT = ''
        NORMAL = ''

COPYRIGHT = "Copyright Danny Smeulders/CastyAnimations"
echo_on = True

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_screen():
    clear_screen()
    s_art = [
        "██        ██",
        "████      ██",    
        "██  ██    ██",
        "██    ██  ██",
        "██      ████",
        "██        ██",
        "██        ██"
    ]
    for line in s_art:
        print(Fore.WHITE + line + Fore.RESET)
    print()
    bar_length = 20
    print("Loading Nyrion 1.0...")
    for i in range(bar_length + 1):
        bar = "█" * i + "-" * (bar_length - i)
        print(Fore.GREEN + f"[{bar}]" + Fore.RESET, end='\r', flush=True)
        time.sleep(0.1)
    print()  # newline after loading bar

def show_help():
    print(Fore.CYAN + "Available commands:" + Fore.RESET)
    print("  help          - Show this help message")
    print("  time          - Show current date and time")
    print("  date          - Show current date")
    print("  cls           - Clear the screen")
    print("  dir           - List files in current directory")
    print("  cd <dir>      - Change directory")
    print("  type <file>   - Show file contents")
    print("  copy <src> <dst> - Copy file")
    print("  move <src> <dst> - Move file")
    print("  del <file>    - Delete file")
    print("  ren <old> <new>  - Rename file")
    print("  mkdir <dir>   - Create a new directory")
    print("  rmdir <dir>   - Remove empty directory")
    print("  echo <text>   - Print text or toggle echo on/off")
    print("  pause         - Pause execution until keypress")
    print("  exit          - Exit Syntrax shell")

def show_time():
    print(Fore.YELLOW + time.strftime("%a %b %d %H:%M:%S %Y") + Fore.RESET)

def show_date():
    print(Fore.YELLOW + time.strftime("%Y-%m-%d") + Fore.RESET)

def list_files():
    try:
        files = os.listdir('.')
        for f in files:
            if os.path.isdir(f):
                print(Fore.CYAN + f + "\\" + Fore.RESET)
            else:
                print(f)
    except Exception as e:
        print(Fore.RED + "Error listing files: " + str(e) + Fore.RESET)

def change_directory(path):
    try:
        os.chdir(path)
    except Exception as e:
        print(Fore.RED + f"Bad command or filename: {e}" + Fore.RESET)

def type_file(filename):
    try:
        with open(filename, 'r') as file:
            print(file.read())
    except Exception as e:
        print(Fore.RED + f"File not found: {e}" + Fore.RESET)

def copy_file(src, dst):
    try:
        shutil.copy2(src, dst)
        print(f"        1 file(s) copied.")
    except Exception as e:
        print(Fore.RED + f"Cannot copy file: {e}" + Fore.RESET)

def move_file(src, dst):
    try:
        shutil.move(src, dst)
        print(f"        1 file(s) moved.")
    except Exception as e:
        print(Fore.RED + f"Cannot move file: {e}" + Fore.RESET)

def delete_file(filename):
    try:
        os.remove(filename)
        print(f"        {filename} deleted.")
    except Exception as e:
        print(Fore.RED + f"Cannot delete file: {e}" + Fore.RESET)

def rename_file(old, new):
    try:
        os.rename(old, new)
        print(f"        File renamed from {old} to {new}.")
    except Exception as e:
        print(Fore.RED + f"Cannot rename file: {e}" + Fore.RESET)

def make_directory(dirname):
    try:
        os.mkdir(dirname)
        print(f"        Directory created: {dirname}")
    except Exception as e:
        print(Fore.RED + f"Cannot create directory: {e}" + Fore.RESET)

def remove_directory(dirname):
    try:
        os.rmdir(dirname)
        print(f"        Directory removed: {dirname}")
    except Exception as e:
        print(Fore.RED + f"Cannot remove directory: {e}" + Fore.RESET)

def echo_command(args):
    global echo_on
    if not args:
        print(Fore.RED + "The syntax of the command is incorrect." + Fore.RESET)
        return
    arg = args[0].lower()
    if arg == "off":
        echo_on = False
    elif arg == "on":
        echo_on = True
    else:
        print(' '.join(args))

def pause_command():
    input("Press any key to continue . . .")

def main():
    global echo_on
    loading_screen()
    clear_screen()
    print(Fore.WHITE + Style.BRIGHT + "Syntrax Version 1.0" + Style.NORMAL + Fore.RESET)
    print(Fore.WHITE + COPYRIGHT + Fore.RESET)
    print()

    while True:
        try:
            cwd = os.getcwd()
            drive = os.path.splitdrive(cwd)[0] or 'C:'
            prompt_path = cwd.replace(drive, '').strip("\\/")
            prompt_path = prompt_path if prompt_path else "\\"
            prompt = f"{drive}{prompt_path}> "

            command = input(Fore.YELLOW + prompt + Fore.RESET).strip()
            if not command:
                continue

            if echo_on:
                print(command)

            parts = command.split()
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd == "help":
                show_help()
            elif cmd == "time":
                show_time()
            elif cmd == "date":
                show_date()
            elif cmd == "cls":
                clear_screen()
            elif cmd == "dir":
                list_files()
            elif cmd == "cd":
                if args:
                    change_directory(args[0])
                else:
                    print(Fore.RED + "The syntax of the command is incorrect." + Fore.RESET)
            elif cmd == "type":
                if args:
                    type_file(args[0])
                else:
                    print(Fore.RED + "The syntax of the command is incorrect." + Fore.RESET)
            elif cmd == "copy":
                if len(args) == 2:
                    copy_file(args[0], args[1])
                else:
                    print(Fore.RED + "The syntax of the command is incorrect." + Fore.RESET)
            elif cmd == "move":
                if len(args) == 2:
                    move_file(args[0], args[1])
                else:
                    print(Fore.RED + "The syntax of the command is incorrect." + Fore.RESET)
            elif cmd == "del":
                if args:
                    delete_file(args[0])
                else:
                    print(Fore.RED + "The syntax of the command is incorrect." + Fore.RESET)
            elif cmd == "ren":
                if len(args) == 2:
                    rename_file(args[0], args[1])
                else:
                    print(Fore.RED + "The syntax of the command is incorrect." + Fore.RESET)
            elif cmd == "mkdir":
                if args:
                    make_directory(args[0])
                else:
                    print(Fore.RED + "The syntax of the command is incorrect." + Fore.RESET)
            elif cmd == "rmdir":
                if args:
                    remove_directory(args[0])
                else:
                    print(Fore.RED + "The syntax of the command is incorrect." + Fore.RESET)
            elif cmd == "echo":
                echo_command(args)
            elif cmd == "pause":
                pause_command()
            elif cmd == "exit":
                print("Exiting Syntrax shell...")
                break
            else:
                print(Fore.RED + f"'{cmd}' is not recognized as an internal or external command," + 
                      "\noperable program or batch file." + Fore.RESET)

        except KeyboardInterrupt:
            print("\nUse 'exit' command to quit.")
        except EOFError:
            print("\nExiting Syntrax shell...")
            break

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit Syntrax...")  # <-- THIS KEEPS THE WINDOW OPEN


           


