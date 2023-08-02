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
- 0-3: ALU instruction
- 4-7: COND instruction
- 8: Enable ALU
- 9: Enable COND (writes to PC)
- 10: Save flags
- 11: NIL result (Result address = 255)
- 12: Arg1 to result (R = A)
- 13: Load register arg1
- 14: Load register arg2
- 15: Store in RAM  (Address from A)
- 16: Load from RAM (Address from A)
- 17: Arg2 to result (R = B)
- 18: Imm16 from arg1 and arg2 (Loaded onto A)
- 19: Imm8 from arg1 (Loaded onto A)
- 20: Imm8 from arg2 (Loaded onto B)
- 21: Imm16 from dest and arg1 (Loaded onto A, arg2 becomes the only argument)
- 22: 
- 23-24: 0: nothing, 1: increment result, 2: decrement result
- 25: Push
- 26: Pop
- 27: Halt
- 28: Reset
- 29-30: Special destination: 0: nothing, 1: SP, 2: LR, 3: PC
- 31: Special destination bus (0: destination, 1: Load into A)

## Instructions

0: NOOP
- 11

1: HALT
- 11
- 27

2: RESET
- 11
- 28

3: MOV REG
- 13

4: MOV IMM16
- 18

5: MOVS REG
- 10
- 13

6: MOVS IMM16
- 10
- 18

7: STR REG
- 13
- 15

8: STR IMM16
- 15
- 18

9: LDR REG
- 13
- 16

10: LDR IMM16
- 16
- 18

11-14: STRS/LDRS
- 10
- Everything else the same

15-19: ADD/MUL/AND/OR/XOR REG REG
- 0-3: 0-4
- 8
- 13
- 14

20-24: ADD/MUL/AND/OR/XOR REG IMM8
- 0-3: 0-4
- 8
- 13
- 20

25-30: SUB/DIV/MOD/EXP/LSH/RSH REG REG
- 0-3: 5-10
- 8
- 13
- 14

31-36: SUB/DIV/MOD/EXP/LSH/RSH REG IMM8
- 0-3: 5-10
- 8
- 13
- 20

37-42: SUB/DIV/MOD/EXP/LSH/RSH IMM8 REG
- 0-3: 5-10
- 8
- 14
- 19

43-44: INC/DEC REG
- 12
- 13
- 23-24: 1-2

45: NOT REG
- 0-3: 11
- 8
- 13

46: NOT IMM8
- 0-3: 11
- 8
- 19

47-74: Arithmetic and bitwise with flags (CMP = SUBS with NIL result)
- 10
- Everything else the same

75: JMP IMM16
- 4-7: 6
- 9
- 12
- 18
- 29-30: 3

76: JMP REG
- 4-7: 6
- 9
- 12
- 13
- 29-30: 3

77-82: J\<C\> IMM16
- 4-7: 0-5
- 9
- 12
- 18
- 29-30: 3

83-88: J\<C\> REG
- 4-7: 0-5
- 9
- 12
- 13
- 29-30: 3

89: PUSH REG
- 12
- 13
- 25

90: PUSH IMM16
- 12
- 18
- 25

91: POP REG
- 26