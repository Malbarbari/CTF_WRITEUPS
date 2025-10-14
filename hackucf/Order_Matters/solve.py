hex_values = ["58335249","58306c45","b5a314e66","63335675",
              "58335177","51563969","4e484a45","66513d3d",
              "4d313935","59544578","4d313943","4d486c7a",
              "6532315a","5831526f","556a4675"]

for h in hex_values:
    if len(h) % 2: 
        continue
    print(bytes.fromhex(h).decode('utf-8', errors='ignore'))
