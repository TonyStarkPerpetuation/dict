from socket import *

HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST,PORT)

class Client():
    def __init__(self):
        self.sockfd = socket()
        self.sockfd.connect(ADDR)

    def view_1(self):
        print('----------------')
        print('---- 1.登录 ----')
        print('---- 2.注册 ----')
        print('---- 3.退出 ----')
        print('----------------')

    def view_2(self):
        print('----------------')
        print('---- 1.查询 ----')
        print('---- 2.记录 ----')
        print('---- 3.注销 ----')
        print('----------------')

    def main(self):
        while True:
            self.view_1()
            you = input('请输入选项:')
            if you == '1':
                str = self.login()
                if str == '登陆成功!':
                    print(str)
                    self.main_1()
            elif you == '2':
                self.enrol()
            elif you == '3':
                self.exit()
                return print('客户端已退出!')

    def main_1(self):
        while True:
            self.view_2()
            you = input('请输入选项:')
            if you == '1':
                self.check()
            elif you == '2':
                self.history()
            elif you == '3':
                self.main()

    def login(self):

        # self.sockfd.send(b'L')
        # tmp = self.sockfd.recv(32).decode()
        # if tmp == 'OK':
        while True:
            print('---登录界面---')
            name = input('用户名:')
            password = input('密码:')
            data = 'L '+name+' '+password
            self.sockfd.send(data.encode())
            result = self.sockfd.recv(128).decode()
            if result == 'True':
                return '登陆成功!'
            elif result == 'False':
                return print('密码错误!')
            else :
                return print('用户名不存在!')

    def enrol(self):
        while True:
            name = input('用户名:')
            if len(name.split(' ')) <= 1:
                name_send = 'E '+name
                self.sockfd.send(name_send.encode())

                name_recv = self.sockfd.recv(32).decode()

                if name_recv == 'Yes':
                    password = input('密码:')
                    if len(password.split(' '))<=1:
                        password_send = 'E '+password
                        self.sockfd.send(password_send.encode())
                        password_recv = self.sockfd.recv(32)
                        if password_recv:
                            return print('注册成功!')
                    else :
                        print('密码内不允许有空格')
                else:
                    print('用户名已存在请重新输入!')
            else :
                print('账号内不允许有空格')

    def exit(self):
        data = 'Q'
        self.sockfd.send(data.encode())
        self.sockfd.close()

    def check(self):
        while True:
            print('-查询单词界面-')
            word = input('>>')
            if word:
                word_send = 'C '+word
                self.sockfd.send(word_send.encode())
                mean = self.sockfd.recv(1024).decode()
                if mean:
                    print(mean)
                else :
                    print('请输入正确单词!')
            else :
                break

    def history(self):
        self.sockfd.send(b'H')
        print('用户   查询单词             查询时间')
        while True:
            data = self.sockfd.recv(1024).decode()
            if '!' in data:
                break
            print(data)


if __name__ == '__main__':
    c = Client()
    c.main()



