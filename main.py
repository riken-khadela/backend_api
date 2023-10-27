import requests, datetime

response = requests.get('http://127.0.0.1:5000/api/get_response')
print(response.text)


# Append-adds at last
print('fffffffff')
file1 = open("myfile.txt", "a")  # append mode
file1.write(f"Today : {datetime.datetime.now()} \n")
file1.close()