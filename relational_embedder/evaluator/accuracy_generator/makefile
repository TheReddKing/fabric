BIN_DIR=../bin

CC=gcc
#Using -Ofast instead of -O3 might result in faster code, but is supported only by newer GCC versions
# CFLAGS=-lm -pthread -O3 -march=native -Wall -funroll-loops -Wno-unused-result
CFLAGS=-lm -pthread -O3 -Wall -march=native -funroll-loops  -Wno-unused-result -I/usr/include/malloc # OS X

all: generator

generator : generator.c
	$(CC) generator.c -o ${BIN_DIR}/generator $(CFLAGS)

clean:
	pushd ${BIN_DIR} && rm -rf generator
