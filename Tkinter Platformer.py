from tkinter import * #Imports all libraries necessary for the program to run
import time
import random

class Window(Frame): #Inherits from frame
    def __init__(self, Master=None):
        self.Started=False #Variable to check if the game has started
        #Frame.__init__(self, Master)
        #Frame=Frame(Root, width=1280, height=720)
        self.Master=Master
        self.InitWindow()

    def  InitWindow(self): #Initialises the window - displays the Enter button, the input area for the player's name and the text to inform the player what to enter
        Root.configure(background='light grey')
        self.Master.title("GUI")
        self.UsernameText=Label(Root, text = "Your Name:")
        self.UsernameText.place(x = 300, y = 100)
        self.UsernameText.configure(background='light grey')
        self.UsernameBox = Entry(Root)
        self.UsernameBox.place(height = 20, width = 60, x = 400, y = 100)
        self.EnterNameButton = Button(Root, text = "Enter", command = self.Enter)
        self.EnterNameButton.place(height = 30, width = 80, x = 390, y = 400)

    def Enter(self): #Runs when the Enter button is pressed
        if not self.Started: #To prevent the player from starting the game again after it has already begun
            self.Username=self.UsernameBox.get()
            self.Started=True
            self.GameLoop()

    def GameLoop(self):
        Root.configure(background='light blue') #Changes the background colour so the player knows the game has begun
        self.UsernameText.destroy()
        self.CamPos=[0, 0] #CamPos - camera position, PlayerPos - player position
        self.PlayerPos=[400,100] #PlayerVel - the players velocity horizontally and vertically
        TimeWait=time.time() #TimeWait - a variable to keep track how much time has passed since the user clicked the Enter button
        self.PlayerVel=[0,-15] #DropDownPlat and UpButton - to stop the program from crashing on first run
        self.DropDownPlat=None #Projectiles - list to store all projectiles
        self.UpButton=None
        Projectiles=[]
        Score=0
        ScoreText=Label(Root, text = "Score: "+str(Score))
        while True:
            for i in Projectiles: #Iterates through each projectile to move them, display them and check for collisions
                i.PlaceMe(self.CamPos)
                if round(i.x/60)*60 == round((self.PlayerPos[0]+30)/60)*60 and round(i.y/30)*30 == round((self.PlayerPos[1])/30)*30: #Inaccrurate but good enough check for collisions
                    if i.Checked.get()==0:
                        Root.destroy() #Ends the game if the player touches a projectile that hasn't been click on
                    else:
                        self.PlayerVel[0]=random.randint(-20,20) #If the player has clicked on it, they are launched in a random direction upwards
                        self.PlayerVel[1]+=random.randint(-30,-25)
                i.x-=i.Speed #Moves the projectile leftwards
                if i.x<-1000: #Removes the projectile if it goes off the screen
                    i.DisplayMe.destroy()
                    Projectiles.remove(i)
            if self.PlayerPos[1]>2000: #Ends the game if the player has fallen off the map
                Root.destroy()
            self.OnGround=False #Variable to check if the player is on the ground (and therefore is allowed to jump)
            self.PlayerPos[0]+=self.PlayerVel[0] #Moves the player by their velocity
            self.PlayerPos[1]+=self.PlayerVel[1]
            if self.PlayerPos[1]>380 and self.PlayerPos[1]<400 and self.PlayerPos[0]>330 and self.PlayerPos[0]<460: #Checks for collisions with platforms - slightly larger than actual to not be unfair
                self.PlayerPos[1]-=self.PlayerVel[1]
                self.PlayerVel[1]=0
                self.OnGround=True
            elif self.PlayerPos[1]>380 and self.PlayerPos[1]<400 and self.PlayerPos[0]>640 and self.PlayerPos[0]<850:
                self.PlayerPos[1]-=self.PlayerVel[1] #Moves the player out of the platform if they hit it
                self.OnGround=True
                if SelectedOption.get()=="Normal": #Acts as a normal platform when normal is selected, otherwise bounces the player
                    self.PlayerVel[1]=0
                else:
                    self.PlayerVel[1]=self.PlayerVel[1]*-1.5
            self.UsernameBox.place(height = 20, width = 60, x = self.PlayerPos[0]-self.CamPos[0], y = self.PlayerPos[1]-self.CamPos[1]) #Positions the player and platforms
            self.EnterNameButton.place(height = 30, width = 80, x = 390-self.CamPos[0], y = 400-self.CamPos[1])
            if not self.DropDownPlat==None: #Check to see if this type of platform has spawned yet
                self.DropDownPlat.place(height = 30, width = 160, x = 690-self.CamPos[0], y = 400-self.CamPos[1])
            self.CamPos[0]+=(-625+self.PlayerPos[0]-self.CamPos[0])/10 #Moves the camera towards the player's position
            self.CamPos[1]+=(-370+self.PlayerPos[1]-self.CamPos[1])/10
            if not self.OnGround:
                self.PlayerVel[1]+=1 #Increases the player's downwards velocity to simulate gravity if they are not on a platform
            if self.PlayerVel[1]>13: #Creates a max falling speed to prevent falling through platforms or going too fast
                self.PlayerVel[1]=13
            self.PlayerVel[0]=self.PlayerVel[0]*0.9 #Friction so the player can stop travelling
            time.sleep(0.016) #0.016 = 16ms = 60 frames per second
            Root.update() #Stops the program from not responding and refreshes button inputs
            if time.time()>TimeWait+2 and self.UpButton==None: #After 2 seconds the player gets movement controls
                self.UpButton = Button(Root, text = "↑", command = self.Up)
                self.UpButton.place(height = 30, width = 30, x = 640, y = 600)
                self.RightButton = Button(Root, text = "→", command = self.Right)
                self.RightButton.place(height = 30, width = 30, x = 690, y = 650)
                self.LeftButton = Button(Root, text = "←", command = self.Left)
                self.LeftButton.place(height = 30, width = 30, x = 590, y = 650)
            elif time.time()>TimeWait+0.6 and self.DropDownPlat==None: #After 0.6 sec the second platform spawns
                Options=["Normal","Bouncy"]
                SelectedOption = StringVar(Root)
                SelectedOption.set(Options[0]) # default value
                self.DropDownPlat = OptionMenu(Root, SelectedOption, *Options)
                self.DropDownPlat.configure(background='light grey')
            elif time.time()>TimeWait+2.2 and random.randint(0,20-(time.time()-TimeWait)//10)==0: #After 2.2 seconds projectiles begin to spawn
                    Projectiles.append(Projectile(self.PlayerPos))
                    Score+=1
                    ScoreText.destroy()
                    ScoreText=Label(Root, text = "Score: "+str(Score))
                    ScoreText.place(x=0,y=0)


    def Up(self): #Methods for player movement, called when the associated button is clicked
        if self.OnGround: #Checks whether the player is on the ground
            self.PlayerVel[1]=-25
    def Left(self):
        self.PlayerVel[0]=-13
    def Right(self):
        self.PlayerVel[0]=13
        

class Projectile: #Class for a projectile
    def __init__(self, PlayerPos):
        self.x=2000 #Sets the projectile's x position to be off the screen
        if random.randint(0,4)==0: #One in 4 projectiles spawn at the players position to force them to move and jump
            self.y=PlayerPos[1]
        else:
            self.y=random.randint(0,1440) #Otherwise the position is randomised
        self.Speed=random.randint(2,7)
        self.Checked=IntVar(Root)
        self.DisplayMe = Checkbutton(Root, variable = self.Checked)
        self.DisplayMe.configure(background='light blue')

    def PlaceMe(self, CamPos): #Tiny method to place the projectile on the screen, could probably be moved to GameLoop
        self.DisplayMe.place(x = self.x-CamPos[0], y = self.y-CamPos[1])

Root = Tk()
Root.geometry("1280x720") #Default window resolution is 1280 by 720
app=Window(Root) #Creates the window
Root.mainloop() #Stops the program from instantly closing - stays here until the Enter button is pressed, then goes to GameLoop
