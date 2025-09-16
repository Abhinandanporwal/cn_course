import socket

HOST, PORT = "127.0.0.1", 9090

def handle_client(conn):
    request = conn.recv(1024).decode("utf-8")
    print("Request:\n", request)

    headers = request.split("\r\n")
    cookie = None
    for header in headers:
        if header.startswith("Cookie:"):
            cookie = header.split(":", 1)[1].strip()

    if cookie:
        response_body = f"<html><body><h1>Welcome back! Your cookie: {cookie}</h1></body></html>"
    else:
        cookie_value = "User123"
        response_body = f"<html><body><h1>Welcome, new user! Setting cookie = {cookie_value}</h1></body></html>"

    response_headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/html; charset=utf-8",
        f"Content-Length: {len(response_body)}",
    ]

    if not cookie:
        response_headers.append("Set-Cookie: user=User123")

    response = "\r\n".join(response_headers) + "\r\n\r\n" + response_body
    conn.sendall(response.encode("utf-8"))
    conn.close()

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"Cookie Server running on http://{HOST}:{PORT}")
        while True:
            conn, _ = server.accept()
            handle_client(conn)
