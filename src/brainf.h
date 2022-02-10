#ifndef BRAINF_H
#define BRAINF_H

#define BF_MAJ_V 1
#define BF_MIN_V 0

#define tI '+'
#define tD '-'
#define tL '<'
#define tR '>'
#define tG ','
#define tP '.'
#define tS '['
#define tE ']'

struct Instruction {
    char t;
    int a;
    struct Instruction *p, *n, *l;
};

void printHelp();
void printVersion();
void interactive();

#endif /* BRAINF_H */
