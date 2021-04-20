class ClientDisconnectError(Exception):
	pass
class ServerDisconnectError(Exception):
	pass

import json

#byteArray = b'[{"Name": "Bence Fabo", "RoomID": 2}, {"Name": "Gellert Csapodi", "RoomID": 3}]'

#print(byteArray)
#string = byteArray.decode('utf-8')
#json_file = json.loads(string)
#print(json_file)
#print(type(json_file[0]))
#s = json.dumps(json_file,indent=4)
#print(s)
#
#myDict = {"Name": "Bence Fabo",
#		  "RoomID": 6}
#print(myDict.get("Nam"), type(myDict.get("RoomID")))
#dict_json = json.dumps(myDict, indent=4)
#print(dict_json)