import socket


def get_current_ip():
    try:
        # Connect to a well-known service that echoes the client's IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to Google's DNS server, port 80
        public_ip = s.getsockname()[0]
        s.close()
        return public_ip
    except:
        return 'NOT FOUND'
