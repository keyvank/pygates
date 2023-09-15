# The Super Programmer's Processor

A Von-Neumann Brainfuck CPU

```
FWD
P = P + 1
PC = PC + 1
MEM[P] = MEM[P]

BWD
P = P - 1
PC = PC + 1
MEM[P] = MEM[P]

INC
P = P
PC = PC + 1
MEM[P] = MEM[P] + 1

DEC
P = P
PC = PC + 1
MEM[P] = MEM[P] - 1

JZ
P = P
PC = X
MEM[P] = MEM[P]
```

```
P =
    p+1 if 0b000
    p-1 if 0b001
    else p

PC =
    X if 0b100 && 
    else PC + 1

MEM[P] =
    MEM[P] + 1 if 0b010
    MEM[P] - 1 if 0b011
    else MEM[P]
```