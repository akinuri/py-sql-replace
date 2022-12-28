from pprint import pprint
import re
import urllib.parse
from tools import *

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

print("Done")
input()
