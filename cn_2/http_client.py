import requests

def http_client():
    url = "https://httpbin.org/get"
    post_url = "https://httpbin.org/post"

    try:
        print("HTTP GET Request")
        response = requests.get(url)
        print("Status Code:", response.status_code)
        print("Headers:", response.headers)
        print("Body:", response.text[:200], "...")  
        print("\nHTTP POST Request")
        data = {"name": "Abhinandan", "msg": "Hello World"}
        response = requests.post(post_url, data=data)
        print("Status Code:", response.status_code)
        print("Headers:", response.headers)
        print("Body:", response.text[:200], "...")

    except requests.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    http_client()
