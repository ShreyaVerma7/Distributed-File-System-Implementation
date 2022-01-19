import socket
import pickle

import random
from cryptography.fernet import Fernet

def pwd(file_name):
    if (file_name=="fs1"):
        full="File Server-1"

    elif(file_name=="fs2"):
        full="File Server-2"
    return("Your Present working directory is "+full+"\n")

def ls(file_name,my_files):
    if (file_name=="fs1"):
        full="File Server-1"

    elif(file_name=="fs2"):
        full="File Server-2"
    files=""
    for i in my_files:
        files=files+"\n\t"+str(i)
    return(full + " contains : " +files+"\n")

def cat(file_to_read,my_files):
    if (file_to_read not in my_files):
        return ("This file is not present in this file server "+"\n")
    else:
        f=open(file_to_read,"r")
        response="Contents of " +file_to_read +" are :\n"+f.read()+"\n"
        f.close()
        return(response)
def cp(file_to_copy,my_files,file_name):
    my_files.append(file_to_copy)
    response=file_to_copy+" copied to " +file_name+"\n"
    return(response)
def add(file_to_add,content_of_file,my_files):
    fa = open(file_to_add, "w+")
    fa.write(content_of_file)
    fa.close()
    my_files.append(file_to_add)
    response=file_to_add+" has been added to this file server"+"\n"
    return([response,my_files])

ip='127.0.0.1'
print("What is port number of this file server? : ")
my_port=int(input())
print("What is port number of Key Distribution Server? : ")
kdsp=int(input())
kds=('127.0.0.1',kdsp)

my_addr=('127.0.0.1',my_port)
file=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
file.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
file.bind(my_addr)
keys={}
my_info=pickle.dumps(my_port)
file.sendto(my_info,kds)
message=file.recvfrom(4096)
my_files=[]
keys['kds']=Fernet(message[0])
file_numb=file.recvfrom(4096)
file_numb=int(file_numb[0].decode())
if (file_numb==1):
    file_name='fs1'
    fa=open("file 1.txt","w+")
    fa.write("This is file 1.txt")
    fb=open("file 2.txt","w+")
    fb.write("This is file 2.txt")
    fa.close()
    fb.close()
    my_files=["file 1.txt","file 2.txt"]
elif(file_numb==2):
    file_name='fs2'
    fa=open("file 3.txt","w+")
    fa.write("This is file 3.txt")
    fb=open("file 4.txt","w+")
    fb.write("This is file 4.txt")
    fa.close()
    fb.close()
    my_files=["file 3.txt","file 4.txt"]
my_files_info=pickle.dumps(my_files)
file.sendto(my_files_info,kds)
while (True):
    enc_message=file.recvfrom(4096)
    enc_message=pickle.loads(enc_message[0])
    key_kds=keys['kds']
    message=[]
    for i in range (3):
        message.append(key_kds.decrypt(enc_message[i]))
        message[i]=message[i].decode()
    session_key=Fernet(message[0])
    client_location=(ip,int(message[1]))
    client_name=message[2]
    keys[client_name]=session_key


    def gen_nonce():
        return (random.randint(1, 10000))
    nonce=gen_nonce()
    enc_nonce=session_key.encrypt(str(nonce).encode())
    file.sendto(enc_nonce,client_location)
    nonce_from_client=file.recvfrom(4096)
    dec_nonce=session_key.decrypt(nonce_from_client[0])
    recv_nonce=dec_nonce.decode()
    if (int(recv_nonce)==nonce-1):
        print(client_name +" is verified ")
        file.sendto(str(1).encode(),client_location)
        while (True):
            action_message=file.recvfrom(4096)
            action_message=pickle.loads(action_message[0])
            if((session_key.decrypt(action_message[0])).decode()=='y'):
                action=(session_key.decrypt(action_message[1])).decode()
                if (action=='pwd'):
                    response=pwd(file_name)
                    response=session_key.encrypt(response.encode())
                    file.sendto(response,client_location)
                if (action=='ls'):
                    response=ls(file_name,my_files)
                    response = session_key.encrypt(response.encode())
                    file.sendto(response, client_location)
                if(action=='cat'):
                    file_to_read=(session_key.decrypt(action_message[2])).decode()
                    response = cat(file_to_read, my_files)
                    response = session_key.encrypt(response.encode())
                    file.sendto(response, client_location)
                if(action=='cp'):
                    file_to_copy=(session_key.decrypt(action_message[2])).decode()
                    message=[file_name,action]
                    message=pickle.dumps(message)
                    file.sendto(message,kds)
                    other_server_info=file.recvfrom(4096)
                    other_server_info=pickle.loads(other_server_info[0])
                    dec_other_server_info=[]
                    for i in other_server_info:
                        dec_other_server_info.append((key_kds.decrypt(i)).decode())
                    if file_to_copy not in my_files:
                        if file_to_copy not in dec_other_server_info:
                            response="This file is not in the other file server \n (Use add function to add this file)"+"\n"
                            response = session_key.encrypt(response.encode())
                            file.sendto(response, client_location)
                        else:
                            response=cp(file_to_copy,my_files,file_name)
                            response = session_key.encrypt(response.encode())
                            file.sendto(response, client_location)
                    else:
                        response="File with this name is already in this server "+"\n"
                        response = session_key.encrypt(response.encode())
                        file.sendto(response, client_location)
                if (action=="add"):
                    file_to_add = (session_key.decrypt(action_message[2])).decode()
                    content_of_file = (session_key.decrypt(action_message[3])).decode()
                    if(file_to_add in my_files):
                        response="File with this name is already present inside the server, choose a different name "+"\n"
                        response = session_key.encrypt(response.encode())
                        file.sendto(response, client_location)
                    else:
                        result=add(file_to_add,content_of_file,my_files)
                        response=result[0]
                        my_files=result[1]
                        response = session_key.encrypt(response.encode())
                        file.sendto(response, client_location)
            elif((session_key.decrypt(action_message[0])).decode()=='n'):
                break

    else:
        print("Client not verified as nonce not correct")
        file.sendto(str(0).encode(), client_location)


