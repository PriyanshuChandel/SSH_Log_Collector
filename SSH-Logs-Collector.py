class linuxApp:
    if not exists('log'):
        makedirs('log')
    fileHandler = open(f"log/logs_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt", 'a')
    authenticationPublicPrivateKey = 'conf/ospf_ssh_private_key'
    logCollectionPath = 'conf/data_path.conf'
    equipmentsXml = 'conf/EQPT.xml'
    userDetail = 'conf/usr.conf'
    portDetail = 'conf/port.conf'
    userName = open(userDetail, "r").readline()
    port = int(open(portDetail, "r").readline())
    iconFile = join(dirname(__file__), 'icon.ico')
    aboutIcon = join(dirname(__file__), 'info.ico')

    def __init__(self):
        self.basicLogPath = ''
        self.sysLogPath = ''
        try:
            self.basicLogPath = open(self.logCollectionPath, "r").readlines()[0].split('=')[1]
            self.sysLogPath = open(self.logCollectionPath, "r").readlines()[1].split('=')[1]
        except FileNotFoundError:
            self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [ERROR] File [{self.logCollectionPath}] '
                                   f'not found\n')
        except Exception as e:
            self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [ERROR] Something went wrong while opening'
                                   f' [{self.logCollectionPath}][{e}]\n')
        self.sftpConnection = None
        self.equipDict = {}
        self.ipList = []
        self.varDict = {}
        self.checkBoxes = {}
        self.window = Tk()
        self.window.config(bg='#F0F0F0')
        self.window.title('LinApp - v1.0')
        self.window.geometry('300x550')
        self.window.iconbitmap(self.iconFile)
        self.window.resizable(False, False)
        self.mainLabel = Label(self.window, text='Linux Log Collection', font=('Arial', 15, 'bold'), fg='blue',
                               bg='#F0F0F0')
        self.mainLabel.place(x=65, y=5)
        self.selectHostLabel = Label(self.window, text='Select host', font=(None, 9, 'bold'), bg='#F0F0F0')
        self.selectHostLabel.place(x=90, y=40)
        self.checkBoxesScrolledText = ScrolledText(self.window, width=14, height=12, bg='white', bd=4)
        self.checkBoxesScrolledText.place(x=90, y=60)

        self.basicLogLabelFrame = LabelFrame(self.window, text='Basic Logs', bd=3, labelanchor='n', relief='ridge',
                                             width=80, height=50)
        self.basicLogBtn = Button(self.basicLogLabelFrame, text='Pack', command=self.threadingBasicLog,
                                  state='disabled', bg='light grey', fg='white', font=('Arial', 8, 'bold'))
        self.basicLogBtn.place(x=17, y=1)
        self.basicLogLabelFrame.place(x=65, y=268)
        self.sysLogLabelFrame = LabelFrame(self.window, text='Sys Logs', bd=3, labelanchor='n', relief='ridge',
                                           width=80, height=50)
        self.sysLogBtn = Button(self.sysLogLabelFrame, text='Pack', command=self.threadingSysLog,
                                state='disabled', bg='light grey', fg='white', font=('Arial', 8, 'bold'))
        self.sysLogBtn.place(x=17, y=1)
        self.sysLogLabelFrame.place(x=165, y=268)
        self.customLogLabelFrame = LabelFrame(self.window, text='Custom Logs', bd=3, labelanchor='n', relief='ridge',
                                              width=290, height=80)
        self.customLogEntry = Entry(self.customLogLabelFrame, bd=4, width=35, bg='white', state='readonly')
        self.customLogEntry.place(x=5, y=5)
        self.customLogBtn = Button(self.customLogLabelFrame, text='Pack', command=self.threadingCustomLog,
                                   state='disabled', bg='light grey', fg='white', font=('Arial', 8, 'bold'))
        self.customLogBtn.place(x=240, y=5)
        self.customLogWarnLabel = Label(self.customLogLabelFrame, text='Note: This option depends on the permissions',
                                        font=('Ariel', 9, 'bold italic'), bg='#F0F0F0')
        self.customLogWarnLabel.place(x=3, y=40)
        self.customLogLabelFrame.place(x=5, y=320)

        self.progressLabelFrame = LabelFrame(self.window, text='Progress', bd=3, labelanchor='n', relief='ridge',
                                             width=290, height=100)
        self.progressOverallLabel = Label(self.progressLabelFrame, text='Overall', font=(None, 9, 'bold'), bg='#F0F0F0')
        self.progressOverallLabel.place(x=1, y=5)
        self.progressOverall = Progressbar(self.progressLabelFrame, length=230, mode="determinate",
                                           style="Custom.Overall.Horizontal.TProgressbar")
        self.progressOverall.place(x=50, y=5)
        self.progressStyleOverall = Style()
        self.progressStyleOverall.theme_use('clam')
        self.progressStyleOverall.configure("Custom.Overall.Horizontal.TProgressbar", background="green", text='0/0')
        self.progressStyleOverall.layout('Custom.Overall.Horizontal.TProgressbar', [('Horizontal.Progressbar.trough',
                                                                                     {'children': [
                                                                                         ('Horizontal.Progressbar.pbar',
                                                                                          {'side': 'left',
                                                                                           'sticky': 'ns'})],
                                                                                         'sticky': 'nswe'}),
                                                                                    ('Horizontal.Progressbar.label',
                                                                                     {'sticky': ''})])

        self.progressPassLabel = Label(self.progressLabelFrame, text='Pass', font=(None, 9, 'bold'), bg='#F0F0F0')
        self.progressPassLabel.place(x=1, y=30)
        self.progressPass = Progressbar(self.progressLabelFrame, length=230, mode="determinate",
                                        style="Custom.Pass.Horizontal.TProgressbar")
        self.progressPass.place(x=50, y=30)
        self.progressStylePass = Style()
        self.progressStylePass.theme_use('clam')
        self.progressStylePass.configure("Custom.Pass.Horizontal.TProgressbar", background="light green", text='0/0')
        self.progressStylePass.layout('Custom.Pass.Horizontal.TProgressbar', [('Horizontal.Progressbar.trough',
                                                                               {'children': [
                                                                                   ('Horizontal.Progressbar.pbar',
                                                                                    {'side': 'left',
                                                                                     'sticky': 'ns'})],
                                                                                'sticky': 'nswe'}),
                                                                              ('Horizontal.Progressbar.label',
                                                                               {'sticky': ''})])

        self.progressFailLabel = Label(self.progressLabelFrame, text='Fail', font=(None, 9, 'bold'), bg='#F0F0F0')
        self.progressFailLabel.place(x=1, y=55)
        self.progressFail = Progressbar(self.progressLabelFrame, length=230, mode="determinate",
                                        style="Custom.Fail.Horizontal.TProgressbar")
        self.progressFail.place(x=50, y=55)
        self.progressStyleFail = Style()
        self.progressStyleFail.theme_use('clam')
        self.progressStyleFail.configure("Custom.Fail.Horizontal.TProgressbar", background="red", text='0/0')
        self.progressStyleFail.layout('Custom.Fail.Horizontal.TProgressbar', [('Horizontal.Progressbar.trough',
                                                                               {'children': [
                                                                                   ('Horizontal.Progressbar.pbar',
                                                                                    {'side': 'left',
                                                                                     'sticky': 'ns'})],
                                                                                'sticky': 'nswe'}),
                                                                              ('Horizontal.Progressbar.label',
                                                                               {'sticky': ''})])

        self.progressLabelFrame.place(x=5, y=400)
        self.messageLabel = Label(self.window, font=('Arial', 9, 'bold'), bg='#F0F0F0')
        self.messageLabel.place(x=6, y=505)
        self.aboutBtn = Button(self.window, text='About', bg='brown', command=self.aboutWindow)
        self.aboutBtn.place(x=250, y=520)

    def threadingBasicLog(self):
        def inner():
            self.basicLogBtn.config(state='disabled', bg='light grey', bd=3, relief='groove')
            self.basicLogLabelFrame.config(fg='green')
            self.sysLogBtn.config(state='disabled', bg='light grey')
            self.customLogEntry.delete(0, 'end')
            self.customLogEntry.config(state='readonly')
            self.customLogBtn.config(state='disabled')
            self.collectFunction('Basic', self.basicLogPath)
            self.basicLogBtn.config(bd=2, relief='raised')
            self.basicLogLabelFrame.config(fg='black')

        threadBasicLog = Thread(target=inner)
        threadBasicLog.start()

    def threadingSysLog(self):
        def inner():
            self.sysLogBtn.config(state='disabled', bg='light grey', bd=3, relief='groove')
            self.sysLogLabelFrame.config(fg='green')
            self.basicLogBtn.config(state='disabled', bg='light grey')
            self.customLogEntry.delete(0, 'end')
            self.customLogEntry.config(state='readonly')
            self.customLogBtn.config(state='disabled')
            self.collectFunction('Sys', self.sysLogPath)
            self.sysLogBtn.config(bd=2, relief='raised')
            self.sysLogLabelFrame.config(fg='black')

        threadSysLog = Thread(target=inner)
        threadSysLog.start()

    def threadingCustomLog(self):
        def inner():
            self.customLogBtn.config(state='disabled', bg='light grey', bd=3, relief='groove')
            self.customLogLabelFrame.config(fg='green')
            self.customLogEntry.config(state='readonly')
            self.sysLogBtn.config(state='disabled')
            self.basicLogBtn.config(state='disabled')
            copyFrom = str(self.customLogEntry.get())
            self.collectFunction('Custom', copyFrom)
            self.customLogBtn.config(bd=2, relief='raised')
            self.customLogLabelFrame.config(fg='black')

        threadCustomLog = Thread(target=inner)
        threadCustomLog.start()

    def collectFunction(self, logsType, path):
        self.progressStyleOverall.configure("Custom.Overall.Horizontal.TProgressbar", text=f'0/{len(self.ipList)}')
        self.progressStylePass.configure("Custom.Pass.Horizontal.TProgressbar", text=f'0/{len(self.ipList)}')
        self.progressStyleFail.configure("Custom.Fail.Horizontal.TProgressbar", text=f'0/{len(self.ipList)}')
        self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [Info] User selected {self.ipList}\n')
        self.disableCheckboxes()
        startTime = time()
        self.messageLabel.config(text='')
        self.messageLabel.config(text='Collecting...')
        self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [Info] Collecting {logsType} logs...\n')
        progressDict = {f'{logsType}LogsCollectDone': [],
                        f'{logsType}LogsCollectFailed': []}
        logsCollectedDone = [progressDict[x] for x in progressDict.keys()][0]
        logsCollectedFail = [progressDict[x] for x in progressDict.keys()][1]
        overallChecked = 0
        for ip in self.ipList:
            hostName = {v: k for k, v in self.equipDict.items()}.get(ip)
            if self.establishSftpConnection(ip, hostName):
                print('1', logsCollectedDone)
                print('2', logsCollectedFail)
                try:
                    fileName = f"{logsType}Logs_{hostName}_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
                    self.sftpConnection.execute(f"rm -f /tmp/{logsType}Logs_*")
                    self.sftpConnection.execute(f"zip -q -r -o /tmp/{fileName} {path}")
                    self.sftpConnection.get(f"/tmp/{fileName}")
                    self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} {logsType}[{path.strip()}] '
                                           f'logs collected successfully for [{hostName}_{ip}].\n')
                    logsCollectedDone.append(f'{hostName}_{ip}')
                    self.updateProgress(self.progressPass, self.progressStylePass, len(logsCollectedDone),
                                        len(self.ipList), 'Pass')
                except FileNotFoundError:
                    self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [ERROR] Failed to copy from '
                                           f'[{hostName}_{ip}], [{path}] is not valid path\n')
                    logsCollectedFail.append(f'{hostName}_{ip}')
                    self.updateProgress(self.progressFail, self.progressStyleFail, len(logsCollectedFail),
                                        len(self.ipList), 'Fail')
                except Exception as e:
                    self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [ERROR] Something went wrong '
                                           f'while executing remote command for [{hostName}_{ip}]. [{e}]\n')
                    logsCollectedFail.append(f'{hostName}_{ip}')
                    self.updateProgress(self.progressFail, self.progressStyleFail, len(logsCollectedFail),
                                        len(self.ipList), 'Fail')
            else:
                logsCollectedFail.append(f'{hostName}_{ip}')
                self.updateProgress(self.progressFail, self.progressStyleFail, len(logsCollectedFail),
                                    len(self.ipList), 'Fail')
            overallChecked += 1
            self.updateProgress(self.progressOverall, self.progressStyleOverall, overallChecked, len(self.ipList),
                                'Overall')
        endTime = time()
        self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [Info] {logsType} logs collected successfully '
                               f'for [{len(logsCollectedDone)}] hosts, {logsCollectedDone}\n')
        self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [Info] {logsType} logs collected failed for '
                               f'[{len(logsCollectedFail)}] host, {logsCollectedFail}\n')
        self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [Info] ELAPSED TIME TO COLLECT '
                               f'{logsType} LOGS is {((endTime - startTime) / 60):.2f} Minutes\n')
        self.messageLabel.config(text='Finished, check logs!')
        self.fileHandler.flush()
        self.enableCheckboxes()

    def establishSftpConnection(self, ip, hostName):
        filterwarnings('ignore')
        try:
            self.fileHandler.write(f"{datetime.now().replace(microsecond=0)} [Info] Trying to connect host "
                                   f"[{hostName}_{ip}] \n")
            cn0pts = CnOpts()
            cn0pts.hostkeys = None
            self.sftpConnection = Connection(host=ip, username=self.userName, port=self.port,
                                             private_key=self.authenticationPublicPrivateKey, cnopts=cn0pts)
            cn0pts.hostkeys = None
            self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [Info] Connection successful to host '
                                   f'[{hostName}_{ip}].\n')
            self.fileHandler.flush()
            return True
        except ConnectionException:
            self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [ERROR] Host[{hostName}_{ip}] '
                                   f'unreachable.\n')
            self.fileHandler.flush()
            return False
        except AuthenticationException:
            self.fileHandler.write(f"{datetime.now().replace(microsecond=0)} [ERROR] Username "
                                   f"[{open(self.userDetail, 'r').readline()}] or public-private key pair is not "
                                   f"correct for Host[{hostName}_{ip}].\n")
            self.fileHandler.flush()
            return False
        except SSHException:
            self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [ERROR] SSH connection failed to '
                                   f'Host[{hostName}_{ip}]. A connection attempt failed because the connected party '
                                   f'did not properly respond after a period of time, or established connection failed '
                                   f'because connected host has failed to respond\n')
            self.fileHandler.flush()
            return False
        except FileNotFoundError:
            self.fileHandler.write(f"{datetime.now().replace(microsecond=0)} [ERROR] userName [{self.userDetail}] or "
                                   f"portDetail [{self.portDetail}] or PPK [{self.authenticationPublicPrivateKey}] file"
                                   f" is missing for Host[{hostName}_{ip}].\n")
            self.fileHandler.flush()
            return False

    def updateProgress(self, progressBar, progressStyle, newVal, totalVal, state):
        resultVal = f'{newVal}/{totalVal}'
        progressBar['value'] = round((newVal / totalVal) * 100, 2)
        progressStyle.configure(f"Custom.{state}.Horizontal.TProgressbar", text=resultVal)
        self.window.update()

    def checkEntryInput(self, event):
        if len(self.customLogEntry.get().strip()) > 0:
            self.disableCheckboxes()
            self.basicLogBtn.config(state='disabled', bg='light grey')
            self.sysLogBtn.config(state='disabled', bg='light grey')
            self.customLogBtn.config(state='normal', bg='green')
        else:
            self.enableCheckboxes()
            self.customLogBtn.config(state='disabled', bg='light grey')
            self.basicLogBtn.config(state='normal', bg='green')
            self.sysLogBtn.config(state='normal', bg='green')

    def disableCheckboxes(self):
        for checkbox in self.checkBoxes.keys():
            checkbox.config(state='disabled', cursor="arrow")

    def enableCheckboxes(self):
        for checkbox in self.checkBoxes.keys():
            checkbox.config(state='normal', cursor="hand2", bg='white')
            checkbox.deselect()

    def populateEquipDict(self):
        self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [Info] Generating Host-IP pair from '
                               f'[{self.equipmentsXml}]\n')
        try:
            for equip, ip in zip(BeautifulSoup(open(self.equipmentsXml).read(), 'xml')('equipment'),
                                 BeautifulSoup(open(self.equipmentsXml).read(), 'xml').findAll('ip')):
                self.equipDict[equip.get('Name')] = ip.text
                self.varDict[equip.get('Name')] = IntVar(value=0)
            self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [Info] Host-IP pair generated for '
                                   f'[{len(self.equipDict)}] hosts.\n{self.equipDict}\n')
        except FileNotFoundError:
            self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [ERROR] file [{self.equipmentsXml}] does '
                                   f'not exists. Checkbutton can not created\n')
        except IOError:
            self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [ERROR] file [{self.equipmentsXml}] unable'
                                   f' to read. Checkbutton can not created\n')
        except ParseError:
            self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [ERROR] file [{self.equipmentsXml}] is not'
                                   f' formatted as valid xml. Checkbutton can not created\n')
        except Exception as e:
            self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} [ERROR] {e} \n')
        self.fileHandler.flush()

    def checkboxCommand(self):
        self.messageLabel.config(text='')
        self.progressStyleOverall.configure("Custom.Overall.Horizontal.TProgressbar", text='0/0')
        self.progressStylePass.configure("Custom.Pass.Horizontal.TProgressbar", text='0/0')
        self.progressStyleFail.configure("Custom.Fail.Horizontal.TProgressbar", text='0/0')
        self.progressOverall['value'] = 0
        self.progressPass['value'] = 0
        self.progressFail['value'] = 0
        self.ipList = [self.equipDict[key] for key in self.equipDict.keys() if self.varDict[key].get() == 1]
        for checkbox, checkboxText in self.checkBoxes.items():
            checkbox.config(bg='light green' if self.varDict[checkboxText].get() == 1 else 'white')
        if len(self.ipList) >= 1:
            self.customLogEntry.config(state="normal")
            self.customLogEntry.delete(0, 'end')
            self.basicLogBtn.config(state="normal", bg='green')
            self.sysLogBtn.config(state="normal", bg='green')
        else:
            self.customLogEntry.delete(0, 'end')
            self.customLogEntry.config(state="readonly")
            self.customLogBtn.config(state="disabled", bg='light grey')
            self.basicLogBtn.config(state="disabled", bg='light grey')
            self.sysLogBtn.config(state="disabled", bg='light grey')

    def aboutWindow(self):
        aboutWin = Toplevel(self.window)
        aboutWin.grab_set()
        aboutWin.geometry('285x90')
        aboutWin.resizable(False, False)
        aboutWin.title('About')
        aboutWin.iconbitmap(self.aboutIcon)
        aboutWinLabel = Label(aboutWin,
                              text=f'Version - 1.1\nDeveloped by Priyanshu\nFor any improvement please reach on '
                                   f'below email\nEmail : chandelpriyanshu8@outlook.com\nMobile : '
                                   f'+91-8285775109 '
                                   f'', font=('Helvetica', 9)).place(x=1, y=6)

    def runGUI(self):
        self.customLogEntry.bind("<KeyRelease>", self.checkEntryInput)
        self.populateEquipDict()
        for equips in self.equipDict.keys():
            var = IntVar()
            checkButtons = Checkbutton(self.checkBoxesScrolledText, text=equips, variable=var, bg='white',
                                       cursor="hand2", command=self.checkboxCommand)
            self.varDict[equips] = var
            self.checkBoxes[checkButtons] = equips
            checkButtons.pack()
            self.checkBoxesScrolledText.window_create('end', window=checkButtons)
        self.fileHandler.write(f'{datetime.now().replace(microsecond=0)} Checkboxes created.. \n')
        self.fileHandler.flush()
        self.window.mainloop()


if __name__ == '__main__':
    flc_app = linuxApp()
    flc_app.runGUI()
