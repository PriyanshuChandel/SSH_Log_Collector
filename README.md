# SSH Log Collector
SSH Log Collector is a GUI application used to collect different types of logs (basic and system logs) of the devices via SSH protocol. Additionally, it can collect custom logs provided by the user. The application is developed in Python and uses PySFTP to communicate with the remote devices. The graphical user interface (GUI) is developed using Tkinter.

### Dependencies
The application is developed in Python and requires the following packages:
- `Tkinter`: For the graphical user interface (GUI)
- `PySFTP`: For communicating with the remote devices via SSH protocol
- `Beautiful Soup`: For parsing the HTML data
- `Paramiko`: For the underlying SSH functionality

### Configuration
- data_path.conf
  - Define the path of basic logs and system logs
- EQPT.xml
  - Define the Equipment name and IP address
- ospf_ssh_private_key
  - Update it with the private keys to authenticate with remote host
- port.conf
  - Configure the port here, generally it will be 22 but define it accordingly
- usr.conf
  - Define the username here to authenticate with host
 
### Installation
- Clone the repository to your local machine using the following command:
  > `git clone https://github.com/Priyanshuuu/SSH-Log-Collector.git`
- Change the current directory to the cloned repository:
  > `cd SSH-Log-Collector`
- Run the application using the following command:
  > `python SSH-Logs-Collector.py`

### How to use
#### Main window
The main window of the application contains a total of 3 frames:
- **Frame 1**: Contains input fields for entering IP addresses in caxe system is not configured in EQPT.xml or getting used temprorarily.
- **Frame 2**: Contains checkboxes for selecting devices from the provided list (extracted from EQPT.xml).
- **Frame 3**: Contains buttons for collecting basic logs, system logs, and custom logs.

#### Enter details
To start the application, the user needs to enter the IP addresses of the devices to be logged in the IP Address entry field or select the devices from the provided list of checkboxes in Frame 2. 

#### Collect logs
After selecting the devices, the user can collect logs by clicking on the respective button in Frame 3:
- **Basic Logs**: Collects basic logs of the devices via SSH protocol and saves them in a zip file.
- **System Logs**: Collects system logs of the devices via SSH protocol and saves them in a zip file.
- **Custom Logs**: Collects custom logs provided by the user via SSH protocol and saves them in a zip file.

After clicking the button, the application will start collecting the logs of the selected devices and show the status of the log collection process in the status box.

### Contributions
Contributions to this repo are welcome. If you find a bug or have a suggestion for improvement, please open an issue on the repository. If you would like to make changes to the code, feel free to submit a pull request.

### Acknowledgments
This program was created as a part of a programming challenge. Special thanks to the challenge organizers for the inspiration.
