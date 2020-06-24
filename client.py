import socket
import threading
import queue
address=('127.0.0.1',31500)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(data,addr):
    sock.sendto(data.encode('ascii'),addr)
def recv():
    while True:
       data,addr=sock.recvfrom(65536)
       if not event.isSet():
           if(data.decode('ascii').split('|',1)[0]=='chat'):
               print(data.decode('ascii').split('|',1)[1])
           elif(data.decode('ascii').split('|',1)[0]=='chatto'):
               print('(p to p chat):{}'.format(data.decode('ascii').split('|',1)[1]))
       queue.put(data)

def reg():
    print('Username',end=':')
    user=input()
    print('Password',end=':')
    passd=input()
    data='reg|'+user+'|'+passd
    send(data,address)
    result=queue.get()
    return result

def login():
    print('Username',end=':')
    user=input()
    print('Passwd',end=':')
    passd=input()
    data='login'+'|'+user+'|'+passd
    send(data,address)
    result=queue.get()
    return result

def chatto(user):
    print('*************chat with {}*****************'.format(user)) 
    while True:

        msg=input()
        if(msg=='quite'):
            return 0
               
        data='chatto|'+user+'|'+msg
        send(data,address)

def chatroom():
    send('forward|I am coming!',address)
    result=queue.get()
    if(result.decode('ascii')=='disable'):
        print('Can not in!')
        return 0
    print('********welcome to chatroom***********')
    while True:
        msg=input()
        if(msg=='quite'):
            return 0   
        data='forward|'+msg
        send(data,address)
        

if __name__=='__main__':
    queue=queue.Queue()
    event=threading.Event()
    event.set()
    recvthread=threading.Thread(target=recv,args=())
    recvthread.start()
   
    while True:
        
        print('Welcome to Chat room!!')
        print('(1):Reginster')
        print('(2):Login')
        print('(3):Enter the chat room')
        print('(4):Chat to someone')
        print('Please select',end=':')
        
        msg=input()
        if(msg=='1'):
            data=reg()
            if(data.decode('ascii')=='reg'):
                print('Register successfully!')
            else:
                print('Register failed!')

        elif(msg=='2'):
            data=login()
            if(data.decode('ascii')=='1'):
                print('Login successfully!')
            elif(data.decode('ascii')=='0'):
                print('Login failed!')
           
        elif(msg=='3'):
            event.clear()
            chatroom()
            event.set()
        elif(msg=='4'):
            event.clear()
            print('who do you want to chat to ?',end=':')
            name=input()
            if name is not 0:
                chatto(name)
            event.set()
    sock.close()

