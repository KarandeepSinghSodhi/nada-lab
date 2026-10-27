import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect pipeline start and end
pipe_start = html.find('<section id="pipeline" class="chapter pipeline-chapter">')
shrutis_start = html.find('<section id="shrutis" class="chapter list-chapter">')

if pipe_start == -1 or shrutis_start == -1:
    print("Could not find pipeline or shrutis boundaries")
    exit(1)

print(f"Found pipeline from index {pipe_start} to {shrutis_start}")
