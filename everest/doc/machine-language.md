# Machine language and Microcode

Instruction format:
1. Instruction: 1 byte
2. Destination: 1 byte
3. Arg 1:       1 byte
4. Arg 2:       1 byte

## Microcode bits
- 0-3: ALU instruction
- 4-7: COND instruction
- 8: Enable ALU
- 9: Enable COND (writes to PC)
- 10: Save flags
- 11: NIL result (Result address = 255)
- 12: Save register (0: arg1, 1: dest)
- 13: Load register arg1
- 14: Load register arg2
- 15: Store in RAM
- 16: Load from RAM
- 17: RAM address from register (arg1)
- 18: Imm16 from arg1 and arg2
- 19: Imm8 from arg1
- 20: Imm8 from arg2
- 21: Imm16 from dest and arg1 (arg2 becomes the only argument)
- 22: Enable write to PC
- 23-24: 0: nothing, 1: increment result, 2: decrement result
- 25: Push
- 26: Pop
- 27: Halt
- 28: Reset