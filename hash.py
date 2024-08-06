import hashlib

def hash_string(string):
    return hashlib.sha256(string.encode()).hexdigest()


print(hash_string("hello"))