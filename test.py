from cryptography.fernet import Fernet
key=Fernet.generate_key()
f=Fernet(key)
bi=Fernet.generate_key()
b=Fernet(bi)
str='abhgn'
ab=f.encrypt(b.encrypt(str.encode()))
print(bi)
ga=f.encrypt(bi)
print(ga)
kab=f.decrypt(ab)
kab=b.decrypt(kab)
print(kab)
print(kab.decode())