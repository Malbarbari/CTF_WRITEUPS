# Conditional 1 — 5 pt

**Competition / Platform:** hackucf.org  
**Category:** Reverse  
**Environment:** Linux x86_64  
**Author:** kablaa  
**File Name:** conditional1  

## Description
Hint: If only there were a good tool to list strings used by a program...

*This challenge requires providing the correct password to the program in order to retrieve the flag.

## Steps

1. **Make the program executable**  

chmod +x conditional1
2. run the file 
./conditional1
# Output: Usage: ./conditional1 password --->The program shows usage instructions and asks for a password.
3. test anything:
./conditional1 123
# Output: Access denied.---->he program denies access when the password is incorrect.
4.Find the correct password inside the binary using strings:
strings conditional1 | grep password
# Output: super_secret_password 
5.Run the program with the correct password
./conditional1 super_secret_password
# Output: Access granted. ------>here we go

the flag: flag{if_i_submit_this_flag_then_i_will_get_points}
