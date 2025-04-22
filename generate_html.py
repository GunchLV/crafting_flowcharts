def generate_mermaid_with_links(components, title="Crafting Chart", wiki_base="https://dragonwilds.runescape.wiki/w/", chart_direction='BT'):
    """
    This function will generate HTML code with flowchart.
    To get components data use ''material_tables'' function
    """
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

import pandas as pd
from io import StringIO

def material_tables(data):
    """
    This function creats dict of items from all data_string strings, to be used in ''generate_mermaid_with_links'' function.
    Open wiki, select material table starting from ''Material'' to end of table (output result item) anc copy as list element in data_string
    """
    all_components = {}
    for crafting_item in data:
        parts, name = crafting_item.strip().split('Output\tQuantity')
        name = name.strip().split('\t')[0]
        parts = pd.read_csv(StringIO(parts.strip()), sep='\t')
        # print(f'"{name}":' + str(list(parts.iloc[:,0])))
        all_components.update({name:list(parts.iloc[:,0])})
    return all_components

# Example with data strings for "Paladin's Platebody" ----------------------------------------------------------

data_string = ['''
Material	Quantity
Iron Bar	12
Hard Leather	8
Padded Cloth	2
Vault Shard	3
Output	Quantity
Paladin's Platebody	1
''',
'''
Material	Quantity
Iron Ore	3
Output	Quantity
Iron Bar	1
''',
'''
Material	Quantity
Leather	2
Adhesive	1
Output	Quantity
Hard Leather	1
''',
'''
Material	Quantity
Animal Hide	1
Output	Quantity
Leather	1
''',
'''
Material	Quantity
Swamp Tar	1
Output	Quantity
Adhesive	1
''',
'''
Material	Quantity
Rough Cloth	
Wool Cloth	1
Output	Quantity
Padded Cloth	1
''',
'''
Material	Quantity
Coarse Thread	3
Output	Quantity
Rough Cloth	1
''',
'''
Material	Quantity
Wool Thread	2
Output	Quantity
Wool Cloth	1
''',
'''
Material	Quantity
Fleece	1
Output	Quantity
Wool Thread	1
''',
'''
Material	Quantity
Flax	1
Output	Quantity
Coarse Thread	1
''']

components = material_tables(data_string)
print(generate_mermaid_with_links(components))
