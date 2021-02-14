import math

calt = int(input("Cruise altitude\n>"))
lalt = int(input("Landing elevation\n>"))

td = math.ceil(((calt-lalt)/1000)*3)

print("T/D Distance: " + str(td))
print("Landing elevation: " + str(lalt))
