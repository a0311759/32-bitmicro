def execute(registers, accumulators, src1, src2, set_flags):
    # Fetch src1
    if src1 in registers:
        a = int(registers[src1], 2)
    elif src1 in accumulators:
        a = int(accumulators[src1], 2)
    else:
        a = int(src1, 2)   # <-- handle binary literal

    # Fetch src2
    if src2 in registers:
        b = int(registers[src2], 2)
    elif src2 in accumulators:
        b = int(accumulators[src2], 2)
    else:
        b = int(src2, 2)   # <-- handle binary literal

    # Two’s complement subtraction
    b_twos = (~b + 1) & 0xFFFFFFFF
    result = (a + b_twos) & 0xFFFFFFFF

    result_bin = f"{result & 0xFFFFFFFF:032b}"
    accumulators["ACC1"] = result_bin
    set_flags(result)
    print(f"SUB {src1}, {src2} → {result_bin} (stored in ACC1)")
