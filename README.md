# T-Mac-Changer

**T-Mac-Changer** is a powerful tool that allows you to easily change the MAC address of any network interface on Linux systems.

## Requirements

[python-3](https://example.com)

## Installation

**1. Clone this repo:**

<pre>git clone https://github.com/tuncay-khalisov/T-Mac-Changer</pre>

**2. Move into the project directory:**

<pre>cd T-Mac-Changer</pre>

**3. Run code:**

<pre>python3 t-mac-changer.py <options></pre>

## Available Options

<pre>
-h, --help              Show this help message and exit
-i, --interface         Interface name
-m, --mac               Set a MAC address manually
-r, --random            Set a random MAC address
--history               History
--restore               Restore MAC address  
</pre>

## Usage

<pre>python3 t-mac-changer.py -i <interface> -m <MAC> </pre>

Random MAC address

<pre>python3 t-mac-changer.py -i <interface> --random </pre>

Show MAC address history

<pre>python3 t-mac-changer.py -i <interface> -m <MAC> --history </pre>

Restore MAC address

<pre>python3 t-mac-changer.py -i <interface> --restore </pre>
