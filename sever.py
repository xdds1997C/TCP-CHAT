import socket



address = ('127.0.0.1', 31500)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)
print('The adress:{}'.format(sock.getsockname()))
client_address=[]
address_user={}
user_passd={}
islogin=[]

def reg(data,addr):
    user=data.split('|',1)[0]
    passd=data.split('|',1)[1]
    user_passd[user]=passd
    sock.sendto('reg'.encode('ascii'),addr)

def login(data,addr):
    user=data.split('|',1)[0]
    passd=data.split('|',1)[1]
    if(user in user_passd.keys() and user not in islogin):
        if(passd==user_passd[user]):
            client_address.append(addr)
            islogin.append(user)
            
            address_user[addr]=user
            sock.sendto('1'.encode('ascii'),addr)
        else:
            sock.sendto('0'.encode('ascii'),addr)
    else:
        sock.sendto('0'.encode('ascii'),addr)

def chatto(data,addr):
    
    if(data.split('|',1)[0]=='chatto'):
        user=data.split('|',2)[1]
        data='chatto|'+address_user[addr]+':'+data.split('|',2)[2]
        for address in address_user:
            if(address_user[address]==user):
                sock.sendto(data.encode('ascii'),address)
                print('{} send to success'.format(data))

def forward(data,addr):
    if(addr in client_address):
        data='chat|'+address_user[addr]+':'+data
        sock.sendto('allow'.encode('ascii'),addr)
    else:
        sock.sendto('disable'.encode('ascii'),addr)
        return 0
    for client_addr in client_address:
        if addr!=client_addr:
            sock.sendto(data.encode('ascii'),client_addr)
           
 
def recv():
    data,addr=sock.recvfrom(65536)
    print("received:",data,"from",addr)
    text=data.decode('ascii')
    flag_data=text.split('|',1)
    flag=flag_data[0]
    data=flag_data[1]
    return flag,data,addr
if __name__=='__main__':
    while True:
        flag_data=recv()
        flag=flag_data[0]
        data=flag_data[1]
        addr=flag_data[2]
        if(flag=='reg'):
            reg(data,addr)
        elif(flag=='login'):
            login(data,addr)
        elif(flag=='forward'):
            forward(data,addr)
        elif(flag=='chatto'):
            data=flag+'|'+data
            chatto(data,addr) 

sock.close()
