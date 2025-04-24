import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import webbrowser
import os
import time
import tkinter as tk
from tkinter import messagebox

def scrape_item_components(full_url):
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

def generate_html_code(components, title="Crafting Chart", wiki_base="https://dragonwilds.runescape.wiki/w/", chart_direction="BT", node_colour="#e7e7e7"):
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
    
    def str_replace(text): # to fix problems that would crash html part
        return text.replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')

    for output, inputs in components.items():
        for input_item in inputs:
            # Connection
            html_string.append(f"  {str_replace(input_item)}[{input_item.replace('(', '').replace(')', '')}] --> {str_replace(output)}[{output.replace('(', '').replace(')', '')}]")
            nodes.update([input_item, output])
    html_string.append("") # just empty line between chart and links
    
    # Create click links
    for node in sorted(nodes):
        link = f"{wiki_base}{node}"
        html_string.append(f"""  click {str_replace(node)} "{str_replace(link)}" _blank""")
    
    # Custom html color code for nodes
    for node in sorted(nodes):
        html_string.append(f"""  style {str_replace(node)} fill:{node_colour} """)
        
    # Add end part
    html_string.append("""</pre>
</body>
</html>""")
    # return dict of recipe ingredients and item name from web adress end part
    return "\n".join(html_string)

def generate_html_file(html_content, item_name, show_result=True, generate_html_file=True):
    
    # Save HTML content to a file
    file_path = f"""{item_name}.html"""
    with open(file_path, "w") as f:
        f.write(html_content)
    
    if show_result==True: # Open the file in the default web browser
        webbrowser.open('file://' + os.path.realpath(file_path))
    
    # Wait a little while to ensure the browser has enough time to load the page
    time.sleep(2)
    
    if generate_html_file==False: # Delete the file after the page is opened
        if os.path.exists(file_path):
            os.remove(file_path)
            

# GUI setup
def main():

    root = tk.Tk()
    root.title("Crafting Flowchart Generator")
    
    # URL entry
    tk.Label(root, text="Enter URL:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    url_entry = tk.Entry(root, width=60)
    url_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=3, sticky='w')
    
    # Create a frame for the options row
    options_frame = tk.Frame(root)
    options_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky='w')
    
    # Checkboxes
    show_result_var = tk.BooleanVar(value=True)
    gen_html_file_var = tk.BooleanVar(value=True)
    
    show_result_cb = tk.Checkbutton(options_frame, text="Show result", variable=show_result_var)
    show_result_cb.pack(side='left', padx=5)
    
    gen_html_file_cb = tk.Checkbutton(options_frame, text="Generate .html file", variable=gen_html_file_var)
    gen_html_file_cb.pack(side='left', padx=5)
    
    # Node colour input
    tk.Label(options_frame, text="Node colour:").pack(side='left', padx=5)
    node_colour_entry = tk.Entry(options_frame, width=20)
    node_colour_entry.pack(side='left', padx=5)
    node_colour_entry.insert(0, "#e7e7e7") # Default node colour

    # Generate button
    def on_generate():
        full_url = url_entry.get()
        if not full_url:
            messagebox.showerror("Error", "Please enter a URL.")
            return
        final_product_name = full_url.split('/')[-1].replace("_"," ").replace("%27","'")
        wiki_base = full_url.split('/w/')[0]+"/w/"
        components = scrape_item_components(full_url)
        html_code = generate_html_code(components, f'''Crafting Chart for "{final_product_name}"''', wiki_base=wiki_base, node_colour=node_colour_entry.get())
        generate_html_file(html_code, final_product_name, show_result=show_result_var.get(), generate_html_file=gen_html_file_var.get())

    generate_btn = tk.Button(root, text="Generate", command=on_generate)
    generate_btn.grid(row=2, column=1, columnspan=2, pady=15)

    root.mainloop()

if __name__ == "__main__":
    main()
