import socket
import pickle
import random
from cryptography.fernet import Fernet

ip='127.0.0.1' #local address
print("What is port number of this Key Distribution Server? : ")
my_port=int(input())

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1',my_port))


fileserver_info={}
fileserver_count=0
clientserver_info={}
clientserver_count=0


#put for loop for 2 file servers

fileserver1_data=s.recvfrom(4096)

fileserver_info['fs1']=[(pickle.loads(fileserver1_data[0])),'tempkey',[]]
kds_fs1=Fernet.generate_key()
fileserver_info['fs1'][1]=Fernet(kds_fs1)
#store symmetric key for fileserver

print("File Server 1 port number "+str(fileserver_info['fs1'][0]))
fileserver_count=fileserver_count+1
s.sendto(kds_fs1,(ip,fileserver_info['fs1'][0]))#send key back
s.sendto(str(fileserver_count).encode(),(ip,fileserver_info['fs1'][0]))
info_files_stored=s.recvfrom(4096)
fileserver_info['fs1'][2]=pickle.loads(info_files_stored[0])

#store info for flies here and second file server


#for loop for 3 clients

client1_data=s.recvfrom(4096)
clientserver_info['cs1']=[(pickle.loads(client1_data[0])),'tempkey']
kds_cs1=Fernet.generate_key()

clientserver_info['cs1'][1]=Fernet(kds_cs1)#store symmetric key for client

clientserver_count=clientserver_count+1
print("Client 1 port number "+str(clientserver_info['cs1'][0]))
s.sendto(kds_cs1,(ip,clientserver_info['cs1'][0]))#send key back
s.sendto(str(clientserver_count).encode(),(ip,clientserver_info['cs1'][0]))
file_info_to_client=""
for i in fileserver_info:
    file_info_to_client=file_info_to_client+i+" contains : "
    for j in fileserver_info[i][2]:
        file_info_to_client=file_info_to_client+"\n\t" + j
    file_info_to_client = file_info_to_client+"\n"
s.sendto(str(file_info_to_client).encode(),(ip,clientserver_info['cs1'][0]))

#address and port number of all clients and file servers recieved and files stored in all file servers

#now client wants to access file server
#use while true for multiple
fileserver_info['fs2']=[4005,'garbage_key',["file 3.txt","file 4.txt"]]
while (True):
    message_info=s.recvfrom(1024)
    message=pickle.loads(message_info[0])
    if message[0] in clientserver_info:#when client wants to access file server
        print((message[0]) + " wants to access "  + (message[1]))
        session_key=Fernet.generate_key()

        cs=message[0]#client name
        fs=message[1]#file name
        nonce=message[2]#nonce

        cp=clientserver_info[cs][0]#client port
        fp=fileserver_info[fs][0]#file port

        ck=clientserver_info[cs][1]#client key
        fk=fileserver_info[fs][1]#file key

        response=[]
        response.append(ck.encrypt(str(nonce).encode()))
        response.append(ck.encrypt(session_key))
        response.append(ck.encrypt(str(fp).encode()))
        response.append(ck.encrypt(fk.encrypt(session_key)))
        response.append(ck.encrypt(fk.encrypt(str(cp).encode())))
        response.append(ck.encrypt(fk.encrypt(cs.encode())))

        response=pickle.dumps(response)
        s.sendto(response,(ip,cp))
    elif message[0] in fileserver_info:
        fs_name=message[0]
        fs_loc=fileserver_info[fs_name][0]
        fs_key=fileserver_info[fs_name][1]
        if message[1]=='cp':

            other_server_files=[]
            enc_other_server_files=[]
            for i in fileserver_info:
                if (i!=fs_name):
                    other_server_files=fileserver_info[i][2]
                else:
                    continue
            for k in other_server_files:
                enc_other_server_files.append(fs_key.encrypt(k.encode()))
            enc_other_server_files=pickle.dumps(enc_other_server_files)
            s.sendto(enc_other_server_files,(ip,fs_loc))














