MAX_32 = 2**32
MAX_SIGNED = 2**31 - 1

def to_32bit_binary(value: int) -> str:
    """Force value into signed 32-bit range and return binary string."""
    value = value % MAX_32
    if value > MAX_SIGNED:
        value -= MAX_32
    return f"{value & 0xFFFFFFFF:032b}"

def execute(registers, accumulators, src1, src2, set_flags):
    # Fetch operands as integers
    if src1 in registers:
        a = int(registers[src1], 2)
    elif src1 in accumulators:
        a = int(accumulators[src1], 2)
    else:
        a = int(src1, 2)

    if src2 in registers:
        b = int(registers[src2], 2)
    elif src2 in accumulators:
        b = int(accumulators[src2], 2)
    else:
        b = int(src2, 2)

    # Ripple-carry addition
    carry = 0
    result = 0
    for i in range(32):
        abit = (a >> i) & 1
        bbit = (b >> i) & 1
        sum_bit = abit ^ bbit ^ carry
        carry = (abit & bbit) | (abit & carry) | (bbit & carry)
        result |= (sum_bit << i)

    result_bin = to_32bit_binary(result)

    # Store result into ACC1
    accumulators["ACC1"] = result_bin

    # Update flags based on integer result
    set_flags(result)

    print(f"ADD {src1}, {src2} → {result_bin} (stored in ACC1)")
