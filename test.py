hello = {"hi": 1, "hello": 2}
bob = {"hi": 3, "hello": 4}

def check(d1, d2):
    if list(d2.keys())[0] not in d1.keys():
        print("yay")
check(hello, bob)