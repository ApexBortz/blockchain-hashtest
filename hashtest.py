# python's build in hash library
import hashlib

# encode a string == encode to UTF-8
encode = 'B'.encode() # no args = UTF-8
# str(10).encode()
# 'digest' into a hash
digest = hashlib.sha256(encode).hexdigest()
print(digest)
digest = hashlib.sha256(encode).hexdigest()
print(digest)
digest = hashlib.sha256(encode).hexdigest()
print(digest)
digest = hashlib.sha256(encode).hexdigest()
print(digest)

print(digest == hashlib.sha256('B'.encode()).hexdigest())