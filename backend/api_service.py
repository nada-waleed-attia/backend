import requests

def fetch_data():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"خطأ: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("خطأ في الاتصال:", e)
        return None