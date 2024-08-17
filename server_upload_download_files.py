import socket
import os

def start_server(host, port, storage_path):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server started on {host}:{port}. Waiting for a connection...")

   
    client_socket, client_address = server_socket.accept()
    print(f"Client connected from: {client_address}")
    
    try:
        action = client_socket.recv(1024).decode()
        print(f"r")
        filename = client_socket.recv(1024).decode()
        file_path = os.path.join(storage_path, filename)
        
        file_exist = os.path.exists(file_path)
        

        if action.lower() == "upload":
            if file_exist:
                print("File already exsist upload cancled")
                client_socket.sendall(b'NACK')
            else:
                client_socket.sendall(b'ACK')
                print("File upload started.")
                receive_file(client_socket, file_path)

        elif action.lower() == "download":
            if file_exist:
                print("File transfer started.")
                client_socket.sendall(b'ACK')
                send_file(client_socket, file_path)
                
            else:
                client_socket.sendall(b'NACK')
                print("File download canceld.")
                
            
        else:
            print("Unknown command.")
            
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        print("Client disconnected.")
        client_socket.close()
        print("Connection closed.")
        server_socket.close()
            
        
def receive_file(client_socket, file_path):
    with open(file_path, 'wb') as file:
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            file.write(chunk)
            client_socket.sendall(b'ACK') 
        print("File upload complete.")

def send_file(client_socket, file_path):
    
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(1024)
                if not chunk:
                    break
                client_socket.sendall(chunk) 
        print("File download complete.")
   
if __name__ == "__main__":
    SERVER_IP = "192.168.7.12" 
    SERVER_PORT = 8965
    STORAGE_PATH = r"C:\Users\Mor Alon\Desktop\Storage_for_homework"  # Change to your desired storage path

    start_server(SERVER_IP, SERVER_PORT, STORAGE_PATH)