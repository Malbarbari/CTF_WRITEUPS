# Mildred — Base64 / Simple — 20 pts

**Competition / Platform:** hackucf.org  
**Category:** Reverse / Binary analysis (Beginner)  
**Environment:** Linux i386 (ELF 32-bit), Tools: `strings`, `base64`, local execution  
**File Name:** `mildred`  

---

## Description
A small ELF binary that requires a password when executed.  
The goal is to analyze its behavior and extract the password/flag embedded in the binary instead of guessing.

---

## Steps / Solution

1. **Check file type and make it executable**  
   ```bash
   file mildred
   chmod +x mildred
   ```
   Run the program with no or random passwords:
   ```bash
   ./mildred
   # Usage: ./mildred PASSWORD

   ./mildred 123
   # Come on, even my aunt Mildred got this one!
   ```
   → The binary expects a password argument.

2. **Search for readable strings inside the binary**  
   We use the `strings` tool to list all printable strings:
   ```bash
   strings mildred
   ```
   Key output:
   ```
   Usage: %s PASSWORD
   malloc failed
   ZjByX3kwdXJfNWVjMG5kX2xlNTVvbl91bmJhc2U2NF80bGxfN2gzXzdoMW5nNQ==
   Correct password!
   Come on, even my aunt Mildred got this one!
   ```
   **Explanation:** Among the output we can clearly see a long Base64-looking string ending with `=`, which is very likely the hidden password.

3. **Decode the Base64 string**  
   ```bash
   echo "ZjByX3kwdXJfNWVjMG5kX2xlNTVvbl91bmJhc2U2NF80bGxfN2gzXzdoMW5nNQ==" | base64 -d
   ```
   Output:
   ```
   f0r_y0ur_5ec0nd_le55on_unbase64_4ll_7h3_7h1ng5
   ```

4. **Use the decoded string as the password**  
   ```bash
   ./mildred f0r_y0ur_5ec0nd_le55on_unbase64_4ll_7h3_7h1ng5
   ```
   Output:
   ```
   Correct password!,,,,,,, Aunt Mildred
   20
   ```

5. **Flag**  
   The flag is simply the decoded password:
   ```
   f0r_y0ur_5ec0nd_le55on_unbase64_4ll_7h3_7h1ng5
   ```
