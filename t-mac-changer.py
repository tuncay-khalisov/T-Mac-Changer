## Import Modules
import subprocess
import optparse
import re
import random
import os

## Get User Input
def get_user_input():

    parse_object = optparse.OptionParser()
    parse_object.add_option("-i","--interface",dest="interface",help="Interface name")
    parse_object.add_option("-m","--mac",dest="mac_address",help="Set a MAC address manually")
    parse_object.add_option("-r","--random",action="store_true",dest="random_mac",help="Set a random MAC address")
    parse_object.add_option("--history",action="store_true",dest="history",help="History")
    parse_object.add_option("--restore",action="store_true",dest="restore_mac",help="Restore MAC address")

    return parse_object.parse_args()

## Get Available Interfaces
def get_available_interfaces():
    try:
        interfaces = subprocess.check_output(["ip","link","show"],text = True)
        interface_list = re.findall(r"\d+: (\w+):", interfaces)
        return interface_list
    except subprocess.CalledProcessError as e:
        print(f"Error Getting Interfaces: {e}")
        return []

## Changing MAC Address
def change_mac_address(user_interface,user_mac_address):
    try:
        subprocess.call(["ip", "link", "set", user_interface, "down"])
        subprocess.call(["ip", "link", "set", "dev", user_interface, "address", user_mac_address])
        subprocess.call(["ip", "link", "set", user_interface, "up"])
    except subprocess.CalledProcessError as e:
        print(f"Error changing MAC address: {e}")

## Control New MAC Address
def control_new_mac(interface):
    try:
        ip = subprocess.check_output(["ip", "a", "show", interface], text=True)
        new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ip))
        if new_mac:
            return new_mac.group(0)
        else:
            print("MAC address not found!")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

## Generating Random MAC Address
def random_mac():
    r_mac = []
    for i in range(6):
        r_mac.append(f"{random.randint(0, 255):02x}")
    r_mac[0] = f"{int(r_mac[0], 16) & 0xfe:02x}"
    return ":".join(r_mac)

## Chack User Inputs
def check_user_inputs(user_input):
    if user_input.mac_address and user_input.random_mac:
        print("Error: You cannot use both --random (-r) and --mac (-m) options at the same time.")
        return False
    
    if user_input.mac_address and user_input.restore_mac:
        print("Error: You cannot use both --restore and --mac (-m) options at the same time.")
        return False

    if user_input.random_mac and user_input.restore_mac:
        print("Error: You cannot use both --random (-r) and --restore options at the same time.")
        return False

def main():
    print("T-Mac-Changer started!")

    (user_input,arguments) = get_user_input()

    ## Checking User Inputs
    if check_user_inputs(user_input) == False:
        return
    

    ## User Interface and User MAC ADDRESS are requireds
    if not user_input.interface or (not user_input.mac_address and not user_input.random_mac):
        print("Please provide both an interface (-i) and a MAC address (-m), or use the --random option.")
        return

    available_interfaces = get_available_interfaces()

    if user_input.interface not in available_interfaces:
        print(f"Error: Interface '{user_input.interface}' not found !!")
        return
    
    if user_input.random_mac:
        user_input.mac_address = random_mac()

    if user_input.restore_mac:
        if os.path.exists('history.txt'):
            with open('history.txt', 'r') as read_file:
                data = read_file.read()
                data_list = data.split("\n")
                user_input.mac_address = data_list[-1] if data_list[-1] else random_mac()  # Take the last valid MAC
                print("MAC address restored!!")
        else:
            print("Error: history.txt file not found!")
            return

    change_mac_address(user_input.interface, user_input.mac_address)

    ## Verify MAC Address
    finalized_mac = control_new_mac(user_input.interface)
    if finalized_mac == user_input.mac_address:
        print(f"Success! Your new MAC address: {finalized_mac}")
        with open('history.txt', 'a') as write_file:
            write_file.write(finalized_mac + '\n')
    else:
        print("Error: MAC address change failed!")

    if user_input.history:
        if os.path.exists('history.txt'):
            with open('history.txt', 'r') as read_file:
                print(f"\n-- History --\n{read_file.read()}")
        else:
            print("Error: history.txt file not found!")


if __name__ == "__main__":
    main()