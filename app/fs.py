# with open("data.txt","a") as file:
#     file.write("Testing the file module 2\n")
#     file.close()
# with open("data.txt","r") as f:
#     print(f.read())

import json

data = {
    "Wie heibt du?": "Ich heibe Sandhya",
    "Wie geht's dir?":"Mir geht's sehr gut, danke!",
    "Lass uns angangen!":"Ja"
}

# with open("data.json","w") as f:
#     json.dump(data,f, indent=4)

with open ("data.json","r") as f:
    print(json.load(f))