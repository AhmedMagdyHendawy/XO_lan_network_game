#!/usr/bin/env python2
from Tkinter import*
from PIL import Image, ImageTk
import socket
import sys
import threading
from functools import partial
import time


class Master(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.frame_width = 300
        self.frame_height = 400
        icon = ImageTk.PhotoImage(file='xo.ico')   
        self.tk.call('wm', 'iconphoto', self._w, icon)
        self.resizable(False, False)
        self.Start=False
        self.Wait=False
        self.opp=False
        self.opp_turn=False
        self.win=False
        self.possiblityX=[0,0,0,0,0,0,0,0]
        self.possiblityO=[0,0,0,0,0,0,0,0]
        self.finish=False
        self.geometry(str(self.frame_width)+"x"+str(self.frame_height))
        self.attributes('-fullscreen',False)
        self.title("X~O")
        self.container = Canvas(self, bg = "black", highlightbackground="black", highlightcolor="black")
        self.container.pack(side = TOP, expand = True, fill = BOTH)
        
        self.Option_x=Button(self.container, command=partial(self.actor_choice,"x"),text="X",
                           height=30,width=30)
        self.container.create_window(40, 330,state="normal", window=self.Option_x,height=30, width=30)

        self.Option_o=Button(self.container, command=partial(self.actor_choice,"o"),text="O",
                           height=30,width=30)
        self.container.create_window(260, 330,state="normal", window=self.Option_o,height=30, width=30)

        self.Option_start=Button(self.container, command=self.start,text="Start",
                           height=30,width=70)
        self.container.create_window(100, 330,state="normal", window=self.Option_start,height=30, width=70)

        self.Option_wait=Button(self.container, command=self.wait,text="Wait",
                           height=30,width=70)
        self.container.create_window(200, 330,state="normal", window=self.Option_wait,height=30, width=70)

        self.text = self.container.create_text(150, 370, text="Welcome"
                                                                  , font=('SWTxt', 12, 'bold'),
                                                                    fill='#00ff00')
        self.container.itemconfig(self.text, state='normal')

        self.x = Image.open('x.png')
        self.x= self.x.resize((100, 100), Image.ANTIALIAS)
        self.x = ImageTk.PhotoImage(self.x)
        self.o = Image.open('o.png')
        self.o= self.o.resize((100, 100), Image.ANTIALIAS)
        self.o = ImageTk.PhotoImage(self.o)
        self.actor=""
        self.cells=[[0,0,0],[0,0,0],[0,0,0]]
        for i in range(3):
            for j in range(3):
                self.cells[i][j] = {"Button":Button(self.container, command=partial(self.action,i,j),
                           height=100,width=100, bg="black", activebackground="black"),
                           "Status": "e"}
                self.container.create_window(i*100+50, j*100+50,state="normal", window=self.cells[i][j]["Button"],height=100, width=100)
        self.bind("<Escape>",self.exit_fullscreen)
        self.PC_thread = threading.Thread(target=self.connectToOpponent)
        self.PC_thread.daemon = True
        self.PC_thread.start()
        


    def exit_fullscreen(self,event=None):
        self.attributes('-fullscreen',False)
        self.geometry(str(self.frame_width)+"x"+str(self.frame_height))

    def actor_choice(self,choice):
        if (self.actor==""):
            self.actor=choice
            if not (self.opp):
                self.PC_socket.send(self.actor+",")
                self.container.itemconfig(self.text, state='hidden')
                self.text = self.container.create_text(150, 370, text="Your Turn"
                                                                  , font=('SWTxt', 12, 'bold'),
                                                                    fill='#00ff00')
                self.container.itemconfig(self.text, state='normal')
            else:
                self.opp=False
            print(self.actor+",")
        else:
            print("You already chose")

    def connectToOpponent(self):
        TCP_IP="192.168.1.7"
        # this IP of my pc. When I want raspberry pi 2`s as a client, I replace it with its IP '169.254.54.195'
        TCP_PORT = 5000
        BUFFER_SIZE = 512
        while(True):
            if (self.Start):
                while True:
                    try:
                        self.PC_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        self.PC_socket.connect((TCP_IP, TCP_PORT))
                        self.container.itemconfig(self.text, state='hidden')
                        self.text = self.container.create_text(150, 370, text="Connected"
                                                                  , font=('SWTxt', 12, 'bold'),
                                                                    fill='#00ff00')
                        self.container.itemconfig(self.text, state='normal')
                        while True:
                            self.PC_socket.send(",")
                            if not(self.actor == ""):
                                while True:

                                    self.Opp_data =self.PC_socket.recv(BUFFER_SIZE)
 
                                    self.Opp_data =(self.Opp_data).split(",")
                                    if not (self.finish):
                                        if not (self.Opp_data[0]==""):
                                            self.opp=True
                                            self.cells[int(self.Opp_data[0])][int(self.Opp_data[1])]["Button"].invoke()

                            else:
                                self.Opp_data =self.PC_socket.recv(BUFFER_SIZE)
                                self.Opp_data =(self.Opp_data).split(",")
       
                                if (self.Opp_data[0]=="x"):
                                    self.opp=True
                                    self.opp_turn=True
                                    self.container.itemconfig(self.text, state='hidden')
                                    self.text = self.container.create_text(150, 370, text="Opponent Turn"
                                                                  , font=('SWTxt', 12, 'bold'),
                                                                    fill='#00ff00')
                                    self.container.itemconfig(self.text, state='normal')
                                    self.Option_o.invoke()
                                elif (self.Opp_data[0]=="o"):
                                    self.opp=True
                                    self.opp_turn=True
                                    self.container.itemconfig(self.text, state='hidden')
                                    self.text = self.container.create_text(150, 370, text="Opponent Turn"
                                                                  , font=('SWTxt', 12, 'bold'),
                                                                    fill='#00ff00')
                                    self.container.itemconfig(self.text, state='normal')
                                    self.Option_x.invoke()
                    except:
                        print("Retrying Connection to Opponent")
                        self.PC_socket.close()

            elif (self.Wait):
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.bind((TCP_IP, TCP_PORT))
                s.listen(1)
                while True :
                    try:    
                        self.PC_socket, addr = s.accept()
                        self.container.itemconfig(self.text, state='hidden')
                        self.text = self.container.create_text(150, 370, text="Connected"
                                                                  , font=('SWTxt', 12, 'bold'),
                                                                    fill='#00ff00')
                        self.container.itemconfig(self.text, state='normal')
                        while True:
                            self.PC_socket.send(",")
                            if not(self.actor == ""):
                                while True:   
                                    self.Opp_data =self.PC_socket.recv(BUFFER_SIZE)

                                    self.Opp_data =(self.Opp_data).split(",")
                                    if not (self.finish):
                                        if not (self.Opp_data[0]==""):
                                            self.opp=True
                                            self.cells[int(self.Opp_data[0])][int(self.Opp_data[1])]["Button"].invoke()
                            else:
                                self.Opp_data =self.PC_socket.recv(BUFFER_SIZE)
                                self.Opp_data =(self.Opp_data).split(",")
                
                                if (self.Opp_data[0]=="x"):
                                    self.opp=True
                                    self.opp_turn=True
                                    self.container.itemconfig(self.text, state='hidden')
                                    self.text = self.container.create_text(150, 370, text="Opponent Turn"
                                                                  , font=('SWTxt', 12, 'bold'),
                                                                    fill='#00ff00')
                                    self.container.itemconfig(self.text, state='normal')
                                    self.Option_o.invoke()
                                elif (self.Opp_data[0]=="o"):
                                    self.opp=True
                                    self.opp_turn=True
                                    self.container.itemconfig(self.text, state='hidden')
                                    self.text = self.container.create_text(150, 370, text="Opponent Turn"
                                                                  , font=('SWTxt', 12, 'bold'),
                                                                    fill='#00ff00')
                                    self.container.itemconfig(self.text, state='normal')
                                    self.Option_x.invoke()     
                    except:	
                        print("Closing socket")
                        self.PC_socket.close()


                
    def start(self):
        self.Start=True
        

    def wait(self):
        self.Wait=True
        

    def action(self,i,j):
        if (self.cells[i][j]["Button"]["image"]=="pyimage1" or self.cells[i][j]["Button"]["image"]=="pyimage2"):
            print("Invalid move")
        else:
            if not (self.finish):
                if(self.opp):
                    if(self.actor=="x"):
                        self.cells[i][j]["Button"].configure(image=self.o)
                        self.cells[i][j]["Status"]="o"
                    elif (self.actor=="o"):
                        self.cells[i][j]["Button"].configure(image=self.x)
                        self.cells[i][j]["Status"]="x"
                    self.result(i,j,self.opp)
                    
                    self.opp=False
                    self.opp_turn=False
                    if not(self.finish):
                        self.container.itemconfig(self.text, state='hidden')
                        self.text = self.container.create_text(150, 370, text="Your Turn"
                                                                        , font=('SWTxt', 12, 'bold'),
                                                                            fill='#00ff00')
                        self.container.itemconfig(self.text, state='normal')
                else:
                    if(self.opp_turn):
                        pass
                    else:
                        if(self.actor=="x"):
                            self.cells[i][j]["Button"].configure(image=self.x)
                            self.cells[i][j]["Status"]="x"
                        elif (self.actor=="o"):
                            self.cells[i][j]["Button"].configure(image=self.o)
                            self.cells[i][j]["Status"]="o"
                        self.data=[i,j]
                        self.data_str=",".join(map(str,self.data))
                        self.PC_socket.send(self.data_str)
                        self.result(i,j,self.opp)
                        self.opp_turn=True
                        if not(self.finish):
                            self.container.itemconfig(self.text, state='hidden')
                            self.text = self.container.create_text(150, 370, text="Opponent Turn"
                                                                            , font=('SWTxt', 12, 'bold'),
                                                                                fill='#00ff00')
                            self.container.itemconfig(self.text, state='normal')
            
    
    def result(self,i,j,opp):
        if (i==0 and j==0) or (i==1 and j==1) or (i==2 and j==2):
            if(self.cells[i][j]["Status"]=="x"):
                self.possiblityX[0]+=1
            elif (self.cells[i][j]["Status"]=="o"):
                self.possiblityO[0]+=1
            if (self.possiblityX[0]==3) or (self.possiblityO[0]==3):
                if (opp):
                    self.win=False
                else:
                    self.win=True
                self.finish=True
        if (i==0 and j==0) or (i==0 and j==1) or (i==0 and j==2):
            if(self.cells[i][j]["Status"]=="x"):
                self.possiblityX[1]+=1
            elif (self.cells[i][j]["Status"]=="o"):
                self.possiblityO[1]+=1
            if (self.possiblityX[1]==3) or (self.possiblityO[1]==3):
                if (opp):
                    self.win=False
                else:
                    self.win=True
                self.finish=True
        if (i==0 and j==0) or (i==1 and j==0) or (i==2 and j==0):
            if(self.cells[i][j]["Status"]=="x"):
                self.possiblityX[2]+=1
            elif (self.cells[i][j]["Status"]=="o"):
                self.possiblityO[2]+=1
            if (self.possiblityX[2]==3) or (self.possiblityO[2]==3):
                if (opp):
                    self.win=False
                else:
                    self.win=True
                self.finish=True
        if (i==1 and j==0) or (i==1 and j==1) or (i==1 and j==2):
            if(self.cells[i][j]["Status"]=="x"):
                self.possiblityX[3]+=1
            elif (self.cells[i][j]["Status"]=="o"):
                self.possiblityO[3]+=1
            if (self.possiblityX[3]==3) or (self.possiblityO[3]==3):
                if (opp):
                    self.win=False
                else:
                    self.win=True
                self.finish=True
        if (i==0 and j==1) or (i==1 and j==1) or (i==2 and j==1):
            if(self.cells[i][j]["Status"]=="x"):
                self.possiblityX[4]+=1
            elif (self.cells[i][j]["Status"]=="o"):
                self.possiblityO[4]+=1
            if (self.possiblityX[4]==3) or (self.possiblityO[4]==3):
                if (opp):
                    self.win=False
                else:
                    self.win=True
                self.finish=True
        if (i==2 and j==0) or (i==2 and j==1) or (i==2 and j==2):
            if(self.cells[i][j]["Status"]=="x"):
                self.possiblityX[5]+=1
            elif (self.cells[i][j]["Status"]=="o"):
                self.possiblityO[5]+=1
            if (self.possiblityX[5]==3) or (self.possiblityO[5]==3):
                if (opp):
                    self.win=False
                else:
                    self.win=True
                self.finish=True
        if (i==0 and j==2) or (i==1 and j==2) or (i==2 and j==2):
            if(self.cells[i][j]["Status"]=="x"):
                self.possiblityX[6]+=1
            elif (self.cells[i][j]["Status"]=="o"):
                self.possiblityO[6]+=1
            if (self.possiblityX[6]==3) or (self.possiblityO[6]==3):
                if (opp):
                    self.win=False
                else:
                    self.win=True
                self.finish=True
        if (i==2 and j==0) or (i==1 and j==1) or (i==0 and j==2):
            if(self.cells[i][j]["Status"]=="x"):
                self.possiblityX[7]+=1
            elif (self.cells[i][j]["Status"]=="o"):
                self.possiblityO[7]+=1
            if (self.possiblityX[7]==3) or (self.possiblityO[7]==3):
                if (opp):
                    self.win=False
                else:
                    self.win=True
                self.finish=True
        print(self.win,self.possiblityO,self.possiblityX)
        if(self.finish):
            if (self.win):
                self.container.itemconfig(self.text, state='hidden')
                self.text = self.container.create_text(150, 370, text="You Won"
                                                , font=('SWTxt', 12, 'bold'),
                                                fill='#00ff00')
                self.container.itemconfig(self.text, state='normal')
            else:
                self.container.itemconfig(self.text, state='hidden')
                self.text = self.container.create_text(150, 370, text="You Lost"
                                                , font=('SWTxt', 12, 'bold'),
                                                fill='#00ff00')
                self.container.itemconfig(self.text, state='normal')


app = Master()
app.mainloop()
