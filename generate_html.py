import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_item(full_url):
    visited = set()
    dependencies = {}

    BASE_URL = full_url.split("/w/")[0]

    def fetch_page(relative_url):
        full_url = urljoin(BASE_URL, relative_url)
        response = requests.get(full_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"})
        response.raise_for_status()
        return response.content

    def recurse(relative_url):
        if relative_url in visited:
            return
        visited.add(relative_url)

        html = fetch_page(relative_url)
        soup = BeautifulSoup(html, "html.parser")

        item_name_tag = soup.find("h1")
        if not item_name_tag:
            return
        item_name = item_name_tag.text.strip()
        ingredients = []

        table = soup.find("table", class_="wikitable")
        if not table:
            return

        rows = table.find_all("tr")
        parsing_materials = False

        for row in rows:
            headers = row.find_all("th")
            if headers and "Material" in headers[0].text:
                parsing_materials = True
                continue
            if parsing_materials:
                cols = row.find_all("td")
                if len(cols) < 2:
                    break
                link_tag = cols[0].find("a")
                if not link_tag:
                    continue
                name = link_tag.get("title", "").strip()
                href = link_tag.get("href", "").strip()
                if name:
                    ingredients.append(name)
                if href and href.startswith("/w/"):
                    recurse(href)

        dependencies[item_name] = ingredients

    # Start the recursion
    start_path = full_url.split("/w/")[1]
    recurse("/w/" + start_path)

    return dependencies

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

# Example usage
components = parse_item("https://dragonwilds.runescape.wiki/w/Chef%27s_Hat")
print(generate_mermaid_with_links(components, '''Crafting Chart for "Chef's Hat"'''))

# Pretty print result
#import pprint
#pprint.pprint(components)
