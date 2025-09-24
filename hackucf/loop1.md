# Loop1 — C Menu Practice — 10 pt

**Competition / Platform:** hackucf.org  
**Category:** Reverse / Binary analysis (beginner)  
**Environment:** Linux x86_64, GDB, pwndbg, Ghidra  
**Author:** Mohammad Ali  
**File Name:** loop1

---

## Description
A small C binary that implements a simple interactive menu with three options: say hello, add numbers, and quit. The challenge is to inspect the program behavior and determine whether any hidden functionality (e.g., a `giveFlag` function) is reachable.

---

## Steps / Solution

1. **Make the program executable:**
   ```bash
   chmod +x loop1
2.run the program and interact with the menu:
./loop1
Example run:

csharp
Copy code
Menu:

[1] Say hello
[2] Add numbers
[3] Quit

[>] 1
What is your name? mohammad
Hello, mohammad!

[>] 2
Enter first number: 1
Enter second number: 2
1 + 2 = 3

[>] 3
Goodbye!
3.Search for readable strings inside the binary:

strings ./loop1 | sed -n '1,200p'


Observed output (truncated):

Menu:
[1] Say hello
[2] Add numbers
[3] Quit
[>] 
Unknown input!
What is your name? 
%99s
Unable to read name!
Hello, %s!
Enter first number: 
Unable to read number!
Enter second number: 
%d + %d = %d
Goodbye!
Wow such h4x0r!
Unknown choice: %d
loop1.c
giveFlag

Notes: The presence of %99s indicates bounded name input. The symbol giveFlag appears in the symbol table/strings — this suggests there may be an extra function compiled into the binary that could contain a flag or special behavior.

5.Reason to use Ghidra
Because strings and casual interaction did not reveal any direct way to call giveFlag, deeper static analysis is required to discover how (and if) giveFlag is reachable. Open the binary in Ghidra (or IDA / radare2) to inspect function listings, control flow, and any checks that gate access to hidden functions.
 
 ![Loop1 program menu (screenshot)](hackucf/loop1.png)
 
python3 -c "print(int(0x7a69))"                                                         
31337
lets try it:
┌──(albarbari㉿kali)-[~/CTF/writeups/hackucf]
└─$ ./loop1
Menu:

[1] Say hello
[2] Add numbers
[3] Quit

[>] 31337
Wow such h4x0r!
flag{much_reversing_very_ida_wow}


















