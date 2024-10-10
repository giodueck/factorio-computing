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

Instructions with an asterisk (\*) are marked as To-Do. They are not basic and may only be included in second iterations.

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
- 6: lsh
- 7: rsh
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
- 6: lshs
- 7: rshs
- 8: ands
- 9: ors
- a: nots
- b: xors
- c: bcats
- d: hcats

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
Value to store is a register or imm16 from arg. 1.

- 0: store
- 1: load
- 2: storei (store and increment AR)
- 3: loadi (load and increment AR)
- 4: stored (store and decrement AR)
- 5: loadd (load and decrement AR)

## Stack: 0x3
Instruction formats: 1 (only return), 4, 5 (push, call)

The stack is 512 cells wide, and SP always points to the first empty address
on the top of the stack.

The stack is held in an independent block of memory inaccessible by load/store
instructions.

- 8: push
- 9: pop
- a\*: call (currently a macro: add lr pc #2, jmp \#subroutine)
- b\*: return (currently a macro: jmp lr)

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
- 0\*: vtadd
- 1\*: vtsub
- 2\*: vtmul
- 3\*: vtdiv
- 4\*: vtmod
- 5\*: vtexp
- 6\*: vtlsh
- 7\*: vtrsh
- 8\*: vtand
- 9\*: vtor
- a\*: vtnot
- b\*: vtxor

### Vector ALU operations (result S): 0x5
- 0\*: vsadd
- 1\*: vssub
- 2\*: vsmul
- 3\*: vsdiv
- 4\*: vsmod
- 5\*: vsexp
- 6\*: vslsh
- 7\*: vsrsh
- 8\*: vsand
- 9\*: vsor
- a\*: vsnot
- b\*: vsxor

### Vector register access: 0x6
- 0: movtv (move registers Tx to Vx)
- 1: movtu (" Tx to Ux)
- 2: movsv (" Sx to Vx)
- 3: movsu (" Sx to Ux)
- 4: movvu (" Vx to Ux)
- 5: movuv (" Ux to Vx)
- 6: copyv (copy single value into all Vx)
- 7: copyu (copy single value into all Vx)
