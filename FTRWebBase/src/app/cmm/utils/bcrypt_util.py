import os
import bcrypt 
from app import app
ROUNDS=5
# salt = bcrypt.gensalt()
# print(salt)
salt = b'$2b$05$frugyJd.fV8zeGjNk4MVJO'

def hash_pw(password):
    return bcrypt.hashpw(password.encode('utf-8'), salt)

if __name__ == '__main__':
    print(bcrypt.gensalt(ROUNDS))
    print(len(hash_pw('a')))
    print(hash_pw('a'))
    print(hash_pw('a'))
    print(hash_pw('a'))
    print()