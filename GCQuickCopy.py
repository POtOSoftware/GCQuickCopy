import string
import sys
import os
import shutil
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

if __name__ == '__main__':
    # grab arguments and store them in a variable for elegance
    args = sys.argv
    input_file = args[1] # if the file isnt the first argument, blame the user!

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
    
    while True:
        # ask if the input file is the 2nd disc, default is NO
        disc2_input = input("Is this the 2nd disc? y/[N]").upper()
        if disc2_input in ['Y', 'N'] or disc2_input == '':
            break
        else:
            print("Please type Y or N! >~<")
    
    if disc2_input == 'y':
        print("Initiating disc 2 mode >:3")
        dest_file_name = "disc2.iso"
    
    # now we construct the destination file path
    dest_folder_name = Path(input_file).stem # remove the file extension from the input file
    print(dest_folder_name)
    dest_file_path = f"{dest_drive}games/{dest_folder_name}" # the final file destination path

    # create the destination directory
    os.makedirs(dest_file_path, exist_ok=True)

    dest_file_full_path = f"{dest_file_path}/{dest_file_name}" # no this variable name isn't confusing at all!

    print(f"Copying {input_file} to {dest_file_full_path}! Get cozy now hehe")
    # copy the file to the destination
    shutil.copyfile(input_file, dest_file_full_path)

    print("Done! Thanks for using RVQuickCopy! x3")