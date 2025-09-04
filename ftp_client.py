from ftplib import FTP

def ftp_client():
    ftp_server = "ftp.dlptest.com"
    username = "dlpuser"
    password = "rNrKYTX9g7z3RgJRmxWuGHbeu"

    try:
        ftp = FTP(ftp_server)
        ftp.login(user=username, passwd=password)
        print("Connected to FTP server")
        print("Directory Listing:")
        ftp.retrlines("LIST")
        with open("test_upload.txt", "w") as f:
            f.write("This is a test file for FTP upload.\n")
        with open("test_upload.txt", "rb") as f:
            ftp.storbinary("STOR test_upload.txt", f)
        print("File uploaded successfully.")
        with open("downloaded.txt", "wb") as f:
            ftp.retrbinary("RETR test_upload.txt", f.write)
        print("File downloaded successfully.")
        ftp.quit()
    except Exception as e:
        print("FTP Error:", e)
if __name__ == "__main__":
    ftp_client()
