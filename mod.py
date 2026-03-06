MAX_32 = 2**32
MAX_SIGNED = 2**31 - 1

def to_32bit_binary(value: int) -> str:
    value = value % MAX_32
    if value > MAX_SIGNED:
        value -= MAX_32
    return f"{value & 0xFFFFFFFF:032b}"

def execute(registers, accumulators, src1, src2, set_flags):
    a = int(registers[src1], 2) if src1 in registers else int(accumulators[src1], 2)
    b = int(registers[src2], 2) if src2 in registers else int(accumulators[src2], 2)

    if b == 0:
        raise ZeroDivisionError("Modulo by zero")

    remainder = a % b
    result_bin = to_32bit_binary(remainder)
    accumulators["ACC1"] = result_bin
    set_flags(remainder)
    print(f"MOD {src1}, {src2} → {result_bin} (stored in ACC1)")
