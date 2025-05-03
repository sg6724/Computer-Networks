import math

def calculate_parity_bits(m):
    r = 0
    while (2 ** r) < (m + r + 1):
        r += 1
    return r

def create_hamming_code(data):
    m = len(data)
    r = calculate_parity_bits(m)
    n = m + r
    hamming = [0] * (n + 1)  # 1-indexed array

    j = 0
    for i in range(1, n + 1):
        if math.log2(i).is_integer():
            continue
        hamming[i] = data[j]
        j += 1

    # Calculate parity bits
    for i in range(r):
        parity_pos = 2 ** i
        parity = 0
        for j in range(1, n + 1):
            if j & parity_pos:
                parity ^= hamming[j]
        hamming[parity_pos] = parity

    return hamming[1:]  # skip 0th index

def detect_and_correct(received):
    n = len(received)
    r = int(math.log2(n + 1))
    error_pos = 0

    # Calculate error position
    for i in range(r):
        parity_pos = 2 ** i
        parity = 0
        for j in range(1, n + 1):
            if j & parity_pos:
                parity ^= received[j-1]
        if parity != 0:
            error_pos += parity_pos

    if error_pos == 0:
        print("No error detected.")
    else:
        print(f"Error detected at position {error_pos}")
        # Correct the bit
        received[error_pos - 1] ^= 1
        print(f"Corrected code: {received}")

# Driver code
data = list(map(int, input("Enter data bits separated by space: ").split()))
hamming_code = create_hamming_code(data)
print(f"Hamming code generated: {hamming_code}")

# Introduce error manually
error_code = hamming_code.copy()
pos = int(input(f"Enter position (1-{len(error_code)}) to introduce error (0 for no error): "))
if pos != 0:
    error_code[pos - 1] ^= 1  # Flip the bit

print(f"Received code: {error_code}")

# Detection and Correction
detect_and_correct(error_code)
