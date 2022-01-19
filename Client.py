import socket
import pickle
import random
from cryptography.fernet import Fernet

ip='127.0.0.1'
print("What is port number of this Client server? : ")
my_port=int(input())
print("What is port number of Key Distribution Server? : ")
kdsp=int(input())
kds=('127.0.0.1',kdsp)
my_addr=('127.0.0.1',my_port)
client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.bind(my_addr)
keys={}
my_info=pickle.dumps(my_port)
client.sendto(my_info,kds)
message=client.recvfrom(4096)
keys['kds']=Fernet(message[0])
client_numb=client.recvfrom(4096)
client_numb=int(client_numb[0].decode())
file_server_info=client.recvfrom(4096)
file_server_info=str(file_server_info[0].decode())
print(file_server_info)
if (client_numb==1):
    client_name='cs1'
elif(client_numb==2):
    client_name='cs2'
elif(client_numb==3):
    client_name='cs3'

#once info sent client wants to access file server


def gen_nonce():
    return(random.randint(1,10000))
#make this part interactive
nonce=gen_nonce()
print("What file server do you want to access? (options are fs1 and fs2) : ")
file_name=input()
while (file_name not in ['fs1','fs2']):
    print("No such file server , Enter file server name again : ")
    file_name = input()
access=[client_name,file_name,str(nonce)]#client 1 wants to access file server 1 change this up and make interactive
send_det=pickle.dumps(access)
client.sendto(send_det,kds)
enc_response=client.recvfrom(4096)
enc_response=pickle.loads(enc_response[0])
key_kds=keys['kds']

response=[]
for i in range(6):
    response.append(key_kds.decrypt(enc_response[i]))
    if (i<3):
        response[i]=response[i].decode()
if nonce==int(response[0]):
    session_key=Fernet(response[1])
    keys[file_name]=session_key
    file_location=(ip,int(response[2]))
    message_to_file=pickle.dumps([response[3],response[4],response[5]])

    client.sendto(message_to_file,file_location)
    file_reply=client.recvfrom(4096)

    file_reply=file_reply[0]
    dec_nonce=session_key.decrypt(file_reply)
    dec_nonce=dec_nonce.decode()
    dec_nonce=int(dec_nonce)-1
    enc_nonce=session_key.encrypt(str(dec_nonce).encode())
    client.sendto(enc_nonce,file_location)
    verified=client.recvfrom(4096)
    verified=verified[0].decode()
    want_continue='y'
    actions=["pwd","ls","cp","cat","add"]
    if (verified=='1'):
        print(file_name+" has verified you")
        print("You can perform these actions :")
        print("\tpwd - List present working directory of a file")
        print("\tls - list the contents of a file server")
        print("\tcp - copy one file from one server to the other ")
        print("\tcat - display contents of a file (read file)")
        print("\tadd - add a file to this server ")
        print("\n")
        while(want_continue=='y'):
            print("What action do you want to do? ")
            action=input()
            yes='y'
            yes=session_key.encrypt(yes.encode())
            action_message=[yes]
            if (action not in actions):
                print("This action is not supported :")
                print("Do you want to continue?(y/n):")
                want_continue=input()
            else:
                if (action=='pwd'):
                    action_message.append(session_key.encrypt(action.encode()))
                    action_message=pickle.dumps(action_message)
                    client.sendto(action_message,file_location)
                    output=client.recvfrom(4096)
                    output=session_key.decrypt(output[0])
                    output=output.decode()
                    print(output)
                    print("Do you want to continue?(y/n):")
                    want_continue = input()
                elif (action=='ls'):
                    action_message.append(session_key.encrypt(action.encode()))
                    action_message = pickle.dumps(action_message)
                    client.sendto(action_message, file_location)
                    output = client.recvfrom(4096)
                    output = session_key.decrypt(output[0])
                    output = output.decode()
                    print(output)
                    print("Do you want to continue?(y/n):")
                    want_continue = input()
                elif(action=="cat"):
                    action_message.append(session_key.encrypt(action.encode()))
                    print("Name the file you want to read ")
                    file_to_read=str(input())
                    action_message.append(session_key.encrypt(file_to_read.encode()))
                    action_message = pickle.dumps(action_message)
                    client.sendto(action_message, file_location)
                    output = client.recvfrom(4096)
                    output = session_key.decrypt(output[0])
                    output = output.decode()
                    print(output)
                    print("Do you want to continue?(y/n):")
                    want_continue = input()
                elif(action=="cp"):
                    action_message.append(session_key.encrypt(action.encode()))
                    print("Name the file you want to copy from other server  ")
                    file_to_copy = str(input())
                    action_message.append(session_key.encrypt(file_to_copy.encode()))
                    action_message = pickle.dumps(action_message)
                    client.sendto(action_message, file_location)
                    output = client.recvfrom(4096)
                    output = session_key.decrypt(output[0])
                    output = output.decode()
                    print(output)
                    print("Do you want to continue?(y/n):")
                    want_continue = input()
                elif(action=="add"):
                    action_message.append(session_key.encrypt(action.encode()))
                    print("Name the file you want to add to server  ")
                    file_to_add = str(input())
                    print("Please write Content of this file")
                    content_of_file=str(input())
                    action_message.append(session_key.encrypt(file_to_add.encode()))
                    action_message.append(session_key.encrypt(content_of_file.encode()))
                    action_message = pickle.dumps(action_message)
                    client.sendto(action_message, file_location)
                    output = client.recvfrom(4096)
                    output = session_key.decrypt(output[0])
                    output = output.decode()
                    print(output)
                    print("Do you want to continue?(y/n):")
                    want_continue = input()

        no='n'
        no = session_key.encrypt(no.encode())
        action_message = [no]
        action_message = pickle.dumps(action_message)
        client.sendto(action_message, file_location)

    else:
        print("Not verified, you are not allowed to perform actions on file server ")
else:
    print("Key Distribution Server not verified as nonce not equal ")




