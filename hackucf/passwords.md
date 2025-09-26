# Source Protection — SunshineCTF 2018 (50 pts)

**File:** `passwords.exe`  
**Platform:** SunshineCTF 2018  
**Category:** Reverse / Binary analysis  
**Environment:** Windows PE (PyInstaller), analysis on Linux  
**Author:** dmaria

---

## Description

People said I shouldn't use Python to write my password vault because they would be able to read my source code, but they underestimated how smart I am.  
In fact, I'm so confident in my source code protection that I'm going to upload my password vault and challenge a bunch of nerds to hack it. Good luck :)

---


### 1️⃣ Identify the binary type

Run:

```bash
file passwords.exe
```

Output:

```text
passwords.exe: PE32 executable for MS Windows 6.00 (console), Intel i386, 6 sections
```

**Explanation:** The `file` output shows this is a Windows PE32 executable (32-bit). Many Python applications distributed for Windows are packaged with PyInstaller, so this is a strong hint the binary contains embedded Python bytecode.

---

### 2️⃣ Quick string check

Run:

```bash
strings passwords.exe | grep password
```

Output:

```text
spasswords
bpasswords.exe.manifest
opyi-windows-manifest-filename passwords.exe.manifest
```

**Explanation:** Only filenames and manifest references appear. No readable flag or password is present directly in the top-level binary strings.

---

### 3️⃣ Extract the PyInstaller archive

**Install and run `pyinstxtractor.py`:**

```bash
# clone the extractor (if you don't already have it)
git clone https://github.com/extremecoders-re/pyinstxtractor.git
cd pyinstxtractor

# run the extractor using Python 2 (recommended)
python3 pyinstxtractor.py passwords.exe
```

Example output:

```text
[+] Processing passwords.exe
[+] Pyinstaller version: 2.1+
[+] Python version: 2.7
[+] Length of package: 3188825 bytes
[+] Found 18 files in CArchive
[+] Beginning extraction...please standby
[+] Possible entry point: pyiboot01_bootstrap.pyc
[+] Possible entry point: passwords.pyc
[!] Please run this script in Python 2.7 to prevent extraction errors during unmarshalling
[!] Skipping pyz extraction
[+] Successfully extracted pyinstaller archive: passwords.exe
```

**Explanation:** PyInstaller packages Python `.pyc` files and resources into the executable. `pyinstxtractor` extracts those embedded files into a directory (`passwords.exe_extracted`), exposing `.pyc` files like `passwords.pyc`.

---

### 4️⃣ Inspect extracted files

Run:

```bash
cd passwords.exe_extracted
ls 
```

Sample output (relevant parts):

```text
bz2.pyd                      passwords.pyc
_hashlib.pyd                 pyiboot01_bootstrap.pyc
Microsoft.VC90.CRT.manifest  pyimod01_os_path.pyc
msvcm90.dll                  pyimod02_archive.pyc
msvcp90.dll                  pyimod03_importers.pyc
msvcr90.dll                  python27.dll
out00-PYZ.pyz                select.pyd
out00-PYZ.pyz_extracted      struct.pyc
passwords.exe.manifest       unicodedata.pyd
```

**Explanation:** The extracted folder contains helper modules, binary python extensions, and most importantly `passwords.pyc` — the compiled Python bytecode for the vault.

---

### 5️⃣ Look for strings in the `.pyc`

Run a strings dump and search for likely identifiers or the contest name:

```bash
strings passwords.pyc 
# or inspect full output
strings passwords.pyc | less
```

Relevant output (excerpt):

```text
GHn3
GHx+
GHqY
Zuck3rb3rg_is_dr34my
Facebook
SwiftOnSecurity15l1f3
Twitter
I_Before_E_Except_After_C
sun{py1n574ll3r_15n7_50urc3_pr073c710n}
SunshineCTF
Welcome to my super secret password vault!
...
```

**Explanation:** The compiled `.pyc` still contains string constants used by the program. `strings` can reveal the flag if it was embedded as a literal string in the source.

---

### 6️⃣ Flag

From the `strings` output above we directly see the flag:

```text
sun{py1n574ll3r_15n7_50urc3_pr073c710n}
```
