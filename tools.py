import re

#region ==================== DEBUG

def dump_list(list):
    if len(list) == 0:
        print("[]")
    else:
        print("[")
        for item in list:
            print("  '" + str(item) + "',")
        print("]")

# Mostly for debug/inspection purposes
def find_str(string, substring, before_length=10, after_length=10):
    matches = []
    for occurence in re.finditer(substring, string, flags=re.IGNORECASE):
        capture_before_start_index = max(occurence.start() - abs(before_length), 0)
        capture_before_end_index   = min(occurence.end()   + abs(after_length), len(string))
        capture_before = string[capture_before_start_index:capture_before_start_index+before_length]
        capture_after  = string[occurence.end():capture_before_end_index]
        capture_before = capture_before.replace("\n", " ")
        capture_after  = capture_after.replace("\n", " ")
        matches.append(f'{capture_before} {occurence.group(0)} {capture_after}')
    return matches

#endregion


#region ==================== STRING LENGTH

"""
The main operation revolves around the serialize function of PHP.
https://www.php.net/manual/en/function.serialize.php
"""

# The length of some characters are greater than 1 even though they appear to be a single char
char_lengths = {
    "1" : ["\\r", "\\n", "\\'", "\\\"", "\\\\"],
    "2" : ["ç", "Ç", "ğ", "Ğ", "ı", "İ", "ö", "Ö", "ü", "Ü", "ş", "Ş", "©", "·"],
    "3" : ["•", "“", "”"],
}

# Allows us to get the real length of a string
def flatten_string(str):
    for length in char_lengths:
        chars = char_lengths[length]
        placeholder = "$" * int(length)
        for char in chars:
            str = str.replace(char, placeholder)
    return str

#endregion


#region ==================== SERIALIZE

# Finds and replaces serialized strings, and updates the length field.
def replace_serialized(subject, old_str, new_str):
    pattern_serialized = "s:\\d+:\\\\\"((?:.(?!s:\\d+))*?)" + re.escape(old_str) + "(.*?)\\\\\";"
    subject = re.sub(
        pattern_serialized,
        lambda match: replace_serialized_callback(match, old_str, new_str),
        subject,
    )
    return subject

def replace_serialized_callback(match, old_str, new_str):
    before_str = match.group(1)
    after_str = match.group(2)
    total_length = len(flatten_string(before_str)) + len(new_str) + len(flatten_string(after_str))
    if old_str in after_str:
        offset = len(old_str) - len(new_str)
        occurences = len(re.findall(old_str, after_str))
        displacement = offset * occurences
        total_length -= displacement
        after_str = after_str.replace(old_str, new_str)
    return f"s:{total_length}:\\\"{before_str}{new_str}{after_str}\\\";"

# Mostly for debug/inspection purposes
def find_serialized(subject, search_str):
    pattern_serialized = r"s:\d+:\\\"((?:.(?!s:\d+))*?)" + re.escape(search_str) + "(.*?)\\\";"
    matches = re.finditer(pattern_serialized, subject)
    matches = [match.group(0) for match in matches]
    return matches

#endregion
