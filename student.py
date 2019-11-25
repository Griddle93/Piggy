from teacher import PiggyParent
import sys
import time


class Piggy(PiggyParent):
    '''
    *************
    SYSTEM SETUP
    *************
    '''
    
    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self)
        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings  
        '''
        self.LEFT_DEFAULT = 80
        self.RIGHT_DEFAULT = 80
        """This is just the way your robot will look when activated. normally between 1000-2000"""
        self.MIDPOINT = 1500 
        self.load_defaults()
        
        
    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)  # Power motor is given and outputed
        self.set_servo(self.SERVO_1, self.MIDPOINT) 
        
    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        """Dictoinary for all terms displayed"""
        
        print("\n *** MENU ***")  # Simply prints menu
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit)
                }
        """ loop and print the menu..."""
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        """ store the user's answer"""
        ans = str.lower(input("Your selection: "))
        """ activate the item selected"""
        menu.get(ans, [None, self.quit])[1]()


    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''

    def dance(self):
        """check to see it's safe"""
        if not self.safe_to_dance():
            print("No can do cheif")
            return   """Will not dance when something is obstructing"""
        else:
            print("It's safe to dance!")
        self.yeet_around() #"""1st dance"""
        self.dothecircle() #"""2nd dance"""
        self.Stopandgo() #"""3rd dance"""
        self.yeet_yeet() #"""calls waive method/dance"""
        self.Dabyeet() 
        self.Repeatdance()

    def safe_to_dance(self):
        """ Does a 360 distance check and returns true if safe to dance"""
        for x in range(4):
            for ang in range(self.MIDPOINT-400, self.MIDPOINT+400, 100): 
                self.servo(ang)
                time.sleep(.1)
                if self.read_distance() < 250:
                    return False  # """The robot has found something"""
            self.turn_by_deg(90)
        return True  # """The robot did not find anything"""


    def yeet_dab(self):
        """A nice yeet dab to get it started"""
        self.right()
        time.sleep(2)
        self.stop()
        self.left()
        time.sleep(.25)
        self.stop()
        self.right()
        time.sleep(.25)
        self.stop()
        self.fwd()
        time.sleep(2)
        self.stop()
        self.servo(1200)
        time.sleep(1)
        self.servo(1700)
        time.sleep(1)

    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 250):  #These codes allow robot to scan and sweep area before dancing"""
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        found_something = False #When the robot finds or sees something
        trigger_distance = 350 #The distance it scans around
        count = 0
        starting_position = self.get_heading() #starting position is placed with robot
        self.right(primary=60, counter=-60)
        while self.get_heading() != starting_position:  #With robot
            if self.read_distance() < trigger_distance and not found_something:  #If nothing is found then it proceeds
                found_something = True  #Means something is found
                count += 1
            elif self.read_distance() > trigger_distance and found_something:
                found_something = False #Means nothing is found
                print("my vision is clear and ready to roll")
        self.stop()
        print("I found this many things: %d" % count)
        return count

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")
        while True:
            self.servo(self.MIDPOINT)  #set servo forward and straight
            while self.read_distance() > 350:  
                self.fwd()
                time.sleep(.01)
            self.stop()
            self.scan()            
            #traversal
            left_total = 0
            left_count = 0
            right_total = 0
            right_count = 0
            for ang, dist in self.scan_data.items():
                if ang < self.MIDPOINT: 
                    right_total += dist
                    right_count += 1
                else:
                    left_total += dist
                    left_count += 1
            left_avg = left_total / left_count
            right_avg = right_total / right_count
            if left_avg > right_avg:
                self.turn_by_deg(-100)
            else:
                self.turn_by_deg(100) 

    def yeet_around(self):
        #Goes around an object if present
        if self.read_distance() < 350:
            self.servo(1000)
            time.sleep(.4)
            self.servo(2000)
            time.sleep(.4)
        self.servo(1500)

    def dothecircle(self):
        """Does 2 circles repetitivley"""
        self.right()
        time.sleep(5)
        self.stop()
    
    def Stopandgo(self):
        """The robot stops abruptly after dancing"""
        self.fwd()
        time.sleep(.1)
        self.back()
        time.sleep(.5)
        self.stop()
        
    def yeet_yeet(self):
        """rapidly yeets around"""
        for x in range(3):
            self.servo(1000)
            time.sleep(.2)
            self.servo(2000)
            time.sleep(.2)
            self.servo(1000)
            time.sleep(.2)
            self.servo(2000)
            time.sleep(.2)
            self.servo(1000)
            time.sleep(.2)
            self.servo(2000)
            time.sleep(.2)
            self.servo(1000)
            time.sleep(.2)
            self.servo(2000)
            time.sleep(.2)
            self.stop()
            
    def Dabyeet(self):
        """dab dance inspired by Treppo's robot"""
        for x in range(7):
            self.right()
            time.sleep(.5)
            self.servo(2000)
            self.stop()
            self.back()
            time.sleep(.5)        #7 full "dabs"
            self.stop()
            self.left()
            time.sleep(.5)
            self.servo(1000)
            self.stop()
            self.back()
            time.sleep(.5)
            self.stop()
            
    def Repeatdance(self):
        """Very repetitive dance that is simple but relatively long"""
        self.fwd()
        time.sleep(.5)
        self.turn_by_deg(90)
        self.fwd()
        time.sleep(.5)
        self.turn_by_deg(90)
        self.fwd()
        time.sleep(.5)
        self.turn_by_deg(90)
        self.fwd()
        time.sleep(.5)
        self.turn_by_deg(90)
        
###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file
    
    p = Piggy()
    
    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()
        
    try:
        while True:  # app loop
            p.menu()
            
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
















