def xor(a, b):
    result = []
    for i in range(1, len(b)):
        result.append('0' if a[i] == b[i] else '1')
    return ''.join(result)

def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0:pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0'*pick, tmp) + dividend[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)

    return tmp

def encodeData(data, key):
    appended_data = data + '0'*(len(key)-1)
    remainder = mod2div(appended_data, key)
    codeword = data + remainder
    return codeword

def detectError(data, key):
    remainder = mod2div(data, key)
    if '1' in remainder:
        print("Error detected!")
    else:
        print("No error detected.")

# Example Usage
data = input("Enter data bits (7 or 8 bits): ")  # Example: 1010101
key = input("Enter divisor polynomial (CRC key): ")  # Example: 1001 (x^3 + 1)

print("\n--- Sender Side ---")
encoded_data = encodeData(data, key)
print("Encoded data (data + CRC):", encoded_data)

print("\n--- Receiver Side ---")
received_data = input("Enter received data: ")  # You can change a bit manually to simulate error
detectError(received_data, key)
