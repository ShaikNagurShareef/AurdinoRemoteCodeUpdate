import os
from utils import get_fqbn_and_port, create_and_write_arduino_code, compile_arduino_sketch, upload_arduino_sketch


try:

    # Configure target file name
    target_file = "arduino_code.ino"

    # Get the home directory path
    home_directory = os.path.expanduser("~")

    # Arduino code filename on remote machine
    arduino_code_filename = target_file#"/Users/tejacherukuri/"+target_file

    # Specify the sketch and folder name
    sketch_name = "my_sketch"

    # Arduino sketch directory
    sketch_directory = os.path.join(home_directory, sketch_name)

    # Arduino sketch code
    with open(arduino_code_filename, "r") as arduino_code_file:
        arduino_code = arduino_code_file.read()

    # Get the Fully Qualified Board Name (FQBN) and Port
    fqbn, port = get_fqbn_and_port()

    sketch_file = create_and_write_arduino_code(arduino_code, sketch_directory)
    compile_arduino_sketch(fqbn, sketch_file)
    upload_arduino_sketch(fqbn, port, sketch_directory)

except Exception as e:
    print(f"An error occurred: ",e)
