import uuid

def uuid_gen():
    return str(uuid.uuid4()).replace('-','')

if __name__ == '__main__':
    print(uuid_gen())