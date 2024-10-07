#!/bin/bash

# Define the serial port
PORT="/dev/ttyACM2"

# Upload the file using ampy
ampy -p $PORT put main.py

# Use picocom to send the import command
# Note: You might need to adjust the delay and escape sequences based on your microcontroller's response time
(
  sleep 3
  echo -e "\r\nimport main\r\n"
) | picocom $PORT

picocom $PORT