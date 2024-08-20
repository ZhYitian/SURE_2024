import serial
import time
import serial.tools.list_ports

# Constants for flow rate calculations
CALIBRATION_FACTOR = 98  # The calibration factor for the flow sensor, same as Arduino interface
SECONDS_PER_MINUTE = 60

# List available COM ports and allow the user to select the Arduino's COM port
ports = serial.tools.list_ports.comports()
portsList = []

# The COM Ports connection can be varied between laptop system. 
print("Available COM Ports:")
for index, port in enumerate(ports):
    portsList.append(port.device)
    print(f"{index + 1}: {port.device} - {port.description}")

try:
    com_index = int(input("Select COM Port for Arduino (e.g., 1 for COM3): ")) - 1
    if 0 <= com_index < len(portsList):
        use = portsList[com_index]
        print("Selected port:", use)
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

def set_servo_position(servo_index, percent):
    command = f"SERVO {servo_index} {percent}\n"
    ser.write(command.encode())
    ser.flush()
    time.sleep(1)
    while ser.in_waiting > 0:
        response = ser.readline().decode().strip()
        if response:
            print(f"Arduino response: {response}")

def get_flow_rate():
    ser.write("FLOW\n".encode())
    ser.flush()
    time.sleep(2)  # Increase delay to ensure Arduino has enough time to measure and respond
    while ser.in_waiting == 0:
        time.sleep(0.1)
    while ser.in_waiting > 0:
        response = ser.readline().decode().strip()
        if response.startswith("FLOW"):
            try:
                pulse_count = int(response.split()[1])
                return pulse_count
            except ValueError:
                print(f"Unexpected response format: {response}")
                return None
        else:
            print(f"Unexpected response: {response}")
            return None

def calculate_flow_rate(pulse_count):
    flow_rate = (pulse_count / CALIBRATION_FACTOR)
    return flow_rate

def calculate_volume(flow_rate):
    volume = (flow_rate / SECONDS_PER_MINUTE) * 1000  # Convert to mL
    return volume

def calculate_volume(flow_rate):
    volume = (flow_rate / SECONDS_PER_MINUTE) * 1000  # Convert to mL
    return volume

def main():
    total_volume = 0

    while True:
        print("\n1. Set servo position")
        print("2. Get flow rate")
        print("3. Exit")
        user_choice = input("What would you like to do? ")
        if user_choice == '1':
            servo_index = input("Enter servo index (0 for PV, 1 for CR1, 2 for CR2): ")
            percent = input("Enter servo position (0-100%): ")
            set_servo_position(servo_index, percent)
        elif user_choice == '2':
            pulse_count = get_flow_rate()
            if pulse_count is not None:
                flow_rate = calculate_flow_rate(pulse_count)
                volume = calculate_volume(flow_rate)
                total_volume += volume

                print(f"Flow rate: {flow_rate:.2f} L/min, Volume this second: {volume:.2f} mL, Total volume: {total_volume:.2f} mL")
            else:
                print("Failed to read flow rate.")
        elif user_choice == '3':
            print("Exiting.")
            ser.close()
            break
        else:
            print("Invalid input. Please enter a valid option.")

if __name__ == "__main__":
    main()
