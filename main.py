import os

def read_log_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when accessing '{filename}'.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    log_file = "mission_computer_main.log"
    read_log_file(log_file)