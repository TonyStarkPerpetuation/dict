import sys,signal
import time
from socket import *
from multiprocessing import *
import pymysql

HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST,PORT)

class Server():
    def __init__(self):
        self.db = pymysql.connect(user='root',password='123456',database='dict',charset='utf8')
        self.cur = self.db.cursor()
        self.sockfd = socket()
        self.name = None

    def enrol(self,connect,data):
        # 注册
        name = data.split(' ')[-1]
        print(name)
        sql = "select name,password from user where name=%s"
        self.cur.execute(sql, [name])
        tup = self.cur.fetchone()

        if tup:
            connect.send(b'No')
        else :

            connect.send(b'Yes')
            data1 = connect.recv(128).decode()
            password = data1.split(' ')[-1]

            if password :
                connect.send(b'OK')
                sql1 = "insert into user (name,password) values (%s,%s)"
                try :
                    self.cur.execute(sql1,[name,password])
                    self.db.commit()
                except Exception as e:
                    self.db.rollback()
            else :
                connect.send(b'')

    def login(self,data,connect):
        name = data.split(' ')[1]
        password = data.split(' ')[2]

        sql = "select password from user where name=%s"
        self.cur.execute(sql,[name])
        tup = self.cur.fetchone()
        # print(tup)
        if tup :
            if tup[0] == password:
                connect.send(b'True')
                self.name = name
            else :
                connect.send(b'False')
        else :
            connect.send(b'Not found')

    def check(self,connect,data):
        # 查单词
        word = data.split(' ',1)[-1]
        # print(word)
        sql = 'select word,mean from words where word=%s'
        self.cur.execute(sql,[word])
        tup = self.cur.fetchone()
        # print(tup)
        if tup:
            connect.send(tup[1].encode())
            sql1 = "insert into history (name,word,time) values (%s,%s,%s)"
            self.cur.execute(sql1,[self.name,word,time.ctime()])
            self.db.commit()
        else :
            connect.send(b'False')

    def history(self,connect):
        # 查历史记录
        sql = "select name,word,time from history where name = %s order by time desc"
        self.cur.execute(sql,[self.name])
        tup = self.cur.fetchmany(10)
        for item in tup:
            tmp = '%s    %-16s  %s' % item
            connect.send(tmp.encode())
            time.sleep(0.05)
        connect.send(b'!')

    def exit(self,addr):
        # 退出
        print(addr,'客户端已退出!')

    def main(self):
        # 套接字
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(ADDR)
        self.sockfd.listen(3)
        print('This is a dict-server ! \nWaitting connect ...')

        signal.signal(signal.SIGCHLD,signal.SIG_IGN)
        while True:
            try :
                connect,addr = self.sockfd.accept()
                print('Connect from:',addr)
            except KeyboardInterrupt:
                sys.exit('退出服务器!')
            except Exception as e:
                print(e)
                continue

            p = Process(target=self.run,args=(connect,addr))
            p.daemon = True
            p.start()
            # self.run(connect,addr)

    def run(self,connect,addr):
        # 运行
        while True:
            data = connect.recv(128).decode()
            a = data.split(' ')[0]

            if a == 'E':
                self.enrol(connect,data)

            elif a == 'L':
                self.login(data,connect)

            elif a == 'Q':
                self.exit(addr)

            elif a == 'C':
                self.check(connect,data)

            elif a == 'H':
                self.history(connect)

if __name__ == '__main__':
    s = Server()
    s.main()











