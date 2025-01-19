from pathlib import Path
import time, os, subprocess
from datetime import datetime

def try_to_push(commit_message, retry_flag):
    try:
        subprocess.run(['git', 'add', '.'], check=True) 
        subprocess.run(['git', 'commit', '-am', commit_message], check=True)
        subprocess.run(['git', 'push'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during git operation: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    if retry_flag:
        time.sleep(60 * 2)  # Wait for 2 minutes
        try_to_push(commit_message, False)
    

def prepare_for_git_push(file_name):
    commit_message = f'Update Windows Start Time: {file_name}'
    return try_to_push(commit_message, True)


def create_file(current_time, folder_name, file_name):
    Path(folder_name).mkdir(exist_ok=True) 
    file_path = Path(folder_name) / file_name
    try:
        with open(file_path, 'r') as file:
            count = len(file.readlines()) + 1
    except FileNotFoundError:
        count = 1

    with open(file_path, 'a') as file:
        file.write(f'{count}: {current_time}')
    return file_name


def process():
    current = datetime.now()

    day = current.strftime('%d') # day of the month. eg: 1-31
    year = current.strftime('%Y') # year. eg: 2025
    day_name = current.strftime('%A') # day of the week. eg: Sunday-Saturday
    month_name = current.strftime('%B') # month of the year. eg: January-December
    month_count = current.strftime('%m') # month count. eg: 1-12

    current_time = current.strftime('%I:%M:%S %p\n') # 12-hour format with AM/PM. eg: 06:13:35 AM
    folder_name = f"{month_count} {month_name} {year}" # eg: 01 January 2025
    file_name = f"{day} {month_name} ({day_name}).txt" # eg: 01 January (Sunday).txt
    return create_file(current_time, folder_name, file_name) 


if __name__ == "__main__":
    file_name = process()

    # Wait for 1 minute to ensure the system starts working correctly.
    # time.sleep(60 * 1)  
    prepare_for_git_push(file_name)