# Machine language and Microcode

Instruction format:
1. Instruction: 1 byte
2. Destination: 1 byte
3. Arg 1:       1 byte
4. Arg 2:       1 byte

Busses:
A: Typically used for arg1 in e.g. the ALU or when executing MOV
B: Like A, but for arg2
R: Result

## Microcode bits
- [x] 0-3: ALU instruction
- [x] 4-7: COND instruction
- [x] 8: Enable ALU
- [x] 9: Enable COND
- [x] 10: Save flags
- [x] 11: NIL result (Result address = 255)
- [x] 12: Arg1 to result (R = A)
- [x] 13: Load register arg1 (Loaded onto A)
- [x] 14: Load register arg2 (Loaded onto B)
- [x] 15: Store in RAM  (Address from A, value from B)
- [x] 16: Load from RAM (Address from A, value onto R)
- [ ] 17: Arg2 to result (R = B)
- [x] 18: Imm16 from arg1 and arg2 (Loaded onto A)
- [x] 19: Imm8 from arg1 (Loaded onto A)
- [x] 20: Imm8 from arg2 (Loaded onto B)
- [x] 21: Imm16 from dest and arg1 (Loaded onto A, arg2 becomes the only argument)
- [ ] 22: 
- [ ] 23-24: 
- [x] 25: Push (Value from A)
- [x] 26: Pop  (Value onto R)
- [x] 27: Clear SP
- [ ] 28: 
- [x] 29-30: Special destination: 0: nothing, 1: nothing, 2: LR, 3: PC
- [ ] 31: 

## ALU Operations
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
- 10: not
- 11: xor

## COND Operations
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
- 10: al (always)

## Stack

The stack is 512 cells wide, and SP always points to the first empty address
on the top of the stack.

The stack is held in an independent block of memory inaccessible by load/store
instructions.

Bit 27 of the Microcode controls clearing the SP, effectively clearing the stack.

## Instructions

- [x] 0: NOOP
- 11

- [x] 1: HALT
(Not a dedicated instruction, use JMP PC instead)

- [x] 2: RESET
- 4-7: 10
- 9
- 11
- 29-30: 3
(Same as JMP IMM16, but ignores arguments which causes the resulting address to be 0)

- [x] 3: MOV REG
- 12
- 13

- [x] 4: MOV IMM16
- 12
- 18

- [x] 5: MOVS REG
- 10
- 12
- 13

- [x] 6: MOVS IMM16
- 10
- 12
- 18

- [x] 7: STR REG\
  Store register (arg2) in address in register (arg1)
- 11
- 13
- 14
- 15

- [x] 8: STR IMM16\
  Store register (arg2) in immediate address (dest << 8 | arg1)
- 11
- 14
- 15
- 21

- [x] 9: LDR REG\
  Load register (dest) from address in register (arg1)
- 13
- 16

- [x] 10: LDR IMM16\
  Load register (dest) from immediate address (arg1 << 8 | arg2)
- 16
- 18

- [x] 11-12: LDRS
- 10
- Everything else the same

- [x] 15-19: ADD/MUL/AND/OR/XOR REG REG
- 0-3: corresponding ALU code
- 8
- 13
- 14

- [x] 20-24: ADD/MUL/AND/OR/XOR REG IMM8
- 0-3: corresponding ALU code
- 8
- 13
- 20

- [x] 25-30: SUB/DIV/MOD/EXP/LSH/RSH REG REG
- 0-3: corresponding ALU code
- 8
- 13
- 14

- [x] 31-36: SUB/DIV/MOD/EXP/LSH/RSH REG IMM8
- 0-3: corresponding ALU code
- 8
- 13
- 20

- [x] 37-42: SUB/DIV/MOD/EXP/LSH/RSH IMM8 REG
- 0-3: corresponding ALU code
- 8
- 14
- 19

- [x] 43: NOT REG
- 0-3: 10
- 8
- 13

- [x] 44: NOT IMM16
- 0-3: 10
- 8
- 18

- [x] 45: NOTS REG
- 0-3: 10
- 8
- 10
- 13

- [x] 46: NOTS IMM16
- 0-3: 10
- 8
- 10
- 18

- [x] 47-74: Arithmetic and bitwise with flags (CMP = SUBS with NIL result)
- 10
- Everything else the same

- [x] 75: JMP IMM16
- 4-7: 10
- 9
- 11
- 18
- 29-30: 3

- [x] 76: JMP REG
- 4-7: 10
- 9
- 11
- 13
- 29-30: 3

- [x] 77-86: J\<C\> IMM16
- 4-7: 0-9
- 9
- 11
- 18
- 29-30: 3

- [x] 87-96: J\<C\> REG
- 4-7: 0-9
- 9
- 11
- 13
- 29-30: 3

- [x] 97: PUSH REG
- 11
- 13
- 25

- [x] 98: PUSH IMM16
- 11
- 18
- 25

- [x] 99: POP REG
- 26

- [x] 100: POPS REG
- 10
- 26

- [x] 101: CLSP
- 11
- 27