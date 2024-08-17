import socket
import os
import sys
import shutil

def connecting(server_ip, server_port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        file_to_upload = "Alons_morning.txt"
        file_to_download = "alons_life.txt"

        action = input("What do you want to do (download or upload): ").lower()

        client_socket.send(action.encode())

        if action.lower() == "download":
           
            client_socket.send(file_to_download.encode())
            confirmation = client_socket.recv(1024)
            if(confirmation.decode() == "ACK"):
                print("downaload started.")
                get_file(file_to_download, client_socket)
            else:
                print("File download canceld.")

        elif action.lower() == "upload":
            
            client_socket.send(file_to_upload.encode())
            confirmation = client_socket.recv(1024)
            if(confirmation.decode() == "ACK"):
                print("upload started.")
                send_file(file_to_upload, client_socket)
            else:
                print("File upload canceld.")

    except Exception as e:
        print(f"Error occurred while connecting: {e}")
        sys.exit(1)
    
    finally:
        print("Connection closed.")
        client_socket.close()


def get_file(file_to_download , client_socket):
    try:
            filename = input("Enter a name for the incoming file and its type: ")
            with open(filename, 'wb') as file:
                while True:
                    file_data = client_socket.recv(1024)
                    if not file_data:
                        break
                    file.write(file_data)
            print("File has been received successfully.")
            move_files_to_location(filename)
        
    
    except Exception as e:
        print(f"[ERROR]: {e}")
        sys.exit(1)

def move_files_to_location(filename):
    try:
        current_path = r"C:\\Alon VS Code\\"
        target_path = r"C:\\Users\\eyalm\\Desktop\\files_from_server\\"
        shutil.move(current_path + filename, target_path + filename)
    
    except Exception as e:
        print(f"[ERROR]: {e}")
        sys.exit(1)

def send_file(filename, client_socket):
    try:
        print(f"Sending file: {filename}")
        with open(filename, 'rb') as file:
            while True:
                file_data = file.read(1024)
                if not file_data:
                    break
                client_socket.sendall(file_data)
                print(f"Sent {len(file_data)} bytes")
            
            print("Data has been sent.")
            
    except Exception as e:
        print(f"[ERROR]: {e}")
        sys.exit(1)
        
if __name__== "__main__":
    SERVER_IP = "192.168.7.12"
    SERVER_PORT = 8965
    connecting(SERVER_IP, SERVER_PORT)