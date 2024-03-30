import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future
import os;
import Physics;
import math;
import phylib;

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;


# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/web.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        # check if the web-pages matches the list
        elif parsed.path.startswith("/table") and parsed.path.endswith(".svg"):
           # this one is different because its an image file

            # retreive the JPG file (binary, not text file)
            fp = open( '.'+self.path, 'rb' );
            content = fp.read();

            self.send_response( 200 ); # OK
                # notice the change in Content-type
            self.send_header( "Content-type", "image/svg+xml" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            self.wfile.write( content );    # binary file
            fp.close();

        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


    def do_POST(self):
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        if parsed.path in [ '/display.html' ]:

            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   );
            #this deletes all tabe-?.svg files in the servers directory
            i = 0;
            while os.path.exists("table%d.svg" %i):
                os.remove("table%d.svg" %i);
                i+=1
            
            #this computes the acceleration on the rolling ball
            vel = Physics.Coordinate(float(form["rb_dx"].value), float(form["rb_dy"].value));
            acc = Physics.Coordinate(0.0,0.0);
            
            speed = Physics.phylib.phylib_length(vel);
            
            if(speed > Physics.VEL_EPSILON):
                acc.x = -vel.x/speed * Physics.DRAG;
                acc.y = -vel.y/speed * Physics.DRAG;
            
            # This constructs a table and adds the balls
            table = Physics.Table()

            pos = Physics.Coordinate(float(form["sb_x"].value), float(form["sb_y"].value));
            posr = Physics.Coordinate(float(form["rb_x"].value), float(form["rb_y"].value));

            sb = Physics.StillBall(1, pos)

            rb = Physics.RollingBall(0, posr, vel, acc)

            table += sb

            table += rb

            #this saves the table-?.svg files to the same directory as the server
            i = 0;
            while table:
                f = open("table%d.svg" %(i), "w");
                string = table.svg();
                f.write(string);
                f.close();
                i+=1;
                table = table.segment()

            # our "nice" HTML page
            string = """
            <html>
                <head>
                    <title> shoot</title>
                </head>
                <body>
                <a href = "/shoot.html">Back</a>
            """
            string += "<p> Still Ball: position=(%.2f,%.2f) veocity=(0.0,0.0) acceleration=(0.0,0.0)</p>" %(sb.obj.still_ball.pos.x, sb.obj.still_ball.pos.y) 
            string += "<p> Rolling Ball: position=(%.2f,%.2f) velocity=(%.2f,%.2f) acceleration=(%.2f,%.2f) </p>" %(rb.obj.rolling_ball.pos.x, rb.obj.rolling_ball.pos.y, rb.obj.rolling_ball.vel.x, rb.obj.rolling_ball.vel.y, rb.obj.rolling_ball.acc.x, rb.obj.rolling_ball.acc.y)
            
            j=0
            for j in range(i):
                string+="""<img src="/table%d.svg">""" %(j)
                j+=1
            
            string+= """</body>
                    </html>
            """
            content = string  

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the browser
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();