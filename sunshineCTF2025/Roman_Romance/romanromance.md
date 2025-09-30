# Roman Romance — Writeup
**Author:** Uvuv  
**Challenge:** Roman Romance (sunshineCTF2025)  
**Category:** Reverse / Binary  
**Files provided:** `romanromance` (ELF), `enc.txt`  
**Flag format:** nonstandard `sunshine{}`

---
When in Rome...
---

## 1 — Initial Reconnaissance
Quick inspection of the ELF and text file:

```sh
$ file romanromance
romanromance: ELF 64-bit LSB pie executable, x86-64, dynamically linked, for GNU/Linux

$ cat enc.txt
tvotijof|lO1x`z1v5`s1nAo`iJ6u1sZ~
```

Strings inspection revealed references to `flag.txt` and `enc.txt`, along with a ransom note — suggesting the program reads `flag.txt` and writes `enc.txt`.

---

## 2 — Quick Decompilation Analysis (ghidra,binaryninga,IDA...)
Key snippet from the decompiled `main` function:

```c
pFVar1 = fopen("flag.txt","r+b");
fseek(pFVar1,0,2);
__size = ftell(pFVar1);
rewind(pFVar1);
__ptr = malloc(__size);
sVar3 = fread(__ptr,1,__size,pFVar1);
for (local_30 = 0; local_30 < (long)__size; local_30++) {
  *(char *)((long)__ptr + local_30) = *(char *)((long)__ptr + local_30) + '';
}
...
pFVar1 = fopen("enc.txt","w");
fwrite(__ptr,1,__size,pFVar1);
```

**Conclusion:** Each byte in `flag.txt` is incremented by `1` and saved to `enc.txt`. To decrypt, subtract `1` from each byte.

---

## 3 — Decryption Method
### Python Script to Decrypt
Save the following as `decrypt.py` in the same directory (or run directly in shell):

```python
#!/usr/bin/env python3
# decrypt.py - subtract 1 from each character in enc.txt and print result
f = open("enc.txt", "r")
data = f.read()
f.close()

new_text = ""
for c in data:
    new_text += chr(ord(c) - 1)

print(new_text)

### Example Run and Result

```sh
$ python3 decrypt.py
sunshine{kN0w_y0u4_r0m@n_hI5t0rY}
```

**Final Flag:** `sunshine{kN0w_y0u4_r0m@n_hI5t0rY}`

---


