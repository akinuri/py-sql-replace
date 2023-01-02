from tools import *

file_path = "test.sql"

file = open(file_path, "r", encoding="utf-8")
lines = file.readlines()
content = "".join(lines)

input_url  = "http://111.22.333.44/~user"

serialized = find_serialized(content, input_url)
dump_list(serialized, "\n" + ("-" * 100) + "\n")

print( "" )
print( "Serialized strings: " + str(len(serialized)) )
print( "" )

input()
