import copy
from tkinter import LEFT
import threading
import datetime
import numpy as np
import tkinter as tk

###################İnput Alma Başladı#########################

sudoku = np.negative(np.ones((21, 21), dtype=np.int32))
file = open("sudoku.txt", "r")
Lines = file.readlines()
print(Lines)
count1 = 0
for line in Lines:
    # 1-6 15-21 satır
    if count1 < 6 or count1 >= 15:
        count2 = 0
        for i in line:
            if count2 < 9:
                if line[count2] == "*":
                    sudoku[count1][count2] = 0
                    count2 += 1
                else:
                    sudoku[count1][count2] = int(line[count2])
                    count2 += 1
            elif (count2 >= 9) and (count2 < 18):
                if line[count2] == "*":
                    sudoku[count1][count2 + 3] = 0
                    count2 += 1
                elif line[count2] == "\n":
                    continue
                else:
                    sudoku[count1][count2 + 3] = int(line[count2])
                    count2 += 1
        count1 += 1
    # 7-9  12-15 satır
    elif ((count1 >= 6) and (count1 < 9)) or ((count1 >= 12) and (count1 < 15)):
        count2 = 0
        for i in line:
            if count2 < 21:
                if line[count2] == "*":
                    sudoku[count1][count2] = 0
                    count2 += 1
                elif line[count2] == "\n":
                    continue
                else:
                    sudoku[count1][count2] = int(line[count2])
                    count2 += 1
        count1 += 1
    # 9-12 satır
    elif (count1 >= 9) and (count1 < 12):
        count2 = 0
        for i in line:
            if count2 < 9:
                if line[count2] == "*":
                    sudoku[count1][count2 + 6] = 0
                    count2 += 1
                elif line[count2] == "\n":
                    continue
                else:
                    sudoku[count1][count2 + 6] = int(line[count2])
                    count2 += 1
        count1 += 1

print(sudoku)
sudoku2 = copy.deepcopy(sudoku)
file.close()


###################İnput Alma Bitti#########################

###################Sudoku-Çözüm#########################
class Solver():

    def __init__(self, x, y, s, x2, y2):
        self.x = x
        self.y = y
        self.file = open('readme.txt', 'w')

    def solve(self, x, y):
        print(threading.current_thread().name)
        find = self.bos_bul(x, y)
        if not find:
            return True
        else:
            row, col = find
            print(find)
        for i in range(1, 10):
            if self.is_valid(x, y, i, (row, col)):
                threadLock.acquire()
                self.file.write(str(sudoku))
                sudoku[row + y][col + x] = i
                threadLock.release()
                if self.solve(x, y):
                    return True
                self.file.write(str(sudoku))
                threadLock.acquire()
                sudoku[row + y][col + x] = 0
                threadLock.release()
        return False

    def solve2(self, x, y, s, x2, y2):
        print(threading.current_thread().name)
        find = self.bos_bul2(x, y, s, x2, y2)
        if not find:
            return True
        else:
            row, col = find
            print(find)
        for i in range(1, 10):
            if self.is_valid2(x, y, i, (row, col)):
                threadLock.acquire()
                self.file.write(str(sudoku))
                sudoku2[row + y][col + x] = i
                threadLock.release()
                if self.solve2(x, y, s, x2, y2):
                    return True
                self.file.write(str(sudoku))
                threadLock.acquire()
                sudoku2[row + y][col + x] = 0
                threadLock.release()
        return False

    def solve3(self, x, y, s, x2, y2):
        print(threading.current_thread().name)
        find = self.bos_bul1(x, y, s, x2, y2)
        if not find:
            return True
        else:
            row, col = find
            print(find)
        for i in range(1, 10):
            if self.is_valid2(x, y, i, (row, col)):
                threadLock.acquire()
                self.file.write(str(sudoku))
                sudoku2[row + y][col + x] = i
                threadLock.release()
                if self.solve3(x, y, s, x2, y2):
                    return True
                self.file.write(str(sudoku))
                threadLock.acquire()
                sudoku2[row + y][col + x] = 0
                threadLock.release()
        return False

    def is_valid2(self, x, y, num, pos):
        # satırkontrol
        threadLock.acquire()
        for i in range(9):
            if sudoku2[pos[0] + y][i + x] == num and pos[1] + x != i:
                threadLock.release()
                return False
        # sütunkontrol
        for i in range(9):
            if sudoku2[i + y][pos[1] + x] == num and pos[0] + y != i:
                threadLock.release()
                return False
        # boxkontrol
        kutu_x = pos[1] // 3
        kutu_y = pos[0] // 3
        for i in range((kutu_y * 3) + y, (kutu_y * 3) + y + 3):
            for j in range((kutu_x * 3) + x, (kutu_x * 3) + x + 3):
                if sudoku2[i][j] == num and (i, j) != pos:
                    threadLock.release()
                    return False
        # ilk ortak kutu
        if (x == 0 and y == 0 and kutu_x == 2 and kutu_y == 2) or (
                x == 0 and y == 12 and kutu_x == 2 and kutu_y == 0) or (
                x == 12 and y == 12 and kutu_x == 0 and kutu_y == 0) or (
                x == 12 and y == 0 and kutu_x == 0 and kutu_y == 2):
            # satır
            for i in range(9):
                if sudoku2[pos[0] + y][6 + i] == num and (i, j) != pos:
                    threadLock.release()
                    return False
            # sütun
            for i in range(9):
                if sudoku2[6 + i][pos[1] + x] == num and (i, j) != pos:
                    threadLock.release()
                    return False
        if (x == 6 and y == 6):
            if kutu_x == 0 and kutu_y == 0:
                for i in range(9):
                    if sudoku2[pos[0] + y][i] == num and pos[1] + x != i:
                        threadLock.release()
                        return False
                for i in range(9):
                    if sudoku2[i][pos[1] + x] == num and pos[0] + y != i:
                        threadLock.release()
                        return False
            elif kutu_x == 2 and kutu_y == 0:
                for i in range(9):
                    if sudoku2[pos[0] + y][i + 12] == num and pos[1] + x != i:
                        threadLock.release()
                        return False
                for i in range(9):
                    if sudoku2[i][pos[1] + x] == num and pos[0] + y != i:
                        threadLock.release()
                        return False
            elif kutu_x == 0 and kutu_y == 2:
                for i in range(9):
                    if sudoku2[pos[0] + y][i] == num and pos[1] + x != i:
                        threadLock.release()
                        return False
                for i in range(9):
                    if sudoku2[i + 12][pos[1] + x] == num and pos[0] + y != i:
                        threadLock.release()
                        return False
            elif kutu_x == 2 and kutu_y == 2:
                for i in range(9):
                    if sudoku2[pos[0] + y][i + 12] == num and pos[1] + x != i:
                        threadLock.release()
                        return False
                for i in range(9):
                    if sudoku2[i + 12][pos[1] + x] == num and pos[0] + y != i:
                        threadLock.release()
                        return False
        threadLock.release()
        return True

    def is_valid(self, x, y, num, pos):
        # satırkontrol
        threadLock.acquire()
        for i in range(9):
            if sudoku[pos[0] + y][i + x] == num and pos[1] + x != i:
                threadLock.release()
                return False
        # sütunkontrol
        for i in range(9):
            if sudoku[i + y][pos[1] + x] == num and pos[0] + y != i:
                threadLock.release()
                return False
        # boxkontrol
        kutu_x = pos[1] // 3
        kutu_y = pos[0] // 3
        for i in range((kutu_y * 3) + y, (kutu_y * 3) + y + 3):
            for j in range((kutu_x * 3) + x, (kutu_x * 3) + x + 3):
                if sudoku[i][j] == num and (i, j) != pos:
                    threadLock.release()
                    return False
        # ilk ortak kutu
        if (x == 0 and y == 0 and kutu_x == 2 and kutu_y == 2) or (
                x == 0 and y == 12 and kutu_x == 2 and kutu_y == 0) or (
                x == 12 and y == 12 and kutu_x == 0 and kutu_y == 0) or (
                x == 12 and y == 0 and kutu_x == 0 and kutu_y == 2):
            # satır
            for i in range(9):
                if sudoku[pos[0] + y][6 + i] == num and (i, j) != pos:
                    threadLock.release()
                    return False
            # sütun
            for i in range(9):
                if sudoku[6 + i][pos[1] + x] == num and (i, j) != pos:
                    threadLock.release()
                    return False
        if (x == 6 and y == 6):
            if kutu_x == 0 and kutu_y == 0:
                for i in range(9):
                    if sudoku[pos[0] + y][i] == num and pos[1] + x != i:
                        threadLock.release()
                        return False
                for i in range(9):
                    if sudoku[i][pos[1] + x] == num and pos[0] + y != i:
                        threadLock.release()
                        return False
            elif kutu_x == 2 and kutu_y == 0:
                for i in range(9):
                    if sudoku[pos[0] + y][i + 12] == num and pos[1] + x != i:
                        threadLock.release()
                        return False
                for i in range(9):
                    if sudoku[i][pos[1] + x] == num and pos[0] + y != i:
                        threadLock.release()
                        return False
            elif kutu_x == 0 and kutu_y == 2:
                for i in range(9):
                    if sudoku[pos[0] + y][i] == num and pos[1] + x != i:
                        threadLock.release()
                        return False
                for i in range(9):
                    if sudoku[i + 12][pos[1] + x] == num and pos[0] + y != i:
                        threadLock.release()
                        return False
            elif kutu_x == 2 and kutu_y == 2:
                for i in range(9):
                    if sudoku[pos[0] + y][i + 12] == num and pos[1] + x != i:
                        threadLock.release()
                        return False
                for i in range(9):
                    if sudoku[i + 12][pos[1] + x] == num and pos[0] + y != i:
                        threadLock.release()
                        return False
        threadLock.release()
        return True

    def bos_bul(self, x, y):
        threadLock.acquire()
        for k in reversed(range(9)):
            for j in  range(9):
                if sudoku[k + y][j + x] == 0:
                    threadLock.release()
                    return k, j
        threadLock.release()
        return None

    def bos_bul1(self, x, y, s, x2, y2):
        threadLock.acquire()
        for k in range(y2 - y):
            for j in range(9):
                if sudoku2[k + y][j + x] == 0:
                    threadLock.release()
                    return k, j
        threadLock.release()
        return None

    def bos_bul2(self, x, y, s, x2, y2):
        threadLock.acquire()
        for k in range(y2 - y, 9):
            for j in reversed(range(9)):
                if sudoku2[k + y][j + x] == 0:
                    threadLock.release()
                    return k, j
        threadLock.release()
        return None


###################Sudoku-Çözüm#########################


###################Arayüz#########################
class Window(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas1 = tk.Canvas(self, width=504, height=504, bg="#ffffff", borderwidth=3, relief="sunken")
        self.canvas1.pack(side=LEFT)
        self.canvas2 = tk.Canvas(self, width=504, height=504, bg="#000000", borderwidth=3, relief="sunken")
        self.canvas2.pack()
        self.submit = tk.Button(self, text="5-Threadli", command=self.on_submit, borderwidth=3, relief="raised")
        self.submit.pack()
        self.submit2 = tk.Button(self, text="10-Threadli", command=self.on_submit2, borderwidth=3, relief="raised")
        self.submit2.pack()
        self.drawGraph()
        self.drawSudoku(0)

    def drawcanvas(self, s):
        self.canvas1.delete('all')
        self.drawSudoku(s)

    def drawLinesOnGraph(self, c):
        c = c.total_seconds()
        self.canvas2.create_line(252, 252, 252 + (c * 15), 178.5, fill="blue", width=3)
        self.canvas2.create_text(252+(c*15),252,text=str(c//1),fill="white")

    def drawGraph(self):
        self.canvas2.create_line(0, 252, 504, 252, fill="green", width=3)
        self.canvas2.create_line(252, 0, 252, 504, fill="green", width=3)
        self.canvas2.create_text(25,252,text="Zaman",fill="white")
        self.canvas2.create_text(252,502,text="KareSayısı",fill="white")



    def drawSudoku(self, s):
        if s == 0:
            for i in range(21):
                y = i * 24
                for j in range(21):
                    x = j * 24
                    if (i + j) % 2 == 0 and sudoku[i][j] != -1:
                        self.canvas1.create_rectangle(x, y, x + 24, y + 24, fill="#c1c2ff")
                        self.canvas1.create_text(x + 12, y + 12, text=sudoku[i][j])
                    elif (i + j) % 2 == 1 and sudoku[i][j] != -1:
                        self.canvas1.create_rectangle(x, y, x + 24, y + 24, fill="#836dff")
                        self.canvas1.create_text(x + 12, y + 12, text=sudoku[i][j])
        elif s == 1:
            for i in range(21):
                y = i * 24
                for j in range(21):
                    x = j * 24
                    if (i + j) % 2 == 0 and sudoku2[i][j] != -1:
                        self.canvas1.create_rectangle(x, y, x + 24, y + 24, fill="#c1c2ff")
                        self.canvas1.create_text(x + 12, y + 12, text=sudoku2[i][j])
                    elif (i + j) % 2 == 1 and sudoku2[i][j] != -1:
                        self.canvas1.create_rectangle(x, y, x + 24, y + 24, fill="#836dff")
                        self.canvas1.create_text(x + 12, y + 12, text=sudoku2[i][j])

    def on_submit(self):
        a = datetime.datetime.now()
        self.thread1()
        b = datetime.datetime.now()
        c = b - a
        print(c)
        self.drawcanvas(0)
        self.drawLinesOnGraph(c)

    def on_submit2(self):
        a = datetime.datetime.now()
        self.thread2()
        b = datetime.datetime.now()
        c = b - a
        print(c)
        self.drawcanvas(1)
        self.drawLinesOnGraph(c)

    def thread1(self):
        print("Çözüm kodu çalışıyor")

        threads = []
        thread1 = myThread(1, "Thread-1", 0, 0, 0, 0, 8, 8)
        thread2 = myThread(2, "Thread-2", 12, 0, 0, 0, 21, 8)
        thread3 = myThread(3, "Thread-3", 6, 6, 0, 0, 14, 14)
        thread4 = myThread(4, "Thread-4", 0, 12, 0, 0, 8, 21)
        thread5 = myThread(5, "Thread-5", 12, 12, 0, 0, 21, 21)

        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)
        threads.append(thread4)
        threads.append(thread5)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def thread2(self):
        print("Çözüm kodu çalışıyor")

        threads = []
        thread1 = myThread(1, "Thread-1.1", 0, 0, 1, 0, 0, 4)
        thread2 = myThread(2, "Thread-1.2", 0, 0, 1, 1, 0, 4)

        thread3 = myThread(3, "Thread-2.1", 12, 0, 1, 0, 12, 4)
        thread4 = myThread(4, "Thread-2.2", 12, 0, 1, 1, 12, 4)

        thread5 = myThread(5, "Thread-3.1", 6, 6, 1, 0, 6, 10)
        thread6 = myThread(6, "Thread-3.2", 6, 6, 1, 1, 6, 10)

        thread7 = myThread(7, "Thread-4.1", 0, 12, 1, 0, 0, 16)
        thread8 = myThread(8, "Thread-4.2", 0, 12, 1, 1, 0, 16)

        thread9 = myThread(9, "Thread-5.1", 12, 12, 1, 0, 12, 16)
        thread10 = myThread(10, "Thread-5.2", 12, 12, 1, 1, 12, 16)

        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)
        threads.append(thread4)
        threads.append(thread5)
        threads.append(thread6)
        threads.append(thread7)
        threads.append(thread8)
        threads.append(thread9)
        threads.append(thread10)
        for t in threads:
            t.start()

        for t in threads:
            t.join()


###################ARAYÜZ#########################
class myThread(threading.Thread):
    def __init__(self, threadID, name, x, y, s, s2, x2, y2):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.x = x
        self.y = y
        self.s = s
        self.x2 = x2
        self.y2 = y2
        self.s2 = s2

    def run(self):
        if self.s == 0:
            solver = Solver(self.x, self.y, self.s, self.x2, self.y2)
            solver.solve(self.x, self.y)
        if self.s == 1:
            if self.s2 == 0:
                solver = Solver(self.x, self.y, self.s, self.x2, self.y2)
                solver.solve3(self.x, self.y, self.s, self.x2, self.y2)
            elif self.s2 == 1:
                solver = Solver(self.x, self.y, self.s, self.x2, self.y2)
                solver.solve2(self.x, self.y, self.s, self.x2, self.y2)


print("MainThread=", threading.current_thread().name)
threadLock = threading.Lock()
root = tk.Tk()
root.title("SAMURAI SUDOKU")
root.geometry('1100x650')
Window(root).pack()

root.mainloop()
