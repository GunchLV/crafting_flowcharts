Depository for crafting flow charts
HTML files can be accesed by using --> https://gunchlv.github.io/crafting_flowcharts/DW_Abyssal_Whip.html and editing end part

Here is python function i am using to generate html
```
def generate_mermaid_with_links(components, title="Crafting Chart", wiki_base="https://dragonwilds.runescape.wiki/w/", chart_direction='BT'):
    html_string = ["""<!DOCTYPE html>
<html>
<head>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
  </script>
</head>
<body>"""]
    html_string.append(f"""  <h2>{title}</h2>
<pre class="mermaid">
graph {chart_direction}""")
    
    nodes = set()
    links = []

    for output, inputs in components.items():
        for input_item in inputs:
            # Connection
            html_string.append(f"  {input_item}[{input_item.replace('_', ' ')}] --> {output}[{output.replace('_', ' ')}]")
            nodes.update([input_item, output])
    html_string.append("") # just empty line between chart and links
    
    # Create click links
    for node in sorted(nodes):
        link = f"{wiki_base}{node}"
        html_string.append(f'  click {node} "{link}" _blank')
        
    # Add end part
    html_string.append("""</pre>
</body>
</html>""")
    return "\n".join(html_string)
```

Ant it can be tested with this example
```
components = {
    "Whip": ["Vault_Core", "Vault_Shard", "Horn", "Hard_Leather", "Abyssal_Spine"],
    "Vault_Core": ["Dragonkin_Vault"],
    "Vault_Shard": ["Dragonkin_Vault"],
    "Horn": ["Ram"],
    "Hard_Leather": ["Leather", "Adhesive"],
    "Leather": ["Animal_Hide"],
    "Adhesive": ["Swamp_Tar"],
    "Abyssal_Spine": ["Abyssal_Demon"]
}

print(generate_mermaid_with_links(components))
```
