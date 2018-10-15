import tkinter as tk
from tkinter import messagebox
import time, random, math, re, csv, sys

import highscoreWidget

FPS = 60

root = tk.Tk()

root.geometry("895x480")
root.resizable(0,0)

diffs = {"easy"  : {"lower_range" : 1,
                    "upper_range" : 5,
                    "operators"   : ["+"],
                    "tiles"       : 3,
                    "timer"       : 6,
                    "special_key" : None
                    },

         "medium": {"lower_range" : 2,
                    "upper_range" : 12,
                    "operators"   : ["+", "-", "*"],
                    "tiles"       : 5,
                    "timer"       : 10,
                    "special_key" : lambda x: 1 < x > -1
                    },
                    

         "hard"  : {"lower_range" : -12,
                    "upper_range" : 12,
                    "operators"   : ["*", "/"],
                    "tiles"       : 5,
                    "timer"       : 3,
                    "special_key" : lambda x: x != 0
                    },

         "custom": {"lower_range" : 1,
                    "upper_range" : 12,
                    "operators"   : ["-"],
                    "tiles"       : 6,
                    "timer"       : 10,
                    "special_key" : None
                    }
         }


def generate_question(d):
    lRange, uRange, operators, ntiles, test_func = [d[x] for x in ["lower_range", "upper_range", "operators", "tiles", "special_key"]]
    operand = operators[random.randint(0, len(operators)-1)]
    L = []
    for n in range(ntiles):
        answer = float()
        while type(answer) == type(float()):
            n1 = random.randint(lRange, uRange)
            n2 = random.randint(lRange, uRange)
            
            try:
                if operand == "/": #Special Case
                    answer = n1
                    problem = "{} {} {} = ".format(n1 * n2, operand, n2) 
                else:
                    answer = eval("{}{}{}".format(n1, operand, n2))
                    problem = "{} {} {} = ".format(n1, operand, n2)
                    
            except ZeroDivisionError:
                answer = float()
                
            else:
                if answer in L or answer == 0:
                    answer = float()
                elif test_func != None:
                    if test_func(answer) == False:
                        answer = float()
                    
            
            
        L.append(answer)
        
    random.shuffle(L) 
    
    for i, n in enumerate(L):
        blockList.append(Block(20 + (107*(i)), 80, 100, 100, str(n)))
    
    return problem, answer
    
class Rect():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.points = (x, y, x+width, y+height)

    def get(self):
        return self.points

    def update_parameters(self):
        self.x, self.y, self.width, self.height = self.points

    def update_points(self):
        self.points = (round(self.x), round(self.y), round(self.x+self.width), round(self.y+self.height))

    def get_pos(self):
        return self.x, self.y

    def move_pos(self, pos):
        x, y = pos
        self.x += x
        self.y += y
        self.update_points()

    def set_pos(self, pos):
        x, y = pos
        self.x = x
        self.y = y
        self.update_points()
        
class Block():
    def __init__(self, x, y, width, height, text):
        self.rect = Rect(x, y - 350, width, height)
        self.defaultPos = (x, y)
        self.text = text
        self.selectState = 0
        self.dock = None

    def kill(self):
        self.defaultPos = (self.defaultPos[0] - 800, self.defaultPos[1])
        root.after(500, self.destroy)

    def destory(self):
        blockList.remove(self)
        del self
        
    def checkCollision(self, x, y):
        if self.rect.get()[0] <= x <= self.rect.get()[2]:
            if self.rect.get()[1] <= y <= self.rect.get()[3]:
                if self.dock != None:
                    self.dock.parent = None
                    self.dock = None
                self.run(x, y)
                return 1
            
    def run(self, x, y):
        self.dockedState = 0
        if self.selectState == 1:
            if dock.checkCollision(x, y):
                if dock.parent == None:
                    self.dock_block(dock)
                else:
                    dock.parent.dock = None
                    dock.parent = None
                    self.selectState = 1 - self.selectState
                        
        self.selectState = 1 - self.selectState
        
    def dock_block(self, dock):
        self.dock = dock
        X, Y, w, h = dock.rect.get()
        dock.parent = self
        self.rect.set_pos((X, Y))

    def undock(self):
        if self.dock != None:
            self.dock.parent = None
            self.dock = None
            
        
    def update(self):
        if self.selectState == 1:
            self.rect.move_pos((Main.mousexrel, Main.mouseyrel))
                
        self.draw()

    def destroy(self):
        None
        
    def draw(self):
        if self.selectState != 1 and self.dock == None:
            if self.rect.get_pos() != self.defaultPos:
                x = (self.defaultPos[0] - self.rect.get_pos()[0]) * 0.1
                y = (self.defaultPos[1] - self.rect.get_pos()[1]) * 0.1
                self.rect.move_pos((x, y))
                
        self.colour = ["#6699ff", "#3d5c99"][self.selectState]
        self.outline = "#3d5c99"
        if self.dock != None:
            self.colour = "#ADD633"
            self.outline = self.colour
            
        canvas.create_rectangle(self.rect.get(), fill = self.colour, outline = self.outline)
        canvas.create_text(self.rect.x + self.rect.width/2, self.rect.y + self.rect.height/2, text = str(self.text), font = "calibri 22", fill = "#ffffff")

class Dock():
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
        self.parent = None

    def checkCollision(self, x, y):
        if self.rect.get()[0] <= x <= self.rect.get()[2]:
            if self.rect.get()[1] <= y <= self.rect.get()[3]:
                return 1
        return 0
    
    def reset(self):
        self.parent = None

    def draw(self):
        canvas.create_rectangle(self.rect.get(), fill = "#ffffff", outline = "#cccccc")

class Timer():
    def __init__(self, center, radius, label, ticks):
        self.xpos, self.ypos = center
        self.radius = radius
        self.max = ticks
        self.text = label
        self.ticks = ticks
        self.rect = (self.xpos - radius, self.ypos - radius, self.xpos + radius, self.ypos + radius)
        radius = 15
        self.secondRect = (self.xpos - radius, self.ypos - radius, self.xpos + radius, self.ypos + radius)

    def setTime(self, x):
        self.max = x

    def get_percentage(self):
        percentage = round((self.ticks/self.max)*100, 2)
        return percentage

    def get_decimal(self):
        decimal = round((self.ticks/self.max), 2)
        return decimal

    def reset(self):
        self.ticks = self.max

    def update(self):
        canvas.create_oval(self.rect, fill = "#3D5C99", outline = "#6699FF", width = "2")
        if self.ticks > 2:
            self.ticks -= 1
            self.degrees = 360 * (self.ticks/self.max)
            canvas.create_arc(self.rect, fill="#6699FF", outline = "#6699FF", start=90, extent = -self.degrees)
        else:
            self.ticks = 0
        canvas.create_text(self.xpos, self.ypos, text = str(math.ceil(self.ticks/120)), font = ("Calibri", 14,), fill = "white")
        canvas.create_text(self.xpos, self.ypos-self.radius - 20, text = str(self.text), font = ("Calibri", 14,), fill = "#333")
        
                      
class Control():
    def __init__(self):
        self.mousex, self.mousey = root.winfo_pointerx(), root.winfo_pointery()
        self.mousexrel, self.mouseyrel = 0, 0
        self.highscoreWindow = None

        self.diff = "easy"
        self.questionNumber = 1
        self.questions = 10
        self.correctAnswers = 0
        self.score = 0
        self.speedScore = 0
        
        self.message = ""
        self.messageColour = "black"

    def set_diff(self):
        self.diff = diffVar.get()
        timer.setTime(120*diffs[self.diff]["timer"])

    def start(self):
        playButton.pack_forget()
        quitButton.pack(pady = 5)
        for child in diffSelectFrame.winfo_children():
            child.configure(state= 'disable')
            
        self.reset()
        menuCanvas.grid_remove()
        gameoverCanvas.grid_remove()
        canvas.grid(row = 0, column = 0, columnspan = 3, rowspan = 2, sticky = "nw")
        hintButton.grid  (row = 2, column = 0, sticky = "n", pady = 10)
        answerButton.grid(row = 2, column = 1, sticky = "n", pady = 10)
        resetButton.grid (row = 2, column = 2, sticky = "n", pady = 10)

    def clearGame(self):
        canvas.grid_remove()
        buttons = [answerButton, hintButton, resetButton]
        for button in buttons:
            button.grid_remove()

    def quitButtonPressed(self):
        if gameoverCanvas.grid_info() != {} or messageBox.askyesno(title = "Quit?", message = "Are you sure you want to quit mid-game?", icon = 'warning'):
            Main.end()
            
    def end(self):
        quitButton.pack_forget()
        playButton.pack()
        
        for child in diffSelectFrame.winfo_children():
            #child.configure(bg = '#DDDDDD')
            child.configure(state= 'normal')
            
        self.clearGame()
        gameoverCanvas.grid_remove()
        menuCanvas.grid()
        playButton.config(text = "Start Game")
        
    def gameover(self):
        self.clearGame()
        goc = gameoverCanvas
        goc.delete("all")
        goc.create_text(350, 50, text = "GAME OVER", font = "Calibri, 20", fill = "black")
        goc.create_text(350, 100,
                        text = "You got {} out of {} correct on {}.".format(self.correctAnswers, self.questions, self.diff),
                        font = "Calibri, 18", fill = "black")
        goc.create_text(350, 150, text = "Speed Score Bounus: +{}".format(round(self.speedScore)), font = "Calibri, 14", fill = "black")
        goc.create_text(350, 200, text = "Score: {}".format(str(round(self.score + self.speedScore)).zfill(5)), font = "Calibri, 18", fill = "black")

        highscoreWidget.save_highscore(userLabel.cget("text"), str(round(self.score + self.speedScore)).zfill(5), self.diff)

        #data = highscoreWidget.load_csv_data()
        #lowestScore = sorted([row for row in data], key = lambda x: x[1])[0]
            

            
        if self.highscoreWindow != None: #Refresh the highscore window if its open
            self.highscoreWindow.refresh()
        
        quitButton.pack_forget()
        playButton.config(text = "Play Again?")
        playButton.pack(pady = 5)
        quitButton.pack(pady = 5)
        gameoverCanvas.grid()

    def open_highscores(self):
        if self.highscoreWindow == None:
            self.highscoreWindow = highscoreWidget.HighscoreWindow(self)
        
    def wipeBlocks(self):
        for block in blockList:
            block.kill()
            
    def setMessage(self, text, colour):
        self.message = text
        self.messageColour = colour

    def clearMessage(self):
        self.message = ""
        
    def answer(self):
        if dock.parent != None: #There is an answer in the dock
            if self.answer == int(dock.parent.text): #If the answer is equal to the docked blocks value
                self.setMessage("Correct", "#7AA300")
                self.correctAnswers += 1
                self.score += 100
                self.speedScore += timer.get_decimal() * 50

            else: #Answer is wrong
                self.setMessage("Incorrect", "#B24C32")
                    
            self.questionNumber += 1
            self.freezeButtons()
            self.wipeBlocks()
            root.after(1000, self.next_question)
            root.after(1000, self.clearMessage)
            root.after(1000, self.unfreezeButtons)
        else: #There is no answer in the dock
            self.setMessage("Select an answer", "#B24C32")

    def skip(self):
        self.questionNumber += 1
        self.next_question()

    def hint(self):
        for block in blockList:
            if str(self.answer) != block.text:
                block.kill()
            
    def next_question(self):
        blockList.clear()
        dock.reset()
        if self.questionNumber > self.questions:
            self.gameover()
            return
        else:
            self.question = generate_question(diffs[self.diff])
            self.question, self.answer = self.question
            self.question = self.question.replace("*", "×")
            self.question = self.question.replace("/", "÷")
            timer.reset()
        

    def freezeButtons(self):
        buttons = [answerButton, hintButton, resetButton]
        for button in buttons:
            button.config(state = tk.DISABLED, bg = "#CDCDCD")

    def unfreezeButtons(self):
        buttons = [answerButton, hintButton, resetButton]
        for index, button in enumerate(buttons):
            button.config(state = tk.NORMAL, bg = ["#ADD633", "#6699FF", "#B24C32"][index])
            
    def reset(self):
        self.questionNumber = 1
        self.score = 0
        self.speedScore = 0
        self.correctAnswers = 0
        self.next_question()

    def main_loop(self):
        self.next_question()
        while True:
            time.sleep(1/120)
            
            canvas.delete("all")

            canvas.create_rectangle(10, 10, canvas.winfo_width(), 60, fill = "#dddddd", outline = "#dddddd")
            canvas.create_rectangle(10, 70, canvas.winfo_width(), 190, fill = "#dddddd", outline = "#dddddd")
            canvas.create_rectangle(10, 201, canvas.winfo_width(), canvas.winfo_height(), fill = "#dddddd", outline = "#dddddd")

            #Progress Bar
            canvas.create_rectangle(15, 15, (canvas.winfo_width())/self.questions * (self.questionNumber-1) + 15, 55, fill = "#6699ff", outline = "#6699ff")
            canvas.create_text(canvas.winfo_width()/2, 35, font = "Calibri, 14", text = "{}%".format(round((self.questionNumber-1)/self.questions*100)), fill = "black")
            
            #Math problem
            canvas.create_text(300, 300, text = self.question, font = "Calibri, 40", fill = "#333", anchor = "e")

            #Message
            canvas.create_text(350, 370, text = str(self.message), font = "Calibri, 20", fill = self.messageColour)

            #Mouse pos and rel pos
            self.mousexold, self.mouseyold = self.mousex, self.mousey
            self.mousex, self.mousey = root.winfo_pointerx(), root.winfo_pointery()
            self.mousexrel, self.mouseyrel = self.mousex - self.mousexold, self.mousey - self.mouseyold
            
            timer.update() #Update the countdown timer

            dock.draw() #Draw the dock where tiles are put

            for block in blockList: #Draw all the tiles
                block.update()

            root.update() #Update the tkinter module

def checkMouse(event):
    x, y = event.x, event.y
    for block in reversed(blockList):
        if block.checkCollision(x, y):
            blockList.remove(block)
            blockList.append(block)
            break

def check(d, i, P, s, S, v, V, W):
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %v = the type of validation that is currently set
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # %W = the tk name of the widget

        #print(d, i, P, s, S, v, V, W)

        regexp = re.compile(r'[a-z]')
        
        if regexp.match(S.lower()) and len(P) <= 11:
            if len(P) >= 3:
                loginButton.config(state = tk.NORMAL)
            else:
                loginButton.config(state = tk.DISABLED)
                
            return 1
        else:
            return 0

def login():
    name = userEntry.get() #Get entry
    userEntry.delete(0, tk.END) #Clear entry
    userLabel.config(text = "{}".format(name)) #Set entry
    infoLabel.config(text = "Signed in as: ")
    userLabel.pack(pady = 5) #Place username
    logoutButton.pack() #Place logout button
    loginButton.pack_forget() #Remove loginbutton
    userEntry.pack_forget() #Remove userEntry
    playButton.config(state = tk.NORMAL)
    
def logout():
    if menuCanvas.grid_info() != {} or gameoverCanvas.grid_info() != {} or messageBox.askyesno(title = "Sign out?", message = "Signing out will end your current game.\nAre you sure you want to sign out?", icon = 'warning'):
        infoLabel.config(text = "Enter Username: ")
        userLabel.pack_forget()
        logoutButton.pack_forget()
        userEntry.pack(pady = 5)
        loginButton.pack(pady = 5)
        playButton.config(state = tk.DISABLED)
        Main.end()
            
Main = Control()

#The game canvas
canvas = tk.Canvas(width = 670, height = 400, bg = "#efefef")
canvas.bind("<Button>", checkMouse)

#The main menu with instructions and credits etc.
menuCanvas = tk.Canvas(width = 670, height = 400, bg = "#efefef")
menuCanvas.create_text(350, 50, text = "300DTS Mathematics Program", font = "Calibri, 20", fill = "black")
menuCanvas.create_text(350, 80, text = "By Hamish Clark", font = "Calibri, 12", fill = "black")
splash = """Please enter a user/nickname on the right hand side and
select a difficuilty.

-Username must be between 3 and 11 characters.
-May only contain letters.

Press "START GAME" to begin!
"""

menuCanvas.create_text(350, 180, text = splash, font = "Calibri, 12", fill = "black")

#The gameover canvas with scores etc.
gameoverCanvas = tk.Canvas(width = 670, height = 400, bg = "#efefef")
gameoverCanvas.grid_configure(row = 0, column = 0)
gameoverCanvas.grid_remove()

messageBox = tk.messagebox

#Side frame that holds the game settings and login.
frame = tk.Frame(bg = "#dddddd",
                 width = 200,
                 height = 392)
frame.pack_propagate(False)

#sub frame for login widgets
loginFrame = tk.Frame(master = frame, width = 200,  bg = frame.cget("bg"))
infoLabel = tk.Label(text = "Enter Username: ", master = loginFrame, bg = frame.cget("bg"), fg = "#555")
userLabel = tk.Label(text = "User", master = loginFrame, bg = frame.cget("bg"), font = "Calibri 20 underline")
loginButton = tk.Button(text = "Sign in", master = loginFrame, width = 10, command = login, bd = 0, bg = "#ADD633", font = "Calibri 14", state = tk.DISABLED)
logoutButton = tk.Button(text = "Sign Out", master = loginFrame, width = 10, command = logout, bd = 0, bg = "#B24C32", font = "Calibri 14")
playButton = tk.Button(text = "Start Game", master = frame, width = 15, command = Main.start, bd = 0, bg = "#ADD633", font = "Calibri 14", state = tk.DISABLED)
quitButton = tk.Button(text = "Quit", master = frame, width = 15, command = Main.quitButtonPressed, bd = 0, bg = "#B24C32", font = "Calibri 14")
showHighscoreButton = tk.Button(text = "Highscores", master = frame, width = 15, command = Main.open_highscores, bd = 0, bg = "#6699FF", font = "Calibri 14")

userEntry = tk.Entry(font = "Calibri 14",
                     master = loginFrame,
                     width = 15,
                     bd = 0,
                     insertbackground = "#6699FF",
                     validate="key",
                     vcmd = (root.register(check), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%w'))

diffSelectFrame = tk.Frame(master = frame, width = 200,  bg = frame.cget("bg"))

MODES = [
    ("Easy", "easy", "#ADD633"),
    ("Medium", "medium", "#6699FF"),
    ("Hard", "hard", "#B24C32"),
    ("Custom", "custom", "#CC33FF"),
]

diffVar = tk.StringVar()
diffVar.set("easy") # initialize

for text, mode, colour in MODES:
    b = tk.Radiobutton(diffSelectFrame,
                       text = text,
                       variable = diffVar,
                       value = mode,
                       indicatoron = 0,
                       bg = '#DDDDDD',
                       bd = 0,
                       width = 18,
                       selectcolor  = colour,
                       relief = tk.SUNKEN,
                       command = Main.set_diff)
    b.pack(anchor='w')

#Game Buttons
answerButton = tk.Button(text = "Answer",
                         bd = 0,
                         bg               = "#ADD633",
                         fg               = "#FDFDFD",
                         activeforeground = "#FDFDFD",
                         activebackground = "#8BB300",
                         width = 32,
                         font = "Calibri 18",
                         command = Main.answer)

hintButton = tk.Button(text = "Hint",
                       bd = 0,
                       width = 8,
                       bg               = "#6699FF",
                       fg               = "#FDFDFD",
                       activeforeground = "#FDFDFD",
                       activebackground = "#3366CC",
                       font = ("Calibri", 18,),
                       command = Main.hint)


resetButton = tk.Button(text = "Skip",
                        bd = 0,
                        width = 8,
                        bg               = "#B24C32",
                        fg               = "#FDFDFD",
                        activeforeground = "#FDFDFD",
                        activebackground = "#901A00",
                        font = ("Calibri", 18,),
                        command = Main.skip)

menuCanvas.grid(row = 0, column = 0, columnspan = 3, rowspan = 2, sticky = "nw")

#Placing side frame widgets
frame.grid(row = 0, column = 3, padx = 10, pady = 10)
loginFrame.pack()
infoLabel.pack()
userEntry.pack(pady = 5)
loginButton.pack(pady = 5)
diffSelectFrame.pack(pady = 30)
playButton.pack(pady = 5)
showHighscoreButton.pack(pady = 5)

#Homemade timer widget for speed bonus
timer = Timer((670- 100, 400 - 90), 63, "Speed Bonus", 120*diffs[Main.diff]["timer"])

blockList = [] #List that holds all the answer blocks

dock = Dock(300, 250, 100, 100) #Where to place the correct block

#Start the main_loop
"""
I've decided to update my own loop alongside tkinters main loop so
I can have more control over my canvas and animations.
In hindsight I probably shouldnt have but its too late now ;)
"""

Main.main_loop()





