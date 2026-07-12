import json
nb = json.load(open(r"D:\coding projects\Spotify-Trends-Analysis\notebooks\exploration.ipynb"))
print(f"Cells: {len(nb['cells'])}")
types = [c['cell_type'] for c in nb['cells']]
print(f"Markdown: {types.count('markdown')}, Code: {types.count('code')}")
