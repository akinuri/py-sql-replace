from pprint import pprint
import re
import urllib.parse
from tools import *

user_args = {
    "input" : {
        "sql"       : "test.sql",
        "url"       : "http://111.22.333.44/~user",
        "public"    : "home/%username%/domains/%domain%/public_html",
    },
    "output" : {
        "sql"       : "test_replaced.sql",
        "url"       : "http://example.com",
        "public"    : "home/%username%/domains/%domain%/public_html",
    },
}

file_path = user_args["input"]["sql"]

file = open(file_path, "r", encoding="utf-8")
lines = file.readlines()
content = "".join(lines)

input_url  = user_args["input"]["url"]
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
input_dict["serialized"]["domain"]      = urllib.parse.urlparse(input_url).netloc
input_dict["normal"]["path"]            = user_args["input"]["public"]

output_url = user_args["output"]["url"]
output_dict = {
    "serialized" : {
        "url" : output_url,
    },
    "normal" : {
        "url" : output_url,
    },
}
output_dict["normal"]["dbl_escaped_fs"] = output_url.replace("/", r"\\/")
output_dict["normal"]["encoded"]        = urllib.parse.quote(output_url, safe="")
output_dict["normal"]["encoded_tilde"]  = urllib.parse.quote(output_url, safe="").replace("~", "%7E")
output_dict["normal"]["dbl_encoded"]    = urllib.parse.quote(urllib.parse.quote(output_url, safe=""), safe="")
output_dict["normal"]["url_wo_schema"]  = re.sub("https?://", "", output_url)
output_dict["normal"]["domain"]         = urllib.parse.urlparse(output_url).netloc
output_dict["serialized"]["domain"]     = urllib.parse.urlparse(output_url).netloc
output_dict["normal"]["path"]           = user_args["output"]["public"]

content = re.sub("content ?: ?\\\\\"(.*?)\\\\\"", r"content: \'\1\'", content)

content = replace_serialized(content, input_dict["serialized"]["url"], output_dict["serialized"]["url"])
content = replace_serialized(content, input_dict["serialized"]["domain"], output_dict["serialized"]["domain"])

content = content.replace(input_dict["normal"]["url"], output_dict["normal"]["url"])
content = content.replace(input_dict["normal"]["dbl_escaped_fs"], output_dict["normal"]["dbl_escaped_fs"])
content = content.replace(input_dict["normal"]["encoded"], output_dict["normal"]["encoded"])
content = content.replace(input_dict["normal"]["encoded_tilde"], output_dict["normal"]["encoded_tilde"])
content = content.replace(input_dict["normal"]["dbl_encoded"], output_dict["normal"]["dbl_encoded"])
content = content.replace(input_dict["normal"]["url_wo_schema"], output_dict["normal"]["url_wo_schema"])
content = content.replace(input_dict["normal"]["domain"], output_dict["normal"]["domain"])
if output_dict["normal"]["path"] != input_dict["normal"]["path"]:
    content = content.replace(input_dict["normal"]["path"], output_dict["normal"]["path"])

output_file = open(user_args["output"]["sql"], "w", encoding="utf-8")
output_file.write(content)
output_file.close()

print("Done")
input()
