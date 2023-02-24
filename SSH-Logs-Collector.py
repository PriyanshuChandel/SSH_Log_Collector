from os.path import join, exists, dirname
from os import makedirs
from tkinter import Tk, Label, Entry, Button, Checkbutton, IntVar, StringVar, Frame
from tkinter.scrolledtext import ScrolledText
from threading import Thread
from pysftp import Connection, CnOpts, ConnectionException, AuthenticationException
from warnings import filterwarnings
from bs4 import BeautifulSoup
from datetime import datetime
from paramiko import SSHException


icon_file = join(dirname(__file__), 'icon.ico')
window = Tk()
window.config(bg='grey')
window.title('FLC - Developed by Priyanshu')
window.minsize(width=426, height=475)
window.maxsize(width=426, height=475)
window.iconbitmap(icon_file)
window.resizable(False, False)

if not exists('log'):
    makedirs('log')
file_handler = open(f"log/logs_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt", 'a')


My_Key = 'conf/ospf_ssh_private_key'
Data_Path = 'conf/data_path.conf'
Eqpt_XML = 'conf/EQPT.xml'
User_Detail = 'conf/usr.conf'
Port_Detail = 'conf/port.conf'

def establishing_sftp_connection(ip):
    global SFTP_Connection
    filterwarnings('ignore')
    Host_Name = ip
    User_Name = open(User_Detail, "r").readline()
    Port = int(open(Port_Detail, "r").readline())
    Cnopts = CnOpts()
    Cnopts.hostkeys = None
    SFTP_Connection = Connection(host=Host_Name, username=User_Name, port=Port, private_key=My_Key, cnopts=Cnopts)
    CnOpts.hostkeys = None
    file_handler.write(f'{datetime.now().replace(microsecond=0)} Connection successful to host {Host_Name}.\n')


basic_log_path = open(Data_Path, "r").readlines()[0].split(' = ')[1]
sys_log_path = open(Data_Path, "r").readlines()[1].split(' = ')[1]


def threading_btn5():
    thread_btn5 = Thread(target=btn5_func)
    thread_btn5.start()


def btn5_func():
    labl10.config(text='Logs collection started...')
    for ip in ip_list:
        try:
            establishing_sftp_connection(ip)
            host_name = {v: k for k, v in eqpt_dict.items()}.get(ip)
            SFTP_Connection.execute(f"rm -f /tmp/Basic_Logs_{host_name}.zip")
            SFTP_Connection.execute(f"zip -q -r -o /tmp/Basic_Logs_{host_name}.zip {basic_log_path}")
            SFTP_Connection.get(f"/tmp/Basic_Logs_{host_name}.zip")
            file_handler.write(
                f'{datetime.now().replace(microsecond=0)} Basic logs collected successfully for {host_name}.\n')
        except ConnectionException:
            file_handler.write(f'{datetime.now().replace(microsecond=0)} Host {ip} unreachable.\n')
        except AuthenticationException:
            file_handler.write(
                f"""{datetime.now().replace(microsecond=0)} Username <{open(User_Detail, "r").readline()}
            > or public-private pair is not correct.\n""")
        except SSHException:
            file_handler.write(f'{datetime.now().replace(microsecond=0)} SSH connection failed to {ip}.\n')
    labl10.config(text='Logs collection finished, check the log file for status')


def threading_btn6():
    thread_btn6 = Thread(target=btn6_func)
    thread_btn6.start()


def btn6_func():
    labl10.config(text='Logs collection started...')
    for ip in ip_list:
        try:
            establishing_sftp_connection(ip)
            host_name = {v: k for k, v in eqpt_dict.items()}.get(ip)
            SFTP_Connection.execute(f"rm -f /tmp/Sys_Logs_{host_name}.zip")
            SFTP_Connection.execute(f"zip -q -r -o /tmp/Sys_Logs_{host_name}.zip {sys_log_path}")
            SFTP_Connection.get(f"/tmp/Sys_Logs_{host_name}.zip")
            file_handler.write(
                f'{datetime.now().replace(microsecond=0)} Sys logs collected successfully for {host_name}.\n')
        except ConnectionException:
            file_handler.write(f'{datetime.now().replace(microsecond=0)} Host {ip} unreachable.\n')
        except AuthenticationException:
            file_handler.write(
                f"""{datetime.now().replace(microsecond=0)} Username <{open(User_Detail, "r").readline()}
            > or public-private pair is not correct.\n""")
        except SSHException:
            file_handler.write(f'{datetime.now().replace(microsecond=0)} SSH connection failed to {ip}.\n')
    labl10.config(text='Logs collection finished, check the log file for status')


def threading_btn7():
    thread_btn4 = Thread(target=btn7_func)
    thread_btn4.start()


def btn7_func():
    labl10.config(text='Logs collection started...')
    for ip in ip_list:
        try:
            establishing_sftp_connection(ip)
            host_name = {v: k for k, v in eqpt_dict.items()}.get(ip)
            copy_from = str(ent7.get())
            SFTP_Connection.execute(f"rm -f /tmp/Additional_Logs_{host_name}.zip")
            SFTP_Connection.execute(f"zip -q -r -o /tmp/Additional_Logs_{host_name}.zip {copy_from}")
            SFTP_Connection.get(f"/tmp/Additional_Logs_{host_name}.zip")
            file_handler.write(
                f'{datetime.now().replace(microsecond=0)} Additional logs collected successfully for {host_name}.\n')
        except ConnectionException:
            file_handler.write(f'{datetime.now().replace(microsecond=0)} Host {ip} unreachable.\n')
        except AuthenticationException:
            file_handler.write(
                f"""{datetime.now().replace(microsecond=0)} Username <{open(User_Detail, "r").readline()}
            > or public-private pair is not correct.\n""")
        except SSHException:
            file_handler.write(f'{datetime.now().replace(microsecond=0)} SSH connection failed to {ip}.\n')
    labl10.config(text='Logs collection finished, check the log file for status')


labl1 = Label(window, text='Linux Log Collection', font=(None, 12, 'bold'), bg='grey').place(x=145, y=1)
lab2 = Label(window, text='Enter IP address of host (press spacebar to enter)', wraplength=170, justify='left',
             font=(None, 8, 'bold'), bg='grey').place(x=6, y=26)
stringvar_2 = StringVar()


def add_additional_ip(self):
    if not len(stringvar_2.get()) == 0:
        eqpt_dict['Additional_Host'] = stringvar_2.get()
        var_dict['Additional_Host'] = IntVar(value=1)
        ip_list.append(eqpt_dict.get('Additional_Host'))
    if len(stringvar_2.get()) == 0:
        ip_list.remove(eqpt_dict.get('Additional_Host'))
        eqpt_dict.pop('Additional_Host')
        var_dict.pop('Additional_Host')


ent2 = Entry(window, bd=4, width=32, bg='lavender', textvariable=stringvar_2)
ent2.place(x=153, y=30)
ent2.bind("<space>", add_additional_ip)
lab3 = Label(window, text='OR', font=(None, 9, 'bold'), bg='grey').place(x=380, y=31)

labl4 = Label(window, text='Select host from below', font=(None, 9, 'bold'), bg='grey').place(x=150, y=60)
text4 = ScrolledText(window, width=14, height=12, bg='white', bd=4)
text4.place(x=145, y=80)
eqpt_dict = dict()
for eqpt, ip in zip(BeautifulSoup(open(Eqpt_XML).read(),'xml')('equipment'), BeautifulSoup(open(Eqpt_XML).read(),'xml').findAll('ip')):
    eqpt_dict[eqpt.get('Name')] = ip.text
ip_list = list()


def checkbox_command():
    global ip_list
    ip_list = [eqpt_dict[key] for key in eqpt_dict.keys() if var_dict[key].get() == 1]


var_dict = dict()
for eqpts in eqpt_dict.keys():
    var_dict[eqpts] = IntVar(value=0)
    checkbutton4 = Checkbutton(text4, text=eqpts, variable=var_dict[eqpts], onvalue=1, offvalue=0, bg='white',
                               cursor="hand2", command=checkbox_command)
    checkbutton4.pack()
    text4.window_create('end', window=checkbutton4)

labl5 = Label(window, text='Click here if you want to collect basic logs from </data/logs/>',
              font=(None, 9, 'bold'), bg='grey').place(x=6, y=290)
btn5 = Button(window, text='Pack', command=threading_btn5, bg='green')
btn5.place(x=380, y=288)

labl6 = Label(window, text='Click here if you want to collect syslog from </var/log/>', font=(None, 9, 'bold'),
              bg='grey').place(x=6, y=320)
btn6 = Button(window, text='Pack', command=threading_btn6, bg='green')
btn6.place(x=380, y=318)

labl7 = Label(window, text='Specify directory to collect anything else', font=(None, 9, 'bold'), bg='grey',
              wraplength=178, justify='left').place(x=6, y=350)
ent7 = Entry(window, bd=4, width=32, bg='lavender')
ent7.place(x=167, y=354)
btn7 = Button(window, text='Pack', command=threading_btn7, bg='green')
btn7.place(x=380, y=354)

labl8 = Label(window, text='Note: This option depends on the permissions', font=(None, 9, 'bold'), bg='grey')
labl8.place(x=6, y=384)

frame9 = Frame(window, bg="white", bd=20, width=410,
               height=60, cursor="target").place(x=6, y=406)
labl9 = Label(frame9, text='Status:', font=(None, 9, 'bold'), bg='white')
labl9.place(x=6, y=406)

labl10 = Label(window, font=(None, 9, 'bold'), bg='white', wraplength=300, justify='left')
labl10.place(x=6, y=426)
window.mainloop()