# Reliable File Transfer using UDP (URFT)

This program implements a Reliable File Transfer system using the User Datagram Protocol (UDP) to transfer files from a client to a server. The system is designed to handle issues such as packet loss and packet duplication, ensuring reliable data transmission over UDP.

## Requirements

- **Reliable Data Transfer**: The program ensures reliable data transmission, even in networks with packet loss or duplication.
- **Binary File Support**: Supports the transfer of binary files.
- **Command-Line Arguments**: The program accepts IP address and port as command-line arguments.
- **Linux Compatibility**: The program is designed to run on Linux-based systems.
- **Python Version**: Developed using Python 3.8 or later.
- **No External Dependencies**: The program runs without requiring additional libraries.
- **UDP Only**: Uses UDP as the only transport layer protocol.
- **Single Socket**: The server operates using a single socket throughout its execution.
- **File Limit**: Supports file transfers with a maximum of 2000 lines (as per project requirements).

## Program Files

- **urft_server.py**: The server program that listens for incoming file transfers.
- **urft_client.py**: The client program that sends files to the server.

## Usage Instructions

### 1. Start the Server
To start the server, run the following command in the terminal:

```bash
python urft_server.py <server_ip> <server_port>
```

### 2. Send a File from the Client
To send a file from the client to the server, run:

```bash
python urft_client.py <server_ip> <server_port> <file_path>
```
