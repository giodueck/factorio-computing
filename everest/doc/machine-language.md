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
- 11: NIL result (Result address = 255) (Enable disables bit 12)
- 12: Save register (0: dest, 1: arg1) (Enable allows 2 direction instructions, ex. add r1 r2)
- 13: Load register arg1
- 14: Load register arg2
- 15: Store in RAM  (Address from A)
- 16: Load from RAM (Address from A)
- 17: 
- 18: Imm16 from arg1 and arg2 (Loaded onto A)
- 19: Imm8 from arg1
- 20: Imm8 from arg2
- 21: Imm16 from dest and arg1 (Loaded onto A, arg2 becomes the only argument)
- 22: Enable write to PC
- 23-24: 0: nothing, 1: increment result, 2: decrement result
- 25: Push
- 26: Pop
- 27: Halt
- 28: Reset

## Instructions

0: NOOP
- 11

1: HALT
- 11?
- 27

2: RESET
- 11?
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

