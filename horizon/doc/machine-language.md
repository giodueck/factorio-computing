# Machine language

Instruction format:
1. Opcode:      1 byte
2. Destination: 1 byte
3. Arg 1:       1 byte
4. Arg 2:       1 byte

Busses:
A: Arg1
B: Arg2
R: Result

Possible meanings of instruction bytes:
Destination: Always a register
Arg1: Always a register
Arg2: Register or imm8, depending on flag in opcode byte

The largest bit in the instruction byte denotes the type of Arg. 2: 0: Reg., 1: Imm8.
For instructions with 1 argument (e.g. conditions, memory and stack) the flag denotes the type
of Arg. 1: 0: Reg., 1: Imm16.

Immediate values must be added using ALU operations, as only the second argument can ever be an immediate.
To facilitate introducing larger immediates, ALU operations to concatenate values exist. Assembly language could make use of these instructions to abstract away MOVing larger immediates into registers, as MOV itself will be an abstraction built on ALU operations.

Instructions with an asterisk (*) are not basic and may only be included in second iterations.

With all this in mind, the possible instruction formats are:
1. opcode
2. opcode Rd Rn Rm      / opcode Rd Rn      (Rd is result and arg1)
3. opcode Rd Rn imm8    / opcode Rd imm8    (Rd is result and arg1)
4. opcode Rn
5. opcode imm16

## Clock stages
1. Load instruction
2. Load registers
3. Save operation result
4. Instruction over

## Registers
Numbered 0x0 to 0xf:
- 0: R0
- ...
- b: R11
- c: RA: Address register
- d: SP
- e: LR
- f: PC

## ALU Operations: 0x0
Instruction formats: 2, 3, 4 (only not)

- 0: add
- 1: sub
- 2: mul
- 3: div
- 4: mod
- 5: exp
- 6: shl
- 7: shr
- 8: and
- 9: or
- a: not
- b: xor
- c: bcat (concatenate a byte to the end of a register's value, useful to input longer immediates)
- d: hcat (concatenate a half word to the end of a register)

## ALU Operations with condition flags: 0x1
Instruction formats: 2, 3, 4 (only not)

- 0: adds
- 1: subs
- 2: muls
- 3: divs
- 4: mods
- 5: exps
- 6: shls
- 7: shrs
- 8: ands
- 9: ors
- a: nots
- b: xors
- c: bcat
- d: hcat

## COND Operations: 0x2
Instruction formats: 1 (only noop), 4, 5

j__
- 0: eq (Z)
- 1: ne (!Z)
- 2: lt (N != V)
- 3: gt (!Z & N = V)
- 4: le (Z & N != V)
- 5: ge (N = V)
- 6: ng (N)
- 7: pz (!N)
- 8: vs (V)
- 9: vc (!V)
- a: mp (always)
- b: nt (never) (noop)

## Memory access: 0x3
Instruction format: 4

Address used is always the one stored in AR.
Value to store is also always a register, and AR is illegal to use as an operand in memory access instructions

- 0: store
- 1: load
- 2*: storei (store and increment AR)
- 3*: loadi (load and increment AR)
- 4*: stored (store and decrement AR)
- 5*: loadd (load and decrement AR)

## Stack: 0x3
Instruction formats: 1 (only return), 4, 5 (push, call)

The stack is 512 cells wide, and SP always points to the first empty address
on the top of the stack.

The stack is held in an independent block of memory inaccessible by load/store
instructions.

- 8: push
- 9: pop
- a: call
- b: return

## Vector operations
### Registers
Numbered 0x10 to 0x4f
- V0..V15 (operand 1)
- U0..U15 (operand 2)
- T0..T15 (result)
- S0..S15 (result alt)

### Loading and storing
Vx and Ux registers can be written like any other register, and Tx and Sx can be read from, but they are all
one function only. Vx and Ux are write-only and Tx and Sx are read-only for non-vector instructions.

### Vector ALU operations (result T): 0x4
- 0*: vtadd
- 1*: vtsub
- 2*: vtmul
- 3*: vtdiv
- 4*: vtmod
- 5*: vtexp
- 6*: vtshl
- 7*: vtshr
- 8*: vtand
- 9*: vtor
- a*: vtnot
- b*: vtxor

### Vector ALU operations (result S): 0x5
- 0*: vsadd
- 1*: vssub
- 2*: vsmul
- 3*: vsdiv
- 4*: vsmod
- 5*: vsexp
- 6*: vsshl
- 7*: vsshr
- 8*: vsand
- 9*: vsor
- a*: vsnot
- b*: vsxor

### Vector register access: 0x6
- 0: movtv (move registers Tx to Vx)
- 1: movtu (" Tx to Ux)
- 2: movsv (" Sx to Vx)
- 3: movsu (" Sx to Ux)
- 4: copyv (copy single value into all Vx)
- 5: copyu (copy single value into all Vx)

## Test programs
; ALU test
xor r0 r0       0x0b 00 00 00   184549376
xor r1 r1       0x0b 01 01 01   184615169
add r0 #15      0x80 00 00 0f   -2147483633
add r1 #5       0x80 01 01 05   -2147417851
add r2 r0 r1    0x00 02 00 01   131073
subs r3 r1 r2   0x11 03 01 02   285409538
exp r4 r0 r1    0x05 04 00 01   84148225
bcat r5 r1 #5   0x8c 05 01 05   -1945829115
hcat r6 r1 #5   0x8d 06 01 05   -1928986363
jmp #16         0xaa 00 00 10   -1442840560

; For loop (branching) test
add r1 nil #2       0x80 01 ff 02   -2147352830
xor r0 r0           0x0b 00 00 00   184549376
loop:               
    add r0 r1       0x00 00 00 01   1
    subs r1 #1      0x91 01 01 01   -1862205183
    noop            0x2b 00 00 00   721420288
    jne loop        0xa1 00 00 02   -1593835518
end:
jmp pc              0x2a 00 0f 00   704646912

; Stack test
xor r0 r0       0x0b 00 00 00   184549376
add r1 nil #4   0x80 01 ff 04   -2147352828
loop:               2
    push r1     0x38 00 01 00   939524352
    subs r1 #1  0x91 01 01 01   -1862205183
    jne loop    0xa1 00 00 02   -1593835518
loop2:              5
    cmp sp nil  0x11 ff 0d ff   301927935
    jeq end     0xa0 00 00 0a   -1610612726
    pop r1      0x39 01 00 00   956366848
    add r0 r1   0x00 00 00 01   1
    jmp loop2   0xaa 00 00 05   -1442840571
end:                10
jmp pc          0x2a 00 0f 00   704646912