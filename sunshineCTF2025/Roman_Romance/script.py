f = open("enc.txt", "r")
data = f.read()
f.close()

new_text = ""
for c in data:
    new_text += chr(ord(c) - 1)

print(new_text)
