import time

MAX_32 = 2**32
MAX_SIGNED = 2**31 - 1
MIN_SIGNED = -2**31

def to_32bit_binary(value: int) -> str:
    value = value % MAX_32
    if value > MAX_SIGNED:
        value -= MAX_32
    return f"{value & 0xFFFFFFFF:032b}"

def is_binary_string(s: str) -> bool:
    return s != "" and all(ch in "01" for ch in s)

class CPU:
    def __init__(self, register_count=35):
        self.registers = {f"R{i}": "0"*32 for i in range(1, register_count+1)}
        self.accumulators = {"ACC1": "0"*32, "ACC2": "0"*32}
        self.flags = {"ZERO":0,"NEG":0,"CARRY":0,"OVERFLOW":0}
        self.pc = 0
        self.instructions = []
        self.labels = {}
        self.halted = False

        self.dispatch = {
            "LOAD": self._op_load,
            "MOV": self._op_mov,
            "ADD": self._op_add,
            "SUB": self._op_sub,
            "MUL": self._op_mul,
            "DIV": self._op_div,
            "FDIV": self._op_fdiv,
            "MOD": self._op_mod,
            "CMP": self._op_cmp,
            "JMP": self._op_jmp,
            "JZ": self._op_jz,
            "JNZ": self._op_jnz,
            "PRINT": self._op_print,
            "EXIT": self._op_exit
        }

    def set_flags(self, value: int):
        self.flags["ZERO"] = int(value == 0)
        self.flags["NEG"] = int(value < 0)
        self.flags["CARRY"] = int(value > MAX_SIGNED or value < MIN_SIGNED)
        self.flags["OVERFLOW"] = int(not MIN_SIGNED <= value <= MAX_SIGNED)

    def execute(self, instruction: str):
        parts = instruction.split()
        if not parts: return
        op = parts[0].upper()
        print(f"\nExecuting (PC={self.pc}): {instruction}")
        handler = self.dispatch.get(op)
        if handler: handler(parts)
        else: print("Unknown instruction")

    def _op_load(self, parts):
        dest = parts[1].replace(",", "")
        val = parts[2]
        if not is_binary_string(val): raise ValueError(f"Invalid binary input: {val}")
        binval = to_32bit_binary(int(val,2))
        if dest in self.registers: self.registers[dest] = binval
        elif dest in self.accumulators: self.accumulators[dest] = binval
        print(f"Loaded {binval} into {dest}")

    def _op_mov(self, parts):
        dest = parts[1].replace(",", "")
        src = parts[2]
        val = to_32bit_binary(self._get_val(src))
        if dest in self.registers: self.registers[dest] = val
        elif dest in self.accumulators: self.accumulators[dest] = val
        print(f"MOV {src} → {dest} = {val}")

    # ALU ops now use _get_val
    def _op_add(self, parts):
        dest = parts[1].replace(",", "")
        src = parts[2]
        result = int(self.registers[dest], 2) + self._get_val(src)
        self.accumulators["ACC1"] = to_32bit_binary(result)
        self.set_flags(result)
        print(f"ADD {dest}, {src} → ACC1 = {self.accumulators['ACC1']}")

    def _op_sub(self, parts):
        dest = parts[1].replace(",", "")
        src = parts[2]
        result = int(self.registers[dest], 2) - self._get_val(src)
        self.accumulators["ACC1"] = to_32bit_binary(result)
        self.set_flags(result)
        print(f"SUB {dest}, {src} → ACC1 = {self.accumulators['ACC1']}")

    def _op_mul(self, parts):
        dest = parts[1].replace(",", "")
        src = parts[2]
        result = int(self.registers[dest], 2) * self._get_val(src)
        self.accumulators["ACC1"] = to_32bit_binary(result)
        self.set_flags(result)
        print(f"MUL {dest}, {src} → ACC1 = {self.accumulators['ACC1']}")

    def _op_div(self, parts):
        dest = parts[1].replace(",", "")
        src = parts[2]
        divisor = self._get_val(src)
        if divisor == 0: raise ZeroDivisionError("Division by zero")
        result = int(self.registers[dest], 2) // divisor
        self.accumulators["ACC1"] = to_32bit_binary(result)
        self.set_flags(result)
        print(f"DIV {dest}, {src} → ACC1 = {self.accumulators['ACC1']}")

    def _op_fdiv(self, parts):
        dest = parts[1].replace(",", "")
        src = parts[2]
        divisor = self._get_val(src)
        if divisor == 0: raise ZeroDivisionError("Division by zero")
        result = int(self.registers[dest], 2) / divisor
        self.accumulators["ACC1"] = to_32bit_binary(int(result))
        self.set_flags(int(result))
        print(f"FDIV {dest}, {src} → ACC1 = {self.accumulators['ACC1']}")

    def _op_mod(self, parts):
        dest = parts[1].replace(",", "")
        src = parts[2]
        divisor = self._get_val(src)
        if divisor == 0: raise ZeroDivisionError("Modulo by zero")
        result = int(self.registers[dest], 2) % divisor
        self.accumulators["ACC1"] = to_32bit_binary(result)
        self.set_flags(result)
        print(f"MOD {dest}, {src} → ACC1 = {self.accumulators['ACC1']}")

    def _op_cmp(self, parts):
        dest = parts[1].replace(",", "")
        src = parts[2]
        result = int(self.registers[dest], 2) - self._get_val(src)
        self.set_flags(result)
        print(f"CMP {dest}, {src} → result = {result}")

    def _op_jmp(self, parts):
        label = parts[1]
        if label in self.labels: self.pc = self.labels[label]; print(f"Jump → {label}")

    def _op_jz(self, parts):
        label = parts[1]
        if self.flags["ZERO"]==1 and label in self.labels: self.pc=self.labels[label]; print(f"JZ → {label}")

    def _op_jnz(self, parts):
        label = parts[1]
        if self.flags["ZERO"]==0 and label in self.labels: self.pc=self.labels[label]; print(f"JNZ → {label}")

    def _op_print(self, parts):
        reg = parts[1]
        val = self._get_val(reg)
        print(f"PRINT {reg} → {to_32bit_binary(val)}")

    def _op_exit(self, parts):
        print("Program requested exit."); self.halted=True

    def _get_val(self, name: str) -> int:
        # Indirect addressing: [Rk] means "use register whose index is in Rk"
        if name.startswith("[") and name.endswith("]"):
            ptr = name[1:-1]  # strip brackets, e.g. "R15"
            if ptr not in self.registers:
                raise ValueError(f"Invalid pointer register: {ptr}")
            idx = int(self.registers[ptr], 2)
            regname = f"R{idx}"
            if regname not in self.registers:
                raise ValueError(f"Register {regname} does not exist")
            return int(self.registers[regname], 2)

        if name in self.registers: return int(self.registers[name], 2)
        if name in self.accumulators: return int(self.accumulators[name], 2)
        if is_binary_string(name): return int(name, 2)
        raise ValueError(f"Invalid operand: {name}")

    def dump_state(self):
        print("\nRegisters:")
        for r, v in self.registers.items():
            print(f"{r}: {v}")
        print("\nAccumulators:")
        for a, v in self.accumulators.items():
            print(f"{a}: {v}")
        print("\nFlags:")
        for f, v in self.flags.items():
            print(f"{f}: {v}")

    def run_file(self, filename):
        self.instructions = []
        self.labels = {}
        with open(filename) as f:
            for line in f:
                line = line.split(";")[0].strip()
                if not line:
                    continue
                if line.endswith(":"):
                    self.labels[line[:-1]] = len(self.instructions)
                else:
                    self.instructions.append(line)
        self.pc = 0
        self.halted = False
        start = time.time()
        while self.pc < len(self.instructions) and not self.halted:
            current_pc = self.pc
            instr = self.instructions[self.pc]
            self.execute(instr)
            if self.pc == current_pc:
                self.pc += 1
        end = time.time()
        print(f"\nComputation time for {filename}: {end-start:.6f} seconds")
        self.dump_state()
