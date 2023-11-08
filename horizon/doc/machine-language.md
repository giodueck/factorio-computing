# Machine language

Instruction format:
1. Instruction: 1 byte
2. Destination: 1 byte
3. Arg 1:       1 byte
4. Arg 2:       1 byte

Busses:
A: Typically used for arg1 in e.g. the ALU or when executing MOV
B: Like A, but for arg2
R: Result

## Registers
- 0: R0
- ...
- b: R11
- c: RA: Address register
- d: SP
- e: LR
- f: PC

## ALU Operations: 0x0
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

## ALU Operations with condition flags: 0x1
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

## COND Operations: 0x2
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
- a: al (always)
- b: nt (never) (noop)

## Stack: 0x3

The stack is 512 cells wide, and SP always points to the first empty address
on the top of the stack.

The stack is held in an independent block of memory inaccessible by load/store
instructions.

- 0: push
- 1: pop
- 2: call
- 3: return

## Memory access: 0x4
Address used is always the one stored in RA.
Value to store is also always a register, and RA is illegal to use as an operand in memory access instructions

- 0: store
- 1: storei (store and increment RA)
- 2: load
- 3: loadi (load and increment RA)
- 4: stored (store and decrement RA)
- 5: loadd (load and decrement RA)

## Vector operations
### Registers
- V0..V15 (operand 1)
- U0..U15 (operand 2)
- T0..T15 (result)
- S0..S15 (result alt)

### Loading and storing
Vx and Ux registers can be written like any other register, and Tx and Sx can be read from, but they are all
one function only. Vx and Ux are write-only and Tx and Sx are read-only for non-vector instructions.

### Vector ALU operations (result T): 0xa
- 0: vtadd
- 1: vtsub
- 2: vtmul
- 3: vtdiv
- 4: vtmod
- 5: vtexp
- 6: vtshl
- 7: vtshr
- 8: vtand
- 9: vtor
- a: vtnot
- b: vtxor

### Vector ALU operations (result S): 0xb
- 0: vsadd
- 1: vssub
- 2: vsmul
- 3: vsdiv
- 4: vsmod
- 5: vsexp
- 6: vsshl
- 7: vsshr
- 8: vsand
- 9: vsor
- a: vsnot
- b: vsxor

### Vector register access: 0xc
- 0: movtv (move registers Tx to Vx)
- 1: movtu (" Tx to Ux)
- 2: movsv (" Sx to Vx)
- 3: movsu (" Sx to Ux)
- 4: copyv (copy single value into all Vx)
- 5: copyu (copy single value into all Vx)