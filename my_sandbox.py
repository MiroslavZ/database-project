def encrypted_string(line: str) -> str:
    line_e = line.encode('utf-8')
    array_bytes = []
    for byte in line_e:
        array_bytes.append(byte)
    result = ""
    for e in array_bytes:
        result += f'*{str(e)}'
    return result[1:]


def decrypt_string(line: str) -> str:
    line_s = line.split('*')
    line_e = []
    for i in range(0, line_s.__len__()):
        line_e.append(int(line_s[i]))
    return bytes(line_e).decode('utf-8')


name = encrypted_string('Мурзик')
print(name)
name = decrypt_string(name)
print(name)
