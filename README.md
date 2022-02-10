<div align="center">
  <img src="https://user-images.githubusercontent.com/84752451/153381548-b64ed2b9-5372-4cb2-bf6f-292ac16017e3.png" height="300">
  
  # oneclip
  
</div>
Shared clipboard experience between Windows and macOS/iOS

#  Installation
This script requires two computers, both with Python3 installed and pip3. If the computer OS combo is macOS to Windows and the Mac is logged into an iCloud account with an iOS or iPadOS device, three-dimensional clipboard will be achieved from PC<>Mac<>iOS/iPadOS. Each time the script connects to a peer, it exchanges a key that is used to cryptographically encrypt the clipboard as it is transmitted between peers (overkill i know).

## Dependencies
This script requires packages that can be found in the requirements.txt file.

## Variables
To set the IP Address and Port Number. Create a file in the root directory called 
```
.env
```
and paste this into it, modifying the values
```
HOST=ip_address_of_server
PORT=random_number_greater_than_1023
```

# Limitations
This script might be somewhat unstable and exhibit freezing. I am still working on making it more reliable. Consider this a beta release :stuck_out_tongue_winking_eye:. If that happens just quit the Python terminal and restart it. If it persists, or you have a different issue, submit an issue and i'll try my best to help.

# Purpose / My Motivation
I wanted a shared clipboard between my iPhone and Mac and PC. I know there is heaps of free software out there; I wanted something lightweight that I didn't have to install.
