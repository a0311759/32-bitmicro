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
        raise ZeroDivisionError("FDIV by zero")

    quotient = a // b
    remainder = a % b

    # Approximate fractional part with 16 bits
    frac = 0
    for i in range(16):
        remainder <<= 1
        frac <<= 1
        if remainder >= b:
            remainder -= b
            frac |= 1

    result_bin = to_32bit_binary(quotient)
    accumulators["ACC1"] = result_bin
    accumulators["ACC2"] = f"{frac:016b}"  # fractional bits
    set_flags(quotient)
    print(f"FDIV {src1}, {src2} → int={result_bin}, frac={accumulators['ACC2']} (stored in ACC1/ACC2)")
