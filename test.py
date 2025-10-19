class idk:
    def __init__(self, dictionary):
        self.dict = dictionary
    def gain(self, abi):
        self.dict.update(abi)

yes = {"1": {"hi": 5}}
hello = idk({"5":{"bye": 2}})
hello.gain(yes)
print(f"he {list(hello.dict.keys())[0]}")