import requests

url = "http://127.0.0.1:8000/upload/"
file_path = "videos/video.mp4"

with open(file_path, "rb") as video_file:
    response = requests.post(url, files={"video": video_file})

print(response.status_code)
print(response.json())
