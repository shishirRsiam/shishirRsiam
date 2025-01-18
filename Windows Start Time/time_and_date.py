from pathlib import Path
import time, os, subprocess
from datetime import datetime

def try_to_push(commit_message, can_try):
    print('try to push...')
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        subprocess.run(['git', 'push'], check=True)
        can_try = 0
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during git operation: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(3)
    if can_try:
        try_to_push(commit_message, False)
    

def prepare_for_git_push(file_name):
    print('Pushing...')
    time.sleep(3)
    commit_message = f'Update WIN_Start_Time: {file_name}'
    print('commit_message ->', commit_message)
    try_to_push(commit_message, True)
    pass 

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

    day = current.strftime('%d')
    year = current.strftime('%Y')
    day_name = current.strftime('%A')
    month_name = current.strftime('%B')
    month_count = current.strftime('%m')

    current_time = current.strftime('%H:%M:%S %p\n')
    folder_name = f"{month_count} {month_name} {year}"
    file_name = f"{day} {month_name} ({day_name}).txt"

    return create_file(current_time, folder_name, file_name)


if __name__ == "__main__":
    file_name = process()
    prepare_for_git_push(file_name)
