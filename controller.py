import sys
import time
from cpu import CPU


def run_file(filename):
    cpu = CPU()  # Fresh CPU instance per run

    try:
        start = time.time()
        cpu.run_file(filename)
        end = time.time()

        print(f"\n[Controller] Total execution time: {end - start:.6f} seconds")

    except SystemExit:
        # Catch EXIT instruction so terminal doesn't close
        print("\nProgram finished.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Runtime error: {e}")


def interactive():
    print("CPU Terminal — type instructions or 'exit'")
    print("Use: run filename.testa  → execute a program file")

    cpu = CPU()

    while True:
        try:
            cmd = input(">> ").strip()

            if not cmd:
                continue

            if cmd.lower() == "exit":
                print("Exiting terminal.")
                break

            if cmd.startswith("run "):
                filename = cmd.split(" ", 1)[1]
                run_file(filename)
                continue

            # Single instruction mode
            start = time.time()
            cpu.execute(cmd)
            end = time.time()

            print(f"[Instruction time: {end - start:.6f} sec]")

        except SystemExit:
            print("Program finished.")
        except Exception as e:
            print(f"Error: {e}")

    print("\nFinal CPU State:")
    cpu.dump_state()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        interactive()
