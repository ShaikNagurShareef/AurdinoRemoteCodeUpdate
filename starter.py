import os
from utils import ssh_connect, compare_and_update, get_fqbn_and_port, create_and_write_arduino_code, compile_arduino_sketch, upload_arduino_sketch, transfer_file

try:
    # source file path
    source_file = "/Users/nagurshareefshaik/Desktop/MSCS/MORSE Studio - GRA/RemoteCodeUpdate/updated_code.ino"

    # target file path
    target_file = "/Users/nagurshareefshaik/Desktop/MSCS/MORSE Studio - GRA/RemoteCodeUpdate/arduino_code.ino"

    # Destination server details
    host = "Tejas-Air.wifi.gsu.edu" #"10.0.0.78" #"Tejas-Air.wifi.gsu.edu"
    username = "tejacherukuri"
    private_key = "/Users/nagurshareefshaik/.ssh/id_arduino_teja"

    # passphrase to decrypt the private key
    passphrase = "ghs@195L" #getpass.getpass("Enter the passphrase for your private key: ")

    # file transfer details
    code_loc = "/Users/tejacherukuri/Shareef/RemoteCodeUpdate/"
    remote_directory = "/Users/tejacherukuri/Shareef/CodeFiles/"
    local_file = "/Users/nagurshareefshaik/Desktop/MSCS/MORSE Studio - GRA/RemoteCodeUpdate/arduino_code.ino" # same as target file

    # compare and check if the target file is updated
    update_flag = compare_and_update(source_file, target_file)

    # command to trigger the Python script
    trigger_py_script = f"python3 {code_loc}update_code_runner.py"

    # List of remote commands to run (replace with your desired commands)
    remote_commands = [trigger_py_script]

    # If the code is updated, then do SSH, move the updated code to the remote, compile, and upload Arduino code
    if update_flag:
        # transfer code file to remote
        file_transfer = transfer_file(host, username, local_file, remote_directory, private_key)

        # If file trasfer is success, do ssh & upload the script to arduino
        if file_transfer:
            # do SSH and execute commands
            ssh_connect(host, username, private_key, passphrase, remote_commands)

except Exception as e:
    print(f"An error occurred: {e}")
