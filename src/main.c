#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>

#include "brainf.h"

void printHelp() {
    fprintf(stderr, "bftoc %d.%d - Brainf*ck to C transpiler\n\nUsage: bftoc [file] [options]\nOptions:\nh - print this message and exit\nv - print the version and exit\ni - enter interactive mode\nc [statement] - execute a statement and exit\no [filename] - specify an output C source file\n", BF_MAJ_V, BF_MIN_V);
}

void printVersion() {
    printf("%d.%d\n", BF_MAJ_V, BF_MIN_V);
}

int main(int argc, char *const *argv) {
    int op;
    while ((op = getopt(argc, argv, "hvic:o:")) != -1) {
        switch (op) {
            case 'h':
            printHelp();
            exit(0);
            break;
            case 'v':
            printVersion();
            exit(0);
            break;
            case 'i':
            interactive();
            break;
        }
    }
}
