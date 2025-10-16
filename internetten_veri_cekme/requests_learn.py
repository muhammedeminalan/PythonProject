import requests
# URL
url="https://jsonplaceholder.typicode.com/posts"
# GET request
get_response= requests.get(url)
print(get_response.json())
# POST request
post_response= requests.post(url, data={"title": "foo", "body": "bar", "userId": 1})
print(post_response.json())
# PUT request
put_response= requests.put(url+"/1", data={"id": 1, "title": "foo", "body": "bar", "userId": 1})
print(put_response.json())
# DELETE request
delete_response= requests.delete(url+"/1")
print(delete_response.status_code)
# HEAD request
head_response= requests.head(url)
print(head_response.headers)
# OPTIONS request
options_response= requests.options(url)
print(options_response.headers)
# PATCH request
patch_response= requests.patch(url+"/1", data={"title": "foo"})
print(patch_response.json())
# AUTH request
auth_response= requests.get("https://httpbin.org/basic-auth/user/passwd", auth=('user', 'passwd'))
print(auth_response.json())
# TIMEOUT request
try:
    timeout_response= requests.get(url, timeout=0.001)
    print(timeout_response.json())
except requests.Timeout:
    print("The request timed out")
# SESSION request
session = requests.Session()
session.get("https://httpbin.org/cookies/set/sessioncookie/123456789")
session.get("https://httpbin.org/cookies")
print(session.cookies.get_dict())
print("--------------------------------------------------------------------------------------")







