from pprint import pprint
import re
import urllib.parse


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


#region ==================== TOOLS

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


#region ==================== APP

file_path = "test.sql"

file = open(file_path, "r", encoding="utf-8")
lines = file.readlines()
content = "".join(lines)

input_url  = "http://111.22.333.44/~user"
input_dict = {
    "serialized" : {
        "url" : input_url,
    },
    "normal" : {
        "url" : input_url,
    },
}
input_dict["normal"]["dbl_escaped_fs"]  = input_url.replace("/", r"\\/")
input_dict["normal"]["encoded"]         = urllib.parse.quote(input_url, safe="")
input_dict["normal"]["encoded_tilde"]   = urllib.parse.quote(input_url, safe="").replace("~", "%7E")
input_dict["normal"]["dbl_encoded"]     = urllib.parse.quote(urllib.parse.quote(input_url, safe=""), safe="")
input_dict["normal"]["url_wo_schema"]   = re.sub("^https?://", "", input_url)
input_dict["normal"]["domain"]          = urllib.parse.urlparse(input_url).netloc
input_dict["normal"]["path"]            = "home/%username%/domains/%domain%/public_html"

output_url = "http://example.com"
output_dict = {
    "serialized" : {
        "url" : output_url,
    },
    "normal" : {
        "url" : output_url,
    },
}
output_dict["normal"]["dbl_escaped_fs"]  = output_url.replace("/", r"\\/")
output_dict["normal"]["encoded"]         = urllib.parse.quote(output_url, safe="")
output_dict["normal"]["encoded_tilde"]   = urllib.parse.quote(output_url, safe="").replace("~", "%7E")
output_dict["normal"]["dbl_encoded"]     = urllib.parse.quote(urllib.parse.quote(output_url, safe=""), safe="")
output_dict["normal"]["url_wo_schema"]   = re.sub("https?://", "", output_url)
output_dict["normal"]["domain"]          = urllib.parse.urlparse(output_url).netloc
output_dict["normal"]["path"]            = "home/%username%/htdocs"

content = re.sub("content ?: ?\\\\\"(.*?)\\\\\"", r"content: \'\1\'", content)

content = replace_serialized(content, input_dict["serialized"]["url"], output_dict["serialized"]["url"])
content = content.replace(input_dict["serialized"]["url"], output_dict["serialized"]["url"])
content = content.replace(input_dict["normal"]["dbl_escaped_fs"], output_dict["normal"]["dbl_escaped_fs"])
content = content.replace(input_dict["normal"]["encoded"], output_dict["normal"]["encoded"])
content = content.replace(input_dict["normal"]["encoded_tilde"], output_dict["normal"]["encoded_tilde"])
content = content.replace(input_dict["normal"]["dbl_encoded"], output_dict["normal"]["dbl_encoded"])
content = content.replace(input_dict["normal"]["url_wo_schema"], output_dict["normal"]["url_wo_schema"])
content = content.replace(input_dict["normal"]["domain"], output_dict["normal"]["domain"])
content = content.replace(input_dict["normal"]["path"], output_dict["normal"]["path"])

output_file = open("output.sql", "w", encoding="utf-8")
output_file.write(content)
output_file.close()

#endregion


print("Done")
input()
