# 64bit — Reverse / Binary analysis — 25 pts

**Competition / Platform:** hackucf.org  
**Category:** Reverse  
**Environment:** Linux x86_64, gdb, pwndbg  
**Author:** kablaa  

**Note:** The flag is the key itself (signed integer — non-standard flag format).  

---

## Description
A 64-bit ELF binary that asks for a key. We must reverse engineer it to find the correct integer key that grants access.

---

## Steps / Solution

1. **Check file type and make it executable**  
Identify the binary format and ensure it can be executed:
```bash
file 64bit
chmod +x 64bit
```
Output:
```
64bit: ELF 64-bit LSB executable, x86-64, dynamically linked, not stripped
```
This tells us it’s a 64-bit ELF and symbols are not stripped, making reverse engineering easier.

---

2. **Run the binary with a random key**  
```bash
./64bit
enter key:
1234
try again
```
It expects a key but doesn’t reveal the correct one.

---

3. **Inspect readable strings**  
```bash
strings 64bit
```
Interesting output:
```
enter key:
win :)
try again
encrypt
main
```
We see references to “encrypt” and success/failure messages, but no key is directly visible.

---

4. **Analyze in GDB with pwndbg**  
Open in gdb and list functions:
```bash
gdb ./64bit
pwndbg> info functions
```
Key functions discovered:
```
encrypt
main
```

---

5. **Disassemble `main`**  
```bash
pwndbg> disas main
```
Relevant part:
```
...
call encrypt
mov [rbp-0x4], eax
cmp [rbp-0x4], 0xdeadbeef
jne ...
```
Explanation:  
- The program reads an integer from the user.  
- It calls `encrypt` with that input.  
- It compares the returned value to `0xdeadbeef`.  
- If equal → prints "win :)", else "try again".

So we need input such that `encrypt(input) == 0xdeadbeef`.

---

6. **Disassemble `encrypt`**  
```bash
pwndbg> disas encrypt
```
Key instructions:
```
mov eax, edi
xor eax, 0x4d2
ret
```
Explanation:  
- The function returns `input ^ 0x4d2`.  
- So: `input ^ 0x4d2 = 0xdeadbeef`.  
- Therefore: `input = 0xdeadbeef ^ 0x4d2`.

---

7. **Compute the correct key**  
Use Python to XOR and convert:
```bash
python3 -c "print(hex(0xDEADBEEF ^ 0x4d2))"
0xdeadba3d
python3 -c "print(int(0xdeadba3d))"
3735927357
```
The key is the integer `3735927357`.

---

8. **Run the program with the correct key**
```bash
./64bit
enter key:
3735927357
win :)
```

---

## Flag
The flag is the key itself:

```
3735927357
```
