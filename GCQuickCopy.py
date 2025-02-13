import string
import sys
import os
import shutil
import readline
from tqdm import tqdm
from pathlib import Path
from ctypes import windll
# whoever says "python doesn't need code comments" is BULLSHITTING this shits kinda hard to read
# either that or i just suck at raw python scripting
# ...i probably just suck at raw python scripting 3:


# big ol get drives function i nabbed from stackoverflow
def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    
    return drives

# made a function for prompting yes/no since im doing it multiple times
def yes_no_prompt(prompt, default):
    while True:
        yes_no_input = input(prompt).upper()
        if yes_no_input == 'Y':
            return True
        elif yes_no_input == 'N':
            return False
        elif yes_no_input == '':
            return default
        else:
            print("Please type Y or N! >~<")


# thank you kind stackoverflow commenter :3 https://stackoverflow.com/a/8505387
# basically all of this is to provide an input function with some placeholder text to speed up the folder renaming process
def input_with_prefill(prompt, prefill):
    def hook(): # you can do such a thing? eugh
        readline.insert_text(prefill)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    result = input(prompt)
    readline.set_pre_input_hook()
    return result

# okay google gemini... lets see what you got
def copy_file(source, dest):
    file_size = os.path.getsize(source)
    with open(source, 'rb') as f_in, open(dest, 'wb') as f_out:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=dest.split('/')[-1]) as progress_bar:
            while True:
                buf = f_in.read(1024)
                if not buf:
                    break
                f_out.write(buf)
                progress_bar.update(len(buf))

# funny little public boolean to let the program know if were copying another disc after
disc2_mode = False

if __name__ == '__main__':
    # grab arguments and store them in a variable for elegance
    args = sys.argv
    input_file = args[1] # if the file isnt the first argument, blame the user!
    # check if there's another args, cause otherwise python gets unhappy
    if len(args) == 3:
        disc2_file = args[2]
        disc2_mode = True
        print(f"Disc 2 detected! Filename: {disc2_file}")

    # get the game id from the iso file and store it
    # (i REALLY hope every GC game has a 6 byte id)    
    with open(input_file, 'rb') as f:
        game_id = f.read(6)
        game_id = game_id.decode('ascii') # convert the raw binary thing to ascii

    dest_file_name = "game.iso"

    # get the available drives, stores it into a variable then displays them to the user
    available_drives = get_drives()
    print("Available drives: ", available_drives)

    while True:
        # ask for drive to copy to
        dest_input = input("Pwease select destination drive: ")

        # uppercase that cause thats the only way it'll work
        dest_drive = dest_input.upper()
        if dest_drive in available_drives:
            dest_drive = f"{dest_drive}:/" # if it's valid, append :/ to the drive letter to make it a valid Windows drive letter
            break
        else:
            # invalid drive letter, loop back to the question
            print("That's not a valid drive! >~<")

    # now we construct the destination file path
    dest_folder_name = f"{Path(input_file).stem} [{game_id}]" # set the destination folder name to the input file name WITHOUT its extension, and include the game id
    print(f"Destination folder is {dest_folder_name}")
    if yes_no_prompt("Would you like to change this folder name? y/[N] ", False):
        dest_folder_name = input_with_prefill("Please change folder name here: ", dest_folder_name)
    
    dest_file_path = f"{dest_drive}games/{dest_folder_name}" # the final file destination path

    # this is just as an override of sorts in case disc 2 is incorrectly detected        
    if disc2_mode == False:
        if yes_no_prompt("Is this the 2nd disc? y/[N] ", False):
            print("Initiating disc 2 mode >:3")
            dest_file_name = "disc2.iso"
            # ask to verify the disc 1 folder name but prefill with the current file name for convenience nya! :3
            dest_folder_name = input_with_prefill("Pwease verify disc 1's folder name: ", dest_folder_name)
            # set the file path
            dest_file_path = f"{dest_drive}games/{dest_folder_name}"

    # create the destination directory
    os.makedirs(dest_file_path, exist_ok=True)

    dest_file_full_path = f"{dest_file_path}/{dest_file_name}" # no this variable name isn't confusing at all!

    print(f"Copying {input_file} to {dest_file_full_path}! Get cozy now hehe")
    # copy the file to the destination
    copy_file(input_file, dest_file_full_path)

    # if there was a 2nd disc present, go ahead and copy that one over too
    if disc2_mode:
        # change game.iso to disc2.iso so nothing gets accidentally overwritten
        dest_file_full_path = f"{dest_file_path}/disc2.iso"

        print(f"Copying {disc2_file} to {dest_file_full_path}! Get cozy now hehe")
        copy_file(disc2_file, dest_file_full_path)

    print("Done! Thanks for using RVQuickCopy! x3")