with open("users.txt", "r") as f:
    userse = f.readlines()
    users = []
    for user in userse:
        users.append(user.split(":")[0])
print(users)