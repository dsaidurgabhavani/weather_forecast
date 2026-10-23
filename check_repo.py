import re

with open("repo_page.html", encoding="utf-8") as f:
    html = f.read()

branches = re.findall(r'"ref_name":"([^"]+)"', html)
print("Branches in ref_name:", set(branches))

commits = re.findall(r'commit/([a-f0-9]{7,40})', html)
print("Recent commit hashes:", commits[:3])
