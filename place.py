from tkinter import *
from client import client
import _thread
import time
import math

class canvas:

    def changeColor(self, color):
        self.currentColor = color

    def new_pixel(self, event):
        if 'ok' in cli.send_request({'method':'put_pixel', 'token':self.token, 'xy':(event.x//self.x_span, event.y//self.y_span), 'color':self.currentColor}):
            self.action = time.time()


    def update(self, xy, img):
        for y in range(xy[1]):
            for x in range(xy[0]):
                self.gameboard.itemconfig(self.painting[x][y], fill = self.color[img[x][y]])


    def how_much_time(self):
        while True:
            self.cooldown.config(text = 'Cooldown : ' + str(max(0, math.ceil(-time.time() + self.action + self.delay))) +
            ' ' * (-len(str(max(0, math.ceil(-time.time() + self.action + self.delay)))) + len(str(self.delay))))

    def motion(self, event):
        mouse_x, mouse_y = event.x, event.y
        self.pos.config(text = 'x : ' + str(mouse_x//self.x_span) + ', y : ' + str(mouse_y//self.y_span))

    def init(self, xy, color, img, token, delay):
        self.token = token
        self.color = color
        self.currentColor = "0"
        self.delay = delay

        self.root = Tk()
        self.root.title("py/place")
        self.x_span = int(600/xy[0])
        self.y_span = int(600/xy[1])
        self.root.geometry('760x610')

        self.painting = [['' for i in range(xy[0])] for i in range(xy[1])]
        self.gameboard = Canvas(self.root, width = 600, height = 600)
        for y in range(xy[1]):
            for x in range(xy[0]):
                self.painting[y][x] = self.gameboard.create_rectangle(x*self.x_span, y*self.y_span, (x+1)*self.x_span, (y+1)*self.y_span, fill=color[img[y][x]])

        self.gameboard.bind('<Button-1>', self.new_pixel)
        self.gameboard.bind('<Motion>', self.motion)

        self.ui = Frame(self.root, width = 160, height = 600)
        self.ui.grid_propagate(False)

        self.cooldown = Label(self.ui, text='Cooldown : ' + str(self.delay))
        self.pos = Label(self.ui, text = '')
        self.action = time.time()
        self.cooldown.grid(row = 0, column = 1, columnspan = 10)
        self.pos.grid(row = 1, column = 1, columnspan = 10)
        i, j, amount = 0, 2, 7
        self.need = Label(self.ui, text = '')
        self.colors = []
        for colors in self.color:
            self.colors.append(Canvas(self.ui, width = 20, height = 20, bd = 0, bg = color[colors], highlightthickness = 0))
            self.colors[-1].bind('<Button-1>',
                        lambda event, arg = colors:
                            self.changeColor(arg))
            self.colors[-1].grid(row = j, column = i)
            i += 1
            if i > amount:
                i = 0
                j += 1
        _thread.start_new_thread(self.how_much_time, ())

        self.gameboard.pack(side = 'left')
        self.ui.pack(side = 'right', anchor = 'e')

        self.root.mainloop()




class place:
    screen = Tk()
    IP = None
    port = None
    token = None
    color = {}
    img = []
    win = canvas()


    def quit(self):
        self.adress = (self.IP.get(), self.port.get())
        self.screen.destroy()


    def refresh(self, publ):
        if 'img' in publ:
            self.win.update(xy=self.xy, img=publ['img'])



    def play(self, response : str) -> bool:
        """Takes the $response$ from the server and decides wether to wait for an event or to play next.
        """



        if 'Token' in response:
            self.token = response['Token']
            self.xy = response['xy']
            self.color = response['color']
            self.img = response['img']
            self.delay = response['delay']
            self.win.init(self.xy, self.color, self.img, self.token, self.delay)
            return False




    def __init__(self):
        """Initializes the game
        """


        # entrée
        IPadress = StringVar()
        IPadress.set("100.115.99.13")
        self.IP = Entry(self.screen, textvariable=IPadress, width=30)
        self.IP.pack()

        # entrée
        value = StringVar()
        value.set("5555")
        self.port = Entry(self.screen, textvariable=value, width=30)
        self.port.pack()

        connect = Button(self.screen, text = 'Chercher ce serveur', command = self.quit)
        connect.pack()

        self.screen.geometry('200x50')

        self.screen.mainloop()



def sub():
    while True:
        game.refresh(cli.wait_for_event())

game = place()
cli = client((game.adress))

_thread.start_new_thread(sub, ())

game.play(cli.send_request({'method' : 'init'}))
cli.send_request({'method' : 'disconnect', 'token' : game.token})
