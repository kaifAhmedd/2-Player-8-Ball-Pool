import phylib;
# we added this to delete files! needed for the first method of Database class
import os;
#we import sqlite3 for A3
import sqlite3;

import math;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

# this has been added for A3
FRAME_RATE = 0.01;

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;
    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" %(self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]);

################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number and position (x,y), vel and acc as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0);
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;
    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" %(self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])

################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__(self, pos):
        """
        Constructor function. Requires pos as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0);
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;
    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" %(self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS);

################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__(self, y):
        """
        Constructor function. Requires y position as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y);
      
        # this converts the phylib_object into a HCusion class
        self.__class__ = HCushion;
    def svg(self):
        if self.obj.hcushion.y == 0:
            y = -25;
        else:
            y = 2700;
        
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" %(y);

################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__(self, x):
        """
        Constructor function. Requires pos x value as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0);
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion;
    def svg(self):
        if self.obj.vcushion.x == 0:
            x = -25;
        else:
            x = 1350;
        
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" %(x);



################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        stringConcatenation = HEADER;
        for item in self:
            if(item != None):
                stringConcatenation+=item.svg();
        stringConcatenation+=FOOTER;
        return stringConcatenation;
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;

            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                      Coordinate( ball.obj.still_ball.pos.x,
                                                  ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        
        # return table
        return new;
    
    # def cueBall(self, gameName, playerName, table, xvel, yvel):
    def cueBall(self):
        cueBall = None
        i=0;
        for i in self:
            if isinstance(i, StillBall) and i.obj.still_ball.number == 0:
                cueBall = i;
                return cueBall;
        return None
        

#this is the database class for A3
class Database:
    conn: sqlite3.Connection
    #this is the first method for the Database class!
    def __init__( self, reset=False):
        if reset == True:
            if os.path.exists('phylib.db'):
                os.remove('phylib.db')
        #create a database and connect to it
        self.conn = sqlite3.connect('phylib.db')
    
    # this is the second method of the Database class for A3. This creates the tables!
    def createDB( self ):
        cursor = self.conn.cursor()
        
        #creating the first table
        cursor.execute( """ CREATE TABLE IF NOT EXISTS Ball
                            ( BALLID   INTEGER NOT NULL,
                              BALLNO   INTEGER NOT NULL,
                              XPOS     FLOAT NOT NULL,
                              YPOS     FLOAT NOT NULL,
                              XVEL     FLOAT,
                              YVEL     FLOAT,
                              PRIMARY KEY (BALLID AUTOINCREMENT) );""")
        
        # creating the second table
        cursor.execute( """ CREATE TABLE IF NOT EXISTS TTable
                            ( TABLEID      INTEGER NOT NULL,
                              TIME         FLOAT NOT NULL,
                              PRIMARY KEY(TABLEID AUTOINCREMENT) );""")

        #creating the third table
        cursor.execute( """ CREATE TABLE IF NOT EXISTS BallTable
                            ( BALLID    INTEGER NOT NULL,
                              TABLEID   INTEGER NOT NULL,
                              FOREIGN KEY(BALLID) REFERENCES Ball,
                              FOREIGN KEY(TABLEID) REFERENCES TTable);""")
        
        #creating the fourth table
        cursor.execute( """ CREATE TABLE IF NOT EXISTS Shot
                            ( SHOTID    INTEGER NOT NULL,
                              PLAYERID  INTEGER NOT NULL,
                              GAMEID    INTEGER NOT NULL,
                              PRIMARY KEY(SHOTID AUTOINCREMENT),
                              FOREIGN KEY(PLAYERID) REFERENCES Player,
                              FOREIGN KEY(GAMEID) REFERENCES Game);""")
        
        #creating the fifth table
        cursor.execute( """ CREATE TABLE IF NOT EXISTS TableShot
                            (TABLEID    INTEGER NOT NULL,
                             SHOTID     INTEGER NOT NULL,
                             FOREIGN KEY(TABLEID) REFERENCES TTable,
                             FOREIGN KEY(SHOTID) REFERENCES Shot);""")
        
        #creating the sixth table
        cursor.execute( """ CREATE TABLE IF NOT EXISTS Game
                            (GAMEID     INTEGER NOT NULL,
                             GAMENAME   VARCHAR(64) NOT NULL,
                             PRIMARY KEY(GAMEID AUTOINCREMENT) );""")
        
        #creating the seventh and last table
        cursor.execute( """ CREATE TABLE IF NOT EXISTS Player
                            (PLAYERID   INTEGER NOT NULL,
                             GAMEID     INTEGER NOT NULL,
                             PLAYERNAME     VARCHAR(64) NOT NULL,
                             PRIMARY KEY(PLAYERID AUTOINCREMENT),
                             FOREIGN KEY(GAMEID) REFERENCES Game);""")
        
        cursor.close();
        self.conn.commit();
    
    def readTable( self, tableID ):
        cursor = self.conn.cursor()
        #not sure if your supposed to add this?
        table = Table()
        #this allows us to check is the tableID exists
        cursor.execute("SELECT COUNT(*) FROM BallTable WHERE TABLEID = ?", (tableID+1, ))
        IDresult = cursor.fetchone()[0]
        #if idresult is 0 then we close the cursor and return 0
        if IDresult == 0:
            cursor.close();
            return None;
        #this allows us to get the tables time attribute from TTable
        cursor.execute("SELECT TIME FROM TTable WHERE TABLEID = ?",(tableID+1, ))
        timeResult = cursor.fetchone()[0]
        table.time = timeResult
        # This allows us to retreiev all the balls attributes from the Ball table
        cursor.execute("""SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL FROM Ball JOIN BallTable ON Ball.BALLID = BallTable.BALLID WHERE BallTable.TABLEID = ?""", (tableID+1,))
        data = cursor.fetchall()
        
        #add the if else statements here. to instantiate objects as astill or rolling ball depending on if they have velocities or not
        i = 0;
        # data is an array of rows of the table so we check each row.
        for i in data:
            if (i[4] == None and i[5] == None) or (i[4] == 0.0 and i[5] == 0.0):
                ballNum = i[1]
                ballPos = Coordinate(i[2],i[3])
                SBall = StillBall(ballNum, ballPos)
                table+=SBall
                
            else:
                ballNum = i[1]
                ballPos = Coordinate(i[2],i[3])
                ballVel = Coordinate(i[4], i[5])
                ballAcc = Coordinate(0.0,0.0);
                speed = phylib.phylib_length(ballVel);
                if(speed > VEL_EPSILON):
                    ballAcc.x = -ballVel.x/speed * DRAG;
                    ballAcc.y = -ballVel.y/speed * DRAG;
                RBall =  RollingBall(ballNum,ballPos,ballVel,ballAcc)
                table+=RBall
        
        
        
        cursor.close();
        self.conn.commit();
        return table;
    
    def writeTable( self, table ):
        cursor = self.conn.cursor();
        
        #inserts tabletime from database
        cursor.execute("""INSERT
                          INTO  TTable  (TIME)
                          VALUES        (?)""",(table.time, ))
        #gets tableID from table
        tableID = cursor.lastrowid;
        
        #inserts ball values into database depending on weather its a rolling or sitll ball.
        i=0
        for i in table:
            if isinstance(i, StillBall):
                cursor.execute("""INSERT
                                  INTO  Ball    ( BALLNO, XPOS, YPOS    )
                                  VALUES        (?,?,?)""", (i.obj.still_ball.number, i.obj.still_ball.pos.x, i.obj.still_ball.pos.y, ))
            elif isinstance(i, RollingBall):
                cursor.execute("""INSERT
                                  INTO  Ball    ( BALLNO, XPOS, YPOS, XVEL, YVEL    )
                                  VALUES        (?,?,?,?,?)""", (i.obj.rolling_ball.number , i.obj.rolling_ball.pos.x, i.obj.rolling_ball.pos.y, i.obj.rolling_ball.vel.x, i.obj.rolling_ball.vel.y, ))
            else:
                continue
        
            ballID = cursor.lastrowid;
            #inserts the ballid and tableid we retrived into the BallTable table
            cursor.execute("""INSERT
                          INTO  BallTable   (BALLID, TABLEID    )
                          VALUES            (?,?)""", (ballID, tableID, ))
        
        cursor.close();
        self.conn.commit();
        tableID = tableID - 1;
        return tableID
    
    def close( self ):
        self.conn.commit();
        self.conn.close();
    
    def getGame (self, gameID):
         cursor = self.conn.cursor();
         gameID = gameID +1;
         cursor.execute("""SELECT Game.GAMENAME, Player.PLAYERNAME FROM Game JOIN Player ON Game.GAMEID = Player.GAMEID WHERE Game.GAMEID = ?""", (gameID,))
         data = cursor.fetchall()
         cursor.close();
         self.conn.commit();
         return data;
     
    def setGame(self, gameName, player1Name, player2Name):
        cursor = self.conn.cursor();
        cursor.execute("""INSERT
                          INTO  Game        (GAMENAME    )
                          VALUES            (?)""", (gameName, ))
        gameID = cursor.lastrowid;
        cursor.execute("""INSERT
                          INTO  Player      (GAMEID,PLAYERNAME    )
                          VALUES            (?,?)""", (gameID, player1Name, ))
        cursor.execute("""INSERT
                          INTO  Player      (GAMEID,PLAYERNAME    )
                          VALUES            (?,?)""", (gameID,player2Name, ))
        
        cursor.close();
        self.conn.commit();
        return gameID-1
    
    def newShot(self, gameName, playerName):
        cursor = self.conn.cursor();
        cursor.execute("SELECT GAMEID FROM Game WHERE GAMENAME = ?", (gameName, ))
        gameID = cursor.fetchone()[0];
        
        cursor.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?", (playerName, ))
        playerID = cursor.fetchone()[0];
        
        cursor.execute("""INSERT
                          INTO  Shot        (PLAYERID,GAMEID    )
                          VALUES            (?,?)""", (playerID,gameID, ))
        
        shotID = cursor.lastrowid;
        cursor.close();
        self.conn.commit();
        return shotID;
        
    def tableShotInsert(self, shotID, tableID):
        cursor = self.conn.cursor();
        cursor.execute("""INSERT
                          INTO  TableShot  (TABLEID, SHOTID)
                          VALUES        (?,?)""",(tableID, shotID))
        cursor.close();
        self.conn.commit();
        
        
        
        
         
         
         
    
#this is the game class
class Game:
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):
        Database().createDB()
        if gameID!=None and gameName==None and player1Name==None and player2Name==None:
            data = Database().getGame(gameID)
            self.gameID = gameID
            self.gameName = data[0][0]
            self.player1Name = data[0][1]
            self.player2Name = data[1][1]    
        elif gameID == None and gameName != None and player1Name!= None and player2Name!= None:
            gameID = Database().setGame(gameName, player1Name, player2Name)
            self.gameID = gameID
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
        else:
            raise TypeError("values are not valid!")
    
    def shoot( self, gameName, playerName, table, xvel, yvel ):
        shotID = Database().newShot(gameName, playerName);
        cueBall = table.cueBall()
        xpos = cueBall.obj.still_ball.pos.x
        ypos = cueBall.obj.still_ball.pos.y
        cueBall.type = phylib.PHYLIB_ROLLING_BALL
        cueBall.obj.rolling_ball.pos.x = xpos
        cueBall.obj.rolling_ball.pos.y = ypos
        cueBall.obj.rolling_ball.vel.x = xvel
        cueBall.obj.rolling_ball.vel.y = yvel
        # not 100% sure if the acceleration part is correct or not.
        ballVel = Coordinate(cueBall.obj.rolling_ball.vel.x, cueBall.obj.rolling_ball.vel.y)
        ballAcc = Coordinate(0.0,0.0);
        speed = phylib.phylib_length(ballVel);
        if(speed > VEL_EPSILON):
            cueBall.obj.rolling_ball.acc.x = -ballVel.x/speed * DRAG;
            cueBall.obj.rolling_ball.acc.y = -ballVel.y/speed * DRAG;
            
        cueBall.obj.rolling_ball.number = 0
        newTable = table
        while table:
            startTime = table.time
            table = table.segment()
            if table != None:
                endTime = table.time
            totalTime = (endTime - startTime) / FRAME_RATE;
            integers = math.floor(totalTime);
            for i in range(integers):
                multiplier = i * FRAME_RATE
                tableTemp = newTable.roll(multiplier);
                # added this line right here to add to an array
                string+=tableTemp.svg();
                tableTemp.time = startTime + multiplier
                tableID = Database().writeTable(tableTemp)
                Database().tableShotInsert(shotID,tableID);
            newTable = table
        #return the array here so that we can use it to get each svg file for animations.
        return string;
        Database().close
