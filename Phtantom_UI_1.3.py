import serial
import time
import serial.tools.list_ports
from datetime import datetime
import os

# List available COM ports and allow the user to select the Arduino's COM port
ports = serial.tools.list_ports.comports()
portsList = []

print("Available COM Ports:")
for index, port in enumerate(ports):
    portsList.append(port.device)
    print(f"{index + 1}: {port.device} - {port.description}")

try:
    com_index = int(input("Select COM Port for Arduino (e.g., 1 for COM3): ")) - 1
    if 0 <= com_index < len(portsList):
        use = portsList[com_index]
        print("Selected port:", use)
        print("Please select the same port in the Arduino UI!")
        print()
    else:
        print("Invalid selection. Please run the script again and select a valid COM port number.")
        exit()
except ValueError:
    print("Invalid input. Please enter a number.")
    exit()

# Setup serial connection with the selected COM port
try:
    ser = serial.Serial(use, 9600, timeout=1)
    time.sleep(2)  # Wait for the connection to establish 
except Exception as e:
    print(f"Error connecting to {use}: {e}")
    exit()

def request_sensor_data():
    ser.write("READ\n".encode())
    while ser.in_waiting <= 0:
        time.sleep(0.1)
    data = ser.readline().decode().strip()
    print(f"Received sensor data: {data}")  # Debugging print
    return data 

def update_conditions(conditions):
    # Unpack the conditions
    servo1, servo2, servo3, pump_rate_left, pump_rate_right, fluid_temp = conditions

    # Convert servo positions from float to integer if necessary
    servo1 = int(servo1)
    servo2 = int(servo2)
    servo3 = int(servo3)

    # Construct the command string with all conditions, including servo positions
    command = f"{servo1},{servo2},{servo3},{pump_rate_left},{pump_rate_right},{fluid_temp}\n"
    
    # Send the command to Arduino
    ser.write(command.encode())
    ser.flush()  # Ensure the command is processed
    time.sleep(1)  # Wait for the Arduino to respond

    # Attempt to read the response from Arduino
    response = ser.readline().decode().strip()
    print(f"Arduino response: {response}")

def collect_and_send_conditions():
    inputs = {
        "Enter servo PV position (10-100%)": None,
        "Enter servo CR1 position (0-100%)": None,
        "Enter servo CR2 position (10-100%)": None,
        "Enter left pump rate (L/min)": None,
        "Enter right pump rate (L/min)": None,
        "Enter fluid temperature in Celsius": None
    }
    
    for prompt in inputs:
        while True:
            user_input = input(f"{prompt}: ")
            try:
                value = float(user_input)  # Attempt to convert input to float
                
                # Special check for servo PV and CR2 positions to be within 10-100%
                if "PV position" in prompt or "CR2 position" in prompt:
                    if not (10 <= value <= 100):
                        print("Error: Servo PV and CR2 positions must be between 10 and 100%.")
                        continue
                
                # Check for servo CR1 positions to be within 0-100%
                elif "CR1 position" in prompt:
                    if not (0 <= value <= 100):
                        print("Error: Servo CR1 position must be between 0 and 100%.")
                        continue
                
                # Check for pump rates and fluid temperature to be positive
                elif ("rate" in prompt or "temperature" in prompt) and value < 0:
                    print("Error: Pump rates and fluid temperature must be positive.")
                    continue
                
                inputs[prompt] = value  # Store valid input
                break  # Exit loop on valid input
                
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    # Directly unpack and return validated values
    servo1, servo2, servo3, pump_rate_left, pump_rate_right, fluid_temp = tuple(inputs.values())
    
    return servo1, servo2, servo3, pump_rate_left, pump_rate_right, fluid_temp

def format_table(conditions, sensor_data=",,,,,"):
    try:
        # Attempt to split and unpack the sensor data
        flow1, flow2, flow3, pressure1, pressure2, pressure3 = sensor_data.split(',')
    except ValueError:
        # Handle cases where sensor data is not as expected
        flow1 = flow2 = flow3 = pressure1 = pressure2 = pressure3 = "N/A"
        print("Warning: Received incomplete sensor data.")

    servo1, servo2, servo3, pump_rate_left, pump_rate_right, fluid_temp = conditions
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = (
        f"Timestamp: {timestamp}\n"
        f"Port selected: {use}\n"
        "Output Name                  | Reading\n"
        "-----------------------------|----------------\n"
        f"Servo PV Openness (%)        | {servo1}\n"
        f"Servo CR1 Openness (%)       | {servo2}\n"
        f"Servo CR2 Openness (%)       | {servo3}\n"
        f"Left Pump Rate (L/min)       | {pump_rate_left}\n"
        f"Right Pump Rate (L/min)      | {pump_rate_right}\n"
        f"Fluid Temperature (°C)       | {fluid_temp} \n"
        f"FL1 Rate (L/min)             | {flow1}\n"
        f"FL2 Rate (L/min)             | {flow2}\n"
        f"FL3 Rate (L/min)             | {flow3}\n"
        f"P1 Pressure (mmHg)           | {pressure1}\n"
        f"P2 Pressure (mmHg)           | {pressure2}\n"
        f"P3 Pressure (mmHg)           | {pressure3}\n"
        "-----------------------------|----------------\n"
    )
    return output

def beta_run(conditions):
    update_conditions(conditions)
    # Generate and print the table with current conditions
    output = format_table((int(conditions[0]), int(conditions[1]), int(conditions[2]), float(conditions[3]), float(conditions[4]), float(conditions[5])), '-,-,-,-,-,-')
    print(output)
    # Define the beta output filename
    script_dir = os.path.dirname(os.path.realpath(__file__))
    beta_filename = os.path.join(script_dir, datetime.now().strftime("Beta Output - %Y-%m-%d - %Hh%Mm%Ss.txt"))
    # Log the output to the beta-specific file
    with open(beta_filename, "a") as file:
        file.write(output + "\n")

def main():
    # Setup initial conditions
    conditions = collect_and_send_conditions()
    # Initialize the positions of the servo motors
    update_conditions(conditions)
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Filename for storing the output, ensuring it's created in the same folder as the script
    filename = os.path.join(script_dir, datetime.now().strftime("Output - %Y-%m-%d - %Hh%Mm%Ss.txt"))
    while True:
        print("\n1. Get sensor readings")
        print("2. Update inputted conditions")
        print("3. Beta run")
        print("4. Exit")
        print()
        user_choice = input("What would you like to do? ")
        print()
        if user_choice == '1':
            # Request sensor data and print it
            sensor_data = request_sensor_data()
            output = format_table(conditions, sensor_data)
            print(output)
            print()
            with open(filename, "a") as file:
                file.write(output + "\n")
            print("Sensor data received successfully!")
            print()
        elif user_choice == '2':
            # Update conditions
            conditions = collect_and_send_conditions()
            update_conditions(conditions)
            output = format_table(conditions)
            with open(filename, "a") as file:
                file.write(output + "\n")
            print("Conditions updated successfully!")
            print()
        elif user_choice == '3':
            # Beta run
            beta_run(conditions)
            print("Beta run executed successfully!")
            print()
        elif user_choice == '4':
            # Exit the program
            print("Exiting.")
            print()
            return
        else:
            print("Invalid input. Please enter a valid option.")
            print()

if __name__ == "__main__":
    main()

