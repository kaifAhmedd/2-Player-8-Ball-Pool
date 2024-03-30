CC = clang
CFLAGS = -Wall -std=c99 -pedantic -g
PYTHON =python3.11

all: _phylib.so

clean:  
	rm -f *.o *.so *.svg myprog phylib_wrap.c phylib.py


phylib_wrap.c phylib.py: phylib.i
	swig -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -fPIC -o phylib_wrap.o -I /usr/include/$(PYTHON)

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) phylib_wrap.o -L. -L /usr/lib/$(PYTHON) -l phylib -l $(PYTHON) -shared -o _phylib.so


libphylib.so: phylib.o
	$(CC) $(CFLAGS) phylib.o -shared -o libphylib.so

phylib.o:  phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -fPIC -o phylib.o

# myprog:  main.o libphylib.so
# 	$(CC) $(CFLAGS) main.o -lm -L. -lphylib -o myprog