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
            html_string.append(f"  {input_item.replace(' ', '_').replace('-', '_')}[{input_item}] --> {output.replace(' ', '_').replace('-', '_')}[{output}]")
            nodes.update([input_item, output])
    html_string.append("") # just empty line between chart and links
    
    # Create click links
    for node in sorted(nodes):
        link = f"{wiki_base}{node}"
        html_string.append(f"""  click {node.replace(' ', '_').replace('-', '_')} "{link.replace(' ', '_').replace('-', '_')}" _blank""")
        
    # Add end part
    html_string.append("""</pre>
</body>
</html>""")
    return "\n".join(html_string)
```

Ant it can be tested with this example
```
components = {
    "Granite Maul": ["Imbued Granite Maul Head", "Ornate Maul Handle", "Imbued Leather Wrappings", "Vault Shard", "Vault Core"],
    "Imbued Granite Maul Head": ["Granite", "Wild Anima", "Vault Shard"],
    "Wild Anima": ["Anima-Infused Bark"],
    "Vault Shard": ["Dragonkin Vault"],
    "Ornate Maul Handle": ["Blightwood","Silver Bar","Bronze Bar","Vault Shard"],
    "Silver Bar": ["Silver Ore"],
    "Bronze Bar": ["Copper Ore","Tin Ore"],
    "Imbued Leather Wrappings": ["Dire Wolf Leather", "Anima-Infused Bark","Vault Shard"],
    "Dire Wolf Leather": ["Dire Wolf Hide"]
}

print(generate_mermaid_with_links(components))
```
