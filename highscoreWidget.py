import tkinter as tk
from tkinter import messagebox
import csv, sys

def save_highscore(name, score, diff):
    print('SAVING HIGHSCORE')
    f = open('highscores.csv', 'a')
    writer = csv.writer(f, delimiter=',', lineterminator='\n')
    writer.writerow([name, score, diff])
    f.close()

def load_csv_data():
    f = open('highscores.csv')
    reader = csv.reader(f)
    tempList = []
    for row in reader:
        tempList.append(row)
    f.close()
    return tempList
        
class HighscoreWindow():
    def __init__(self, controlParent):
        self.master = tk.Tk()
        self.master.config(bg = "white")
        self.master.title("Highscores")
        self.master.call('wm', 'attributes', '.', '-topmost', '1') #Keep it on top of ERYTING
        self.master.protocol("WM_DELETE_WINDOW", self.destroy)
        self.controlParent = controlParent
        self.highscoreData = load_csv_data()
        self.radioFrame = tk.Frame(self.master)
        self.HighscoreFrame = tk.Frame(self.master)
        self.radioFrame.grid()
        self.HighscoreFrame.grid()

        self.diffVar = tk.StringVar()
        self.diffVar.set("easy") # initialize

        MODES = [
                ("Easy", "easy", "#ADD633"),
                ("Medium", "medium", "#6699FF"),
                ("Hard", "hard", "#B24C32"),
                ("Custom", "custom", "#CC33FF"),
        ]

        self.diffVar = tk.StringVar(self.master)
        self.diffVar.set("easy") # initialize

        for text, mode, colour in MODES:
            self.b = tk.Radiobutton(self.radioFrame,
                               text = text,
                               variable = self.diffVar,
                               value = mode,
                               indicatoron = 0,
                               bg = '#DDDDDD',
                               bd = 0,
                               width = 11,
                               selectcolor  = colour,
                               relief = tk.SUNKEN,
                               command = self.refresh)
            self.b.pack(anchor='w', side = "left")

        
        self.indexTable = tk.Listbox(master = self.HighscoreFrame,
                                disabledforeground = "black",
                                setgrid = 5,
                                exportselection = 0,
                                bd = 0,
                                width = 2,
                                font = "Calibri 14")
        self.indexTable.grid(row = 0, column = 0)

        self.nameTable = tk.Listbox(master = self.HighscoreFrame,
                               disabledforeground = "black",
                               setgrid = 5,
                               exportselection = 0,
                               bd = 0,
                               width = 15,
                               font = "Calibri 14")
        self.nameTable.grid(row = 0, column = 1)

        self.scoreTable = tk.Listbox(master = self.HighscoreFrame,
                                disabledforeground = "black",
                                exportselection = 0,
                                bd = 0,
                                width = 6,
                                font = "Calibri 14")
        self.scoreTable.grid(row = 0, column = 2)

        self.diffTable = tk.Listbox(master = self.HighscoreFrame,
                               disabledforeground = "black",
                               exportselection = 0,
                               bd = 0,
                               width = 8,
                               font = 'Calibri 14')
        self.diffTable.grid(row = 0, column = 3)

        self.tables = [self.indexTable, self.nameTable, self.scoreTable, self.diffTable]

        self.load()

    def load(self):
        self.highscoreData = load_csv_data()
        data = sorted(self.highscoreData, key = lambda x:x[1], reverse = True)
        data = [x for x in data if x[2] == self.diffVar.get()]
        if len(data) != 0:
            for index in range(10):
                try:
                    name, score, diff = data[index]
                    self.add_highscore(index+1, name, score, diff)
                except IndexError:
                    break

            for box in self.tables:
                box.itemconfig(0, bg = "red")
                
        for box in self.tables:
            box.config(state = tk.DISABLED)

    def clear(self):
        for table in self.tables:
            table.delete(0, tk.END)

    def refresh(self):
        for box in self.tables:
            box.config(state = tk.NORMAL)
        self.clear()
        self.load()

    def add_highscore(self, index, name, score, diff):
        self.indexTable.insert(tk.END, str(index)+'.')
        self.nameTable.insert(tk.END, name)
        self.scoreTable.insert(tk.END, score)
        self.diffTable.insert(tk.END, diff)

    def destroy(self):
        self.controlParent.highscoreWindow = None
        self.master.destroy()

if __name__ == "__main__":
    window = HighscoreWindow(None)

