import json
import urllib.request
from pathlib import Path
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
def call(url,method="GET",data=None):
    payload=None if data is None else json.dumps(data).encode()
    request=urllib.request.Request(url,data=payload,method=method,headers={"Content-Type":"application/json"})
    with opener.open(request,timeout=10) as result:
        return result.status,json.load(result)
base="http://127.0.0.1:5000"
status, users=call(base+"/api/users")
assert status==200 and isinstance(users,list)
user={"name":"Lab8 verification","email":"lab8@example.com","phone":"12345678","address":"Beirut","country":"Lebanon"}
status,created=call(base+"/api/users/add","POST",user)
assert status==201
try:
    assert call(base+"/api/users/"+str(created["user_id"]))[1]["name"]==user["name"]
    created["name"]="Updated Lab8 verification"
    assert call(base+"/api/users/update","PUT",created)[1]["name"]==created["name"]
finally:
    assert call(base+"/api/users/delete/"+str(created["user_id"]),"DELETE")[0]==200
status,names=call("http://127.0.0.2:3000/get_users")
assert status==200 and names==["Omar","Ali","Sara"]
output="PASS: Lab 5 list, create, read, update, delete routes. Test user removed.\n"
output+="PASS: GET http://127.0.0.2:3000/get_users returned HTTP 200: "+json.dumps(names)+"\n"
Path("evidence/07-api-verification.txt").write_text(output,encoding="utf-8")
print(output)
