import os
import sys
import json
import subprocess


# Define the path to the Arduino CLI executable
arduino_cli_path = "/opt/homebrew/bin/arduino-cli"  # Replace with the actual path to arduino-cli

# Define a function for connecting to a remote server via SSH and executing multiple remote commands.
def ssh_connect(host, username, private_key, passphrase, remote_commands):
    try:
        # Loop through the list of remote commands to execute on the remote server.
        for remote_command in remote_commands:
            # Construct the SSH command to execute remotely, including the private key, host, and remote command.
            ssh_command = [
                "ssh",
                "-i", private_key,                 # Specify the private key for authentication.
                "-o", "StrictHostKeyChecking=no",    # Disable strict host key checking to avoid prompts.
                f"{username}@{host}",               # The SSH username and host to connect to.
                remote_command                      # The remote command to execute on the server.
            ]

            # Execute the SSH command using the subprocess module.
            result = subprocess.run(
                ssh_command,                      # Command to execute.
                capture_output=True,              # Capture the command's standard output.
                text=True,                        # Treat the output as text (string).
                check=True,                       # Raise an exception if the command returns a non-zero exit code.
                input=passphrase                  # Pass the private key passphrase as input.
            )

            # Print the output of the executed remote command.
            print(result.stdout)

    except subprocess.CalledProcessError as e:
        # Handle exceptions raised when the SSH command returns a non-zero exit code.
        print(f"An error occurred: {e.stderr}")

def transfer_file(ssh_host, ssh_username, target_file, destination_directory, private_key):

    # Construct the SCP command
    scp_command = [
        "scp",
        "-i", private_key,
        target_file,
        f"{ssh_username}@{ssh_host}:{destination_directory}"
    ]

    try:
        # Execute the SCP command
        subprocess.run(scp_command, check=True)
        print("File transfer successful.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"File transfer failed with error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
        

# Function to read the contents of a file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to write content to a file
def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# Function to compare two files and update the target file if they are different
def compare_and_update(source_file, target_file):
    source_content = read_file(source_file)
    target_content = read_file(target_file)

    if source_content == target_content:
        return False # if files are same
    else:
        write_file(target_file, source_content)
        return True # if files are different

# Function to get the fully-qualified board name (fqbn) and port for Arduino boards
def get_fqbn_and_port():
    try:
        # configure default port & fqbn
        dfqbn = "arduino:avr:mega"
        dport = "/dev/cu.usbmodem1101"
        # List all available boards using the Arduino CLI
        list_boards_command = f"{arduino_cli_path} board list --format json"
        boards_output = subprocess.check_output(list_boards_command, shell=True, text=True)

        # Parse the JSON output to get board information
        boards_info = json.loads(boards_output)

        for board_info in boards_info:
            port_info = board_info.get("port", {})
            matching_boards = board_info.get("matching_boards", [])

            for matching_board in matching_boards:
                fqbn = matching_board.get("fqbn", "")
                port = port_info.get("address", "")

                if fqbn and port:
                    return fqbn, port
        print("Defaulted Port & FQBN...")
        return dfqbn, dport 
    
    except subprocess.CalledProcessError as e:
        print(f"Exception while configuring Port & FQBN...{e}")
        return None, None

# Function to create and write Arduino code to a sketch file
def create_and_write_arduino_code(arduino_code, sketch_directory):
    # Create a directory for the sketch if it doesn't exist
    os.makedirs(sketch_directory, exist_ok=True)

    # Use the base name of the sketch directory as the sketch name
    sketch_name = f"{os.path.basename(sketch_directory)}.ino"

    # Define the sketch file path
    sketch_file = os.path.join(sketch_directory, sketch_name)

    # Write Arduino code to the sketch file
    with open(sketch_file, "w") as file:
        file.write(arduino_code)
    
    return sketch_file

# Function to compile an Arduino sketch
def compile_arduino_sketch(fqbn, sketch_file):
    try:
        # Compile the Arduino sketch using the Arduino CLI
        compile_command = f"{arduino_cli_path} compile --fqbn {fqbn} {sketch_file}"
        compile_process = subprocess.run([compile_command], check=True, shell=True, capture_output=True)

        if compile_process.returncode != 0:
            print("Compilation failed.")

        #compile_command = f"{arduino_cli_path} compile --fqbn {fqbn} {sketch_file}"
        #compile_process = subprocess.Popen(compile_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #compile_process.communicate()

        #if compile_process.returncode != 0:
            #print("Compilation failed.")
            #sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"Compilation failed with error: {e}")

    except Exception as e:
        print(f"An error occurred: ",e)

# Function to upload an Arduino sketch to a board
def upload_arduino_sketch(fqbn, port, sketch_directory):
    try:
        # Upload the compiled sketch using the Arduino CLI
        
        upload_command = f"{arduino_cli_path} upload --fqbn {fqbn} --port {port} {sketch_directory}"
        upload_process = subprocess.run([upload_command], check=True, shell=True, capture_output=True)

        if upload_process.returncode == 0:
            print("Upload successful.")
        else:
            print("Upload failed.")

        #upload_command = f"{arduino_cli_path} upload --fqbn {fqbn} --port {port} {sketch_directory}"
        #upload_process = subprocess.Popen(upload_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #upload_process.communicate()

        #if upload_process.returncode == 0:
            #print("Upload successful.")
        #else:
            #print("Upload failed.")

    except subprocess.CalledProcessError as e:
        print(f"Upload failed with error: {e}")

    except Exception as e:
        print(f"An error occurred: ",e)
