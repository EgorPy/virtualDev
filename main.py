import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog
import os
import time
import math
import win32com.client
import keyboard
import threading
import webbrowser
import pickle


class PassClass:
    keycode = 1

    def __init__(self, keycode):
        self.keycode = keycode


class App:
    def getFolderInformation(self, folderPath):
        # returningData = False
        self.outputText.insert("end", f"opening files in folder \"{folderPath}\"\n\n")
        for f in os.listdir(str(folderPath)):
            try:
                file = open(f"{str(folderPath)}\\{f}", "r", encoding="utf-8")
                unknownFileFormat = True
                # text formats
                for i in self.textFormats:
                    if file.name.rfind(f".{i}") != -1:
                        self.outputText.insert("end", f"---{file.name}---\n", i)
                        unknownFileFormat = False
                        break
                if unknownFileFormat == True:
                    # image formats
                    for i in self.imageFormats:
                        if file.name.rfind(f".{i}") != -1:
                            self.outputText.insert("end", f"---{file.name}---\n", i)
                            unknownFileFormat = False
                            break
                if unknownFileFormat == True:
                    # audio formats
                    for i in self.audioFormats:
                        if file.name.rfind(f".{i}") != -1:
                            self.outputText.insert("end", f"---{file.name}---\n", i)
                            unknownFileFormat = False
                            break
                if unknownFileFormat == True:
                    # video formats
                    for i in self.videoFormats:
                        if file.name.rfind(f".{i}") != -1:
                            self.outputText.insert("end", f"---{file.name}---\n", i)
                            unknownFileFormat = False
                            break
                if unknownFileFormat == True:
                    # archive formats
                    for i in self.archiveFormats:
                        if file.name.rfind(f"{i}") != -1:
                            self.outputText.insert("end", f"---{file.name}---\n", i)
                            unknownFileFormat = False
                            break

                if unknownFileFormat == True:
                    self.outputText.insert("end", f"---{file.name}---\n")
                # data = file.readlines()
                # for i in data:
                #     self.outputText.insert("end", f"{i}")
                # returningData = True
            except UnicodeDecodeError as e:
                self.outputText.insert("end", f"<Cannot decode data, error: {e}>")
            except ValueError as e:
                self.outputText.insert("end", f"<Path is not in str format (Program error), error: {e}>")
            except PermissionError as e:
                self.outputText.insert("end", f"<Permission denied (Maybe caused by opening folder), error: {e}>")
            except FileNotFoundError as e:
                self.outputText.insert("end", f"<Folder not found, error: {e}>")
            self.outputText.insert("end", "\n\n")
            # return returningData

    def getFileInformation(self, filePath):
        returningData = False
        try:
            file = open(filePath, "r", encoding="utf-8")
            self.outputText.insert("end", f"---{file.name}---\n")
            data = file.readlines()
            for i in data:
                self.outputText.insert("end", f"{i}")
            returningData = True
        except UnicodeDecodeError as e:
            self.outputText.insert("end", f"<Cannot decode data, error: {e}>")
        except ValueError as e:
            self.outputText.insert("end", f"<Path is not in str format (Program error), error: {e}>")
        except PermissionError as e:
            self.outputText.insert("end", f"<Permission denied (Maybe caused by opening folder), error: {e}>")
        except FileNotFoundError as e:
            self.outputText.insert("end", f"<File not found, error: {e}>")
        except FileExistsError as e:
            self.outputText.insert("end", f"<File exists, error: {e}>")
        self.outputText.insert("end", "\n\n")
        return returningData

    def checkDownloads(self):
        # getting information in downloads folder
        self.getFolderInformation("C:\\Users\\Egor\\Downloads")
        # self.getFolderInformation("C:\\Users\\Egor\\Downloads\\Telegram Desktop")

    def loadLatestRunData(self):
        # getting information in savedData folder
        # self.getFolderInformation("C:\\Users\\Egor\\Desktop\\virtualDev\\savedData")
        self.getFileInformation("C:\\Users\\Egor\\Desktop\\virtualDev\\savedData\\latestRun.txt")

    def saveData(self):
        # saving latest run info
        file = open("savedData/latestRun.txt", "w")
        file.write(str(time.ctime()))

    def createCalendar(self):
        try:
            fileToRead = open("savedData/calendar.pickle", "rb")
            loaded_object = pickle.load(fileToRead)
            fileToRead.close()
        except FileNotFoundError:
            self.calendarList = []
            # ^ this is a list of str information about what activities you need to do in each day that you wrote
            # you can get any element of this list using this code: self.calendarList[month][day]
            for month in range(self.monthsInYear):
                self.calendarList.append([])
                for day in range(self.daysInMonth):
                    self.calendarList[month].append("")
            print(*self.calendarList, sep="\n")
            fileToStore = open("savedData/calendar.pickle", "wb")
            pickle.dump(self.calendarList, fileToStore)
            fileToStore.close()
        count = 1
        for y in range(self.weeksInMonth):
            for x in range(self.daysInWeek):
                # this expression is needed
                if count < 32:
                    # adding button to list
                    self.calendarButtonsList.append(
                        tkinter.Button(self.calendarCanvas, text=count, relief="flat", bg="#aaaaaa", activebackground=self.bgColor).place(
                            x=x * self.WIDTH / self.daysInWeek,
                            y=y * (self.HEIGHT - 160) / self.weeksInMonth + 100,
                            width=self.WIDTH / self.daysInWeek + 1,
                            height=(self.HEIGHT - 160) / self.weeksInMonth
                        ))
                    if y == 0:
                        self.calendarButtonsList.append(
                            tkinter.Label(self.calendarCanvas, text=self.weekDays[x], relief="flat", bg="#aaaaaa", activebackground=self.bgColor).place(
                                x=x * self.WIDTH / self.daysInWeek,
                                y=10,
                                width=self.WIDTH / self.daysInWeek + 1,
                                height=50
                            )
                        )
                count += 1

    def configuration(self):
        # colors
        self.bgColor = "#000000"
        self.scrollDarkColor = "#0000bb"
        self.firstColor = "black"
        self.textFilesColor = "#0000FF"
        self.imageFilesColor = "#00AAFF"
        self.audioFilesColor = "#00FFFF"
        self.videoFilesColor = "#00FFAA"
        self.archiveFilesColor = "#00FF00"
        self.calendarForeground = "#CCCCFF"

        # fonts
        self.filesFont = ("Courier", 18, "bold")
        self.buttonsFont = ("Courier", 12, "bold")
        self.calendarFont = ("Bebas Neue Bold", 10, "bold")

        # calendar
        self.calendarButtonsList = []
        self.selectedMonth = ""
        self.monthsInYear = 12
        self.weeksInMonth = 5
        self.daysInMonth = 31
        self.daysInWeek = 7
        self.weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        # keyboard heatmap
        self.lastKey = ""
        self.heatDownSpeed = 1
        self.heatUpSpeed = 1
        self.keyboardScale = self.WIDTH / 35
        self.zeroRowKeys = "1234567890-="
        self.firstRowKeys = "qwertyuiop[]\\"
        self.secondRowKeys = "asdfghjkl;'"
        self.thirdRowKeys = "zxcvbnm,./"
        self.zeroRowKeysHeat = [[0, 0, 0] for i in range(len(self.zeroRowKeys))]
        self.firstRowKeysHeat = [[0, 0, 0] for i in range(len(self.firstRowKeys))]
        self.secondRowKeysHeat = [[0, 0, 0] for i in range(len(self.secondRowKeys))]
        self.thirdRowKeysHeat = [[0, 0, 0] for i in range(len(self.thirdRowKeys))]

        # lists
        self.todoFilePath = ""
        self.queryTypes = ["run",
                           "search",
                           "search1",
                           "checkfile",
                           "checkfolder",
                           "calendar",
                           "algorithm",
                           "todo",
                           "translate"]
        self.appNames = ["telegram",
                         "google chrome",
                         "lego mindstorms education ev3",
                         "lego digital designer",
                         "adobe acrobat dc",
                         "android studio",
                         "cmd",
                         "git bash",
                         "git cmd",
                         "git gui",
                         "intellij idea community edition",
                         "microsoft edge",
                         "microsoft visual studio code",
                         "movavi video editor plus",
                         "punto switcher", "putty",
                         "pycharm community edition",
                         "idle (python 3.7 64-bit)",
                         "idle (python 3.9 64-bit)",
                         "roblox player", "roblox studio",
                         "tlauncher",
                         "zoom"]
        self.appPaths = ["D:\\PortableApps\\Telegram\\Telegram.exe",
                         "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                         "C:\\Program Files (x86)\\LEGO Software\\LEGO MINDSTORMS Edu EV3\\MindstormsEV3.exe",
                         "D:\\LEGO Digital Designer\\LDD.exe",
                         "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe",
                         "C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe",
                         "%windir%\\system32\\cmd.exe",
                         "C:\\Users\\Egor\\AppData\\Local\\Programs\\Git\\git-bash.exe",
                         "C:\\Users\\Egor\\AppData\\Local\\Programs\\Git\\git-cmd.exe",
                         "C:\\Users\\Egor\\AppData\\Local\\Programs\\Git\\cmd\\git-gui.exe",
                         "D:\\IntellijIdea\\IntelliJ IDEA Community Edition 2021.3.1\\bin\\idea64.exe",
                         "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
                         "C:\\Users\\Egor\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
                         "D:\\Movavi\\Movavi Video Editor Plus\\VideoEditorPlus.exe",
                         "C:\\Program Files (x86)\\Yandex\\Punto Switcher\\punto.exe",
                         "C:\\Program Files\\PuTTY\\putty.exe",
                         "D:\\Desktop\pycharm\\PyCharm Community Edition 2020.2\\bin\\pycharm64.exe",
                         "C:\\Users\\Egor\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\idlelib\\idle.pyw",
                         "C:\\Users\\Egor\\AppData\\Local\\Programs\\Python\\Python39\\pythonw.exe \"C:\\Users\\Egor\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\idlelib\\idle.pyw\"",
                         "C:\\Users\\Egor\\AppData\\Local\\Roblox\\Versions\\version-04be97a13ff0427b\\RobloxPlayerLauncher.exe",
                         "C:\\Users\\Egor\\AppData\\Local\\Roblox\\Versions\\RobloxStudioLauncherBeta.exe",
                         "C:\\Users\\Egor\\AppData\\Roaming\\.minecraft\\Tlauncher.exe"]
        self.textFormats = ["txt",
                            "md",
                            "py",
                            "spec",
                            "docx",
                            "pdf",
                            "ppt",
                            "pptx",
                            "html",
                            "css",
                            "js",
                            "kt",
                            "kts",
                            "xml",
                            "xlsx",
                            "json",
                            "dll"]
        self.imageFormats = ["png",
                             "jpg",
                             "jpeg",
                             "bmp",
                             "ico"]
        self.audioFormats = ["wav", "mp3", "ogg"]
        self.videoFormats = ["mp4", "mkv", "mov", "avi"]
        self.archiveFormats = ["zip", "rar", "lnk"]

        # other
        self.possibleQueriesListboxMaxHeight = 5

    def __init__(self):
        self.lastText = ""

        def incorrectPath():
            self.outputText.insert("end", "Path to file is incorrect or file does not exist\n")
            answer = tkinter.messagebox.askyesno("Todo file path change", "Change todo file path?")
            if answer == True:
                self.todoFilePath = tkinter.filedialog.askopenfilename()
                file = open("todoFilePath", "w")
                file.write(self.todoFilePath)
                self.outputText.insert("end", f"Path to todo file set to \"{self.todoFilePath}\"\n")

        def isPossibleQueryParam(param, possibleQueryParams):
            if param != "" and param != " ":
                for i in possibleQueryParams:
                    if param in i:
                        return True
            return False

        def runSomething(args):
            # get type of query
            # possible:
            # "\"todo\" to get a list of tasks that you wrote earlier to complete\n"
            # "\"check <folder path>\" to get information of files in folder\n"
            # "\"run <app name>\" to run app you want\n"
            # "\"search <search query>\" to search something in google chrome\n"
            # "\"algorithm\" to create algorithm that computer will execute automatically\n\n"
            query = self.mainEntry.get().lower()
            queryType, queryParam = splitByTwoWords(query)
            queryParam = queryParam.replace("/", "\\")
            queryParam = queryParam.lower()
            # for i in self.queryTypes:
            #     if queryType in i:
            #         queryTypeIndex = self.queryTypes.index(i)
            #         queryType = self.queryTypes[queryTypeIndex]

            self.outputText.config(state="normal")
            if queryType == "todo" or queryType == "todo ":
                if self.todoFilePath != "":
                    returnedData = self.getFileInformation(self.todoFilePath)
                    if returnedData == False:
                        incorrectPath()
                else:
                    incorrectPath()

            if queryType in "translate " or queryType in "gthtdjlxbr":
                webbrowser.open("https://www.google.com/search?q=translate&oq=translate&aqs=chrome.0.69i59j0i131i433i512j0i512j0i433i512l2j69i60l3.1265j0j7&sourceid=chrome&ie=UTF-8")
                time.sleep(2)
                for i in range(19):
                    keyboard.press_and_release("tab")
                    time.sleep(0.01)

            if queryType in "calendar":
                openCalendar(None)

            if queryParam != "" and queryParam != " ":
                if queryType == "run" or queryType == "run ":
                    try:
                        index = -1
                        # get index of app in self.appNames
                        for i in self.appNames:
                            if queryParam in i:
                                index = self.appNames.index(i)
                                break
                        wsh = win32com.client.Dispatch("WScript.Shell")
                        if index != -1:
                            try:
                                wsh.Run("\"" + self.appPaths[index] + "\"")
                                self.outputText.insert("end", f"running {self.appNames[index].capitalize()}\n")
                            except IndexError:
                                self.outputText.insert("end", f"not yet implemented :) (IndexError while getting appPaths using index (index: {index}))\n")
                        else:
                            self.outputText.insert("end", "unknown app\n")
                            answer = tkinter.messagebox.askyesno("File not found", "Incorrect path to app or app does not exists.\n Do you want to set path to this app?")
                            if answer == True:
                                file = tkinter.filedialog.askopenfile()
                                # saving file path to file
                                fileToSave = open(f"savedData/run/RUN_{queryParam}.txt", "w")
                                fileToSave.write(file.name)
                                fileToSave.close()

                    except ValueError:
                        self.outputText.insert("end", "you used the \"run\" command incorrectly. Usage: \"run <app name>\"\n")
                    except IndexError:
                        self.outputText.insert("end", "you used the \"run\" command incorrectly. Usage: \"run <app name>\"\n")

                if queryType == "checkfile" or queryType == "checkfile ":
                    self.getFileInformation(queryParam)

                if queryType == "checkfolder" or queryType == "checkfolder ":
                    self.getFolderInformation(queryParam)

                if queryType == "search" or queryType == "search ":
                    webbrowser.open("https://google.com")
                    time.sleep(1)
                    wsh = win32com.client.Dispatch("WScript.Shell")
                    for j in f"{queryParam}~":
                        wsh.SendKeys(j)
                        time.sleep(0.01)

                if queryType == "search1" or queryType == "search1 ":
                    webbrowser.open("https://google.com")
                    time.sleep(2)
                    wsh = win32com.client.Dispatch("WScript.Shell")
                    for j in f"{queryParam}~":
                        wsh.SendKeys(j)
                        time.sleep(0.01)
                    time.sleep(1)
                    for j in range(19):
                        keyboard.press_and_release("tab")
                        time.sleep(0.01)

            self.outputText.config(state="disabled")

            # self.outputText.see("end")

        def runSelectedApp(args):
            # listBoxElementIndex = self.possibleQueriesListbox.curselection()[0]
            # self.mainEntry.insert("end", self.possibleQueriesListbox.get(listBoxElementIndex))
            runSomething(args)

        def onClosing():
            self.saveData()
            self.root.destroy()

        def deleteHint(args):
            if self.mainEntry.get() == "Run, find, execute anything":
                self.mainEntry.config(fg="white")
                self.mainEntry.delete(0, "end")

        def enterHint(args):
            if self.mainEntry.get() == "":
                self.mainEntry.config(fg="gray")
                self.mainEntry.insert(0, "Run, find, execute anything")
                self.root.focus()

        def insertInformation(string: str, tag=None):
            self.outputText.insert("end", string, tag)

        def possibleQueries():
            #     query = self.mainEntry.get().lower()
            #     queryType, queryParam = splitByTwoWords(query)
            #
            #     # showing possible queryTypes
            #     if self.lastText.lower() != query:
            #         possibleQueryTypes = findWordsWithText(queryType, self.queryTypes)
            #         self.possibleQueriesListbox.delete(0, "end")
            #         possibleQueriesListboxHeight = len(possibleQueryTypes)
            #         if possibleQueriesListboxHeight > self.possibleQueriesListboxMaxHeight:
            #             possibleQueriesListboxHeight = self.possibleQueriesListboxMaxHeight
            #         self.possibleQueriesListbox.config(height=possibleQueriesListboxHeight)
            #         for i in possibleQueryTypes:
            #             self.possibleQueriesListbox.insert("end", i)
            #
            #         if isPossibleQueryParam(queryParam, self.appNames):
            #             if queryType == "run" or queryType == "run ":
            #                 # showing possible apps to run
            #                 possibleAppNames = findWordsWithText(queryParam, self.appNames)
            #                 self.possibleQueriesListbox.delete(0, "end")
            #                 possibleQueriesListboxHeight = len(possibleAppNames)
            #                 if possibleQueriesListboxHeight > self.possibleQueriesListboxMaxHeight:
            #                     possibleQueriesListboxHeight = self.possibleQueriesListboxMaxHeight
            #                 self.possibleQueriesListbox.config(height=possibleQueriesListboxHeight)
            #                 for i in possibleAppNames:
            #                     self.possibleQueriesListbox.insert("end", i)
            #
            #     self.lastText = query
            #
            def drawKeyboardHeatmapIfKeyPressed(k):
                if keyboard.is_pressed(str(k)):
                    drawKeyboardHeatmap(PassClass(ord(k)))

            for k in self.zeroRowKeys:
                drawKeyboardHeatmapIfKeyPressed(k)
            for k in self.firstRowKeys:
                drawKeyboardHeatmapIfKeyPressed(k)
            for k in self.secondRowKeys:
                drawKeyboardHeatmapIfKeyPressed(k)
            for k in self.thirdRowKeys:
                drawKeyboardHeatmapIfKeyPressed(k)

            self.root.after(5, possibleQueries)

        def drawKeyboardHeatmap(key):
            v = key.keycode
            if v == 219:
                k = "["
            elif v == 221:
                k = "]"
            elif v == 220:
                k = "\\"
            elif v == 189:
                k = "-"
            elif v == 187:
                k = "="
            elif v == 186:
                k = ";"
            elif v == 222:
                k = "'"
            elif v == 188:
                k = ","
            elif v == 190:
                k = "."
            elif v == 191:
                k = "/"
            else:
                k = chr(v).lower()
                if not k.isprintable():
                    k = "<unprintable>"
                    pk = self.lastKey
                else:
                    self.lastKey = k
                    pk = self.lastKey
            # print(k, v)
            self.keyboardHeatmapCanvas.delete("all")

            # draw current typed letter
            if k in self.zeroRowKeys:
                index = self.zeroRowKeys.index(k)
                self.zeroRowKeysHeat[index][0] += self.heatUpSpeed
                self.zeroRowKeysHeat[index][1] += self.heatUpSpeed
                if self.zeroRowKeysHeat[index][0] > 255:
                    self.zeroRowKeysHeat[index][0] = 255
                if self.zeroRowKeysHeat[index][1] > 255:
                    self.zeroRowKeysHeat[index][1] = 255
                if self.zeroRowKeysHeat[index][2] > 255:
                    self.zeroRowKeysHeat[index][2] = 255

            if k in self.firstRowKeys:
                index = self.firstRowKeys.index(k)
                self.firstRowKeysHeat[index][0] += self.heatUpSpeed
                self.firstRowKeysHeat[index][1] += self.heatUpSpeed
                if self.firstRowKeysHeat[index][0] > 255:
                    self.firstRowKeysHeat[index][0] = 255
                if self.firstRowKeysHeat[index][1] > 255:
                    self.firstRowKeysHeat[index][1] = 255
                if self.firstRowKeysHeat[index][2] > 255:
                    self.firstRowKeysHeat[index][2] = 255

            if k in self.secondRowKeys:
                index = self.secondRowKeys.index(k)
                self.secondRowKeysHeat[index][0] += self.heatUpSpeed
                self.secondRowKeysHeat[index][1] += self.heatUpSpeed
                if self.secondRowKeysHeat[index][0] > 255:
                    self.secondRowKeysHeat[index][0] = 255
                if self.secondRowKeysHeat[index][1] > 255:
                    self.secondRowKeysHeat[index][1] = 255
                if self.secondRowKeysHeat[index][2] > 255:
                    self.secondRowKeysHeat[index][2] = 255

            if k in self.thirdRowKeys:
                index = self.thirdRowKeys.index(k)
                self.thirdRowKeysHeat[index][0] += self.heatUpSpeed
                self.thirdRowKeysHeat[index][1] += self.heatUpSpeed
                if self.thirdRowKeysHeat[index][0] > 255:
                    self.thirdRowKeysHeat[index][0] = 255
                if self.thirdRowKeysHeat[index][1] > 255:
                    self.thirdRowKeysHeat[index][1] = 255
                if self.thirdRowKeysHeat[index][2] > 255:
                    self.thirdRowKeysHeat[index][2] = 255

            # draw keyboardHeatmap
            for i in range(len(self.zeroRowKeys)):
                if k == self.zeroRowKeys[i]:
                    color = [255, 255, 255]
                else:
                    color = [self.zeroRowKeysHeat[i][0], 0, 255 - self.zeroRowKeysHeat[i][1]]
                self.keyboardHeatmapCanvas.create_rectangle(
                    i * self.keyboardScale, 0, (i + 1) * self.keyboardScale, self.keyboardScale,
                    fill=rgbToHex(color)
                )
                self.keyboardHeatmapCanvas.create_text(
                    i * self.keyboardScale + self.keyboardScale / 2, self.keyboardScale / 2,
                    fill="black", text=str(self.zeroRowKeys[i])
                )

                self.zeroRowKeysHeat[i][0] -= self.heatDownSpeed
                self.zeroRowKeysHeat[i][1] -= self.heatDownSpeed
                if self.zeroRowKeysHeat[i][0] < 0:
                    self.zeroRowKeysHeat[i][0] = 0
                if self.zeroRowKeysHeat[i][1] < 0:
                    self.zeroRowKeysHeat[i][1] = 0
                if self.zeroRowKeysHeat[i][2] < 0:
                    self.zeroRowKeysHeat[i][2] = 0

            for i in range(len(self.firstRowKeys)):
                if k == self.firstRowKeys[i]:
                    color = [255, 255, 255]
                else:
                    color = [self.firstRowKeysHeat[i][0], 0, 255 - self.firstRowKeysHeat[i][1]]
                self.keyboardHeatmapCanvas.create_rectangle(
                    i * self.keyboardScale, self.keyboardScale, (i + 1) * self.keyboardScale, self.keyboardScale * 2,
                    fill=rgbToHex(color)
                )
                self.keyboardHeatmapCanvas.create_text(
                    i * self.keyboardScale + self.keyboardScale / 2, self.keyboardScale + self.keyboardScale / 2,
                    fill="black", text=str(self.firstRowKeys[i])
                )

                self.firstRowKeysHeat[i][0] -= self.heatDownSpeed
                self.firstRowKeysHeat[i][1] -= self.heatDownSpeed
                if self.firstRowKeysHeat[i][0] < 0:
                    self.firstRowKeysHeat[i][0] = 0
                if self.firstRowKeysHeat[i][1] < 0:
                    self.firstRowKeysHeat[i][1] = 0
                if self.firstRowKeysHeat[i][2] < 0:
                    self.firstRowKeysHeat[i][2] = 0

            for i in range(len(self.secondRowKeys)):
                if k == self.secondRowKeys[i]:
                    color = [255, 255, 255]
                else:
                    color = [self.secondRowKeysHeat[i][0], 0, 255 - self.secondRowKeysHeat[i][1]]
                self.keyboardHeatmapCanvas.create_rectangle(
                    i * self.keyboardScale, self.keyboardScale * 2, (i + 1) * self.keyboardScale, self.keyboardScale * 3,
                    fill=rgbToHex(color)
                )
                self.keyboardHeatmapCanvas.create_text(
                    i * self.keyboardScale + self.keyboardScale / 2, self.keyboardScale * 2 + self.keyboardScale / 2,
                    fill="black", text=str(self.secondRowKeys[i])
                )

                self.secondRowKeysHeat[i][0] -= self.heatDownSpeed
                self.secondRowKeysHeat[i][1] -= self.heatDownSpeed
                if self.secondRowKeysHeat[i][0] < 0:
                    self.secondRowKeysHeat[i][0] = 0
                if self.secondRowKeysHeat[i][1] < 0:
                    self.secondRowKeysHeat[i][1] = 0
                if self.secondRowKeysHeat[i][2] < 0:
                    self.secondRowKeysHeat[i][2] = 0

            for i in range(len(self.thirdRowKeys)):
                if k == self.thirdRowKeys[i]:
                    color = [255, 255, 255]
                else:
                    color = [self.thirdRowKeysHeat[i][0], 0, 255 - self.thirdRowKeysHeat[i][1]]
                self.keyboardHeatmapCanvas.create_rectangle(
                    i * self.keyboardScale, self.keyboardScale * 3, (i + 1) * self.keyboardScale, self.keyboardScale * 4,
                    fill=rgbToHex(color)
                )
                self.keyboardHeatmapCanvas.create_text(
                    i * self.keyboardScale + self.keyboardScale / 2, self.keyboardScale * 3 + self.keyboardScale / 2,
                    fill="black", text=str(self.thirdRowKeys[i])
                )

                self.thirdRowKeysHeat[i][0] -= self.heatDownSpeed
                self.thirdRowKeysHeat[i][1] -= self.heatDownSpeed
                if self.thirdRowKeysHeat[i][0] < 0:
                    self.thirdRowKeysHeat[i][0] = 0
                if self.thirdRowKeysHeat[i][1] < 0:
                    self.thirdRowKeysHeat[i][1] = 0
                if self.thirdRowKeysHeat[i][2] < 0:
                    self.thirdRowKeysHeat[i][2] = 0

            # draw current letter
            self.keyboardHeatmapCanvas.create_text(270, self.keyboardScale / 0.2, text=f"Current letter: {pk}", font=("Courier", 40), fill="white")

        def openFile(event):
            index = event.widget.index("@%s,%s" % (event.x, event.y))
            # getting number before dot
            lineIndex = ""
            for i in str(index):
                if i == ".":
                    break
                lineIndex += i
            filePath = self.outputText.get(f"{lineIndex}.0", f"{lineIndex}.end")[3:-3]
            filePath = f"\"{filePath}\""
            if filePath.rfind(".py") != -1:
                answer = tkinter.messagebox.askyesnocancel("Choose app", "Do you want to open this file in the notepad?\n If not, file will be opened in the default app")
                if answer == True:
                    openedFileThread = threading.Thread(target=os.system, args=[f"notepad {filePath}"])
                    openedFileThread.start()
                elif answer == False:
                    openedFileThread = threading.Thread(target=os.system, args=[filePath])
                    openedFileThread.start()
            else:
                openedFileThread = threading.Thread(target=os.system, args=[filePath])
                openedFileThread.start()

        def openCalendar(event):
            self.outputText.pack_forget()
            self.calendarCanvas.pack(fill="both", expand=True)
            self.backFromCalendarButton.pack(anchor="nw")

        def closeCalendar(event=None):
            self.calendarCanvas.pack_forget()
            self.outputText.pack(fill="both", expand=True)
            self.backFromCalendarButton.pack_forget()

        self.root = tkinter.Tk()
        self.root.title("VirtualDev")
        self.root.state("zoomed")
        self.WIDTH = self.root.winfo_screenwidth()
        self.HEIGHT = self.root.winfo_screenheight()
        self.configuration()
        self.root.config(background=self.bgColor)
        self.root.resizable(False, False)

        self.mainEntry = tkinter.Entry(self.root, bg=self.bgColor, fg="gray", justify="center", font=("Courier", 20), insertbackground="white")
        self.mainEntry.insert(0, "Run, find, execute anything")
        self.outputText = tkinter.Text(self.root, relief="flat", bg=self.bgColor, fg="white", font=("Courier", 18), insertbackground="white", wrap="none")
        # highlightthickness removes light gray border around widget
        self.keyboardHeatmapCanvas = tkinter.Canvas(self.root, bg=self.bgColor, highlightthickness=0)

        # calendar
        self.calendarCanvas = tkinter.Canvas(self.root, bg=self.bgColor, highlightthickness=0)
        self.backFromCalendarButton = tkinter.Button(self.mainEntry, text="back", bg=self.bgColor, fg="white", relief="flat", font=self.buttonsFont,
                                                     command=closeCalendar, activebackground=self.bgColor, activeforeground="white")
        self.createCalendar()

        # scrollbars for self.outputText
        self.outputTextYScrollbar = tkinter.ttk.Scrollbar(self.outputText, command=self.outputText.yview)
        self.outputTextXScrollbar = tkinter.ttk.Scrollbar(self.outputText, command=self.outputText.xview, orient="horizontal")
        # styling the scrollbars
        style = tkinter.ttk.Style()
        style.theme_use('clam')
        # list the options of the style
        # # (Argument should be an element of TScrollbar, eg. "thumb", "trough", ...)
        # print(style.element_options("Horizontal.TScrollbar.thumb"))
        # configure the style
        style.configure("Horizontal.TScrollbar", gripcount=0,
                        background="black", darkcolor="white", lightcolor="white",
                        troughcolor="black", bordercolor="black", arrowcolor="black")
        style.configure("Vertical.TScrollbar", gripcount=0,
                        background="black", darkcolor="white", lightcolor="white",
                        troughcolor="black", bordercolor="black", arrowcolor="black")
        # Create and show a widget using the custom style
        self.outputTextXScrollbar.config(style="My.Horizontal.TScrollbar")
        self.outputTextYScrollbar.config(style="My.Vertical.TScrollbar")
        self.outputText.config(xscrollcommand=self.outputTextXScrollbar.set, yscrollcommand=self.outputTextYScrollbar.set)

        # text formats
        for i in self.textFormats:
            self.outputText.tag_config(i, font=self.filesFont, foreground=self.textFilesColor)
        # image formats
        for i in self.imageFormats:
            self.outputText.tag_config(i, font=self.filesFont, foreground=self.imageFilesColor)
        # audio formats
        for i in self.audioFormats:
            self.outputText.tag_config(i, font=self.filesFont, foreground=self.audioFilesColor)
        # video formats
        for i in self.videoFormats:
            self.outputText.tag_config(i, font=self.filesFont, foreground=self.videoFilesColor)
        # archive formats
        for i in self.archiveFormats:
            self.outputText.tag_config(i, font=self.filesFont, foreground=self.archiveFilesColor)
        # calendar
        self.outputText.tag_config("calendar", font=self.filesFont, foreground=self.calendarForeground)

        # text formats
        for i in self.textFormats:
            self.outputText.tag_bind(i, "<Button-1>", openFile)
        # image formats
        for i in self.imageFormats:
            self.outputText.tag_bind(i, "<Button-1>", openFile)
        # audio formats
        for i in self.audioFormats:
            self.outputText.tag_bind(i, "<Button-1>", openFile)
        # video formats
        for i in self.videoFormats:
            self.outputText.tag_bind(i, "<Button-1>", openFile)
        # archive formats
        for i in self.archiveFormats:
            self.outputText.tag_bind(i, "<Button-1>", openFile)
        # calendar
        self.outputText.tag_bind("calendar", "<Button-1>", openCalendar)

        self.mainEntry.bind("<Return>", runSomething)
        self.mainEntry.bind("<Enter>", deleteHint)
        self.mainEntry.bind("<FocusIn>", deleteHint)
        self.mainEntry.bind("<Leave>", enterHint)
        self.mainEntry.bind("<FocusOut>", enterHint)
        self.backFromCalendarButton.bind("<Return>", closeCalendar)
        # self.possibleQueriesListbox.bind("<Return>", runSelectedApp)
        # self.possibleQueriesListbox.bind("<ButtonRelease-1>", runSelectedApp)
        # for i in self.appNames:
        #     self.possibleQueriesListbox.insert("end", i)
        drawKeyboardHeatmap(PassClass)
        possibleQueries()

        self.mainEntry.pack(fill="x")
        # self.possibleQueriesListbox.pack(fill="x")
        self.outputText.pack(fill="both", expand=True)
        # self.keyboardHeatmapCanvas.pack(side="right", fill="both", expand=True)
        # self.something.pack(fill="x")
        self.outputTextXScrollbar.pack(side='bottom', fill='x')
        self.outputTextYScrollbar.pack(side='right', fill='y')

        self.outputText.config(state="normal")

        insertInformation("VirtualDev started\nLoading latest run data...\n\n")
        self.loadLatestRunData()
        insertInformation(" Welcome back!\n\n")
        insertInformation(" - type \"translate\" to open Google Translate\n")
        insertInformation(" - type \"checkfile <file path>\" to get information of files in folder\n")
        insertInformation(" - type \"checkfolder <folder path>\" to get information of files in folder\n")
        insertInformation(" - type \"run <app name>\" to run app you want\n")
        insertInformation(" - type \"search <search query>\" to search something in the internet\n")
        insertInformation(" - type \"algorithm\" to create algorithm that computer will execute automatically\n")
        insertInformation(" - type \"")
        insertInformation("calendar", "calendar")
        insertInformation("\" to open ")
        insertInformation("calendar", "calendar")
        insertInformation("\n")
        insertInformation(" - type \"exit\" to exit the VirtualDev\n\n")

        # self.outputText.see("end")
        self.outputText.config(state="disabled")

        self.root.protocol("WM_DELETE_WINDOW", onClosing)

        self.root.mainloop()


def splitByTwoWords(text):
    queryType = ""
    queryParam = ""
    queryTypeIndex = 10000
    firstSpaceIndex = 0
    for c in text:
        if c == " ":
            break
        firstSpaceIndex += 1
    queryType = text[:firstSpaceIndex]
    queryParam = text[firstSpaceIndex + 1:]
    return queryType, queryParam


def findWordsWithText(word, listOfWords):
    foundWords = []
    for i in listOfWords:
        if word in i:
            foundWords.append(i)
    return foundWords


def degToRad(degree):
    return degree * math.pi / 180


def rgbToHex(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    r, g, b = rgb
    r = int(r);
    g = int(g);
    b = int(b)
    return f'#{r:02x}{g:02x}{b:02x}'


if __name__ == "__main__":
    App()
