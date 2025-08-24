import os
import markdown
from datetime import datetime

# Paths
POSTS_DIR = "posts"
OUTPUT_DIR = "output"
TEMPLATE_FILE = "template.html"
STYLE_FILE = "style.css"

# Read HTML template
with open(TEMPLATE_FILE, 'r') as f:
    template = f.read()

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Copy CSS to output
with open(STYLE_FILE, 'r') as f:
    css = f.read()
with open(os.path.join(OUTPUT_DIR, 'style.css'), 'w') as f:
    f.write(css)

# Store metadata for homepage
index_entries = []

# Loop through Markdown posts
for filename in os.listdir(POSTS_DIR):
    if not filename.endswith(".md"):
        continue

    filepath = os.path.join(POSTS_DIR, filename)
    with open(filepath, 'r') as f:
        lines = f.read().splitlines()

    # Extract frontmatter
    if lines[0] == "---":
        title = ""
        date = ""
        content_start = 0
        for i, line in enumerate(lines[1:], start=1):
            if line.startswith("title:"):
                title = line.split("title:")[1].strip()
            elif line.startswith("date:"):
                date = line.split("date:")[1].strip()
            elif line == "---":
                content_start = i + 1
                break
        content_md = "\n".join(lines[content_start:])
    else:
        title = filename.replace(".md", "")
        date = ""
        content_md = "\n".join(lines)

    html_content = markdown.markdown(content_md)

    # Apply template
    final_html = template.replace("{{ title }}", title)\
                         .replace("{{ date }}", date)\
                         .replace("{{ content }}", html_content)

    # Write to output
    output_filename = filename.replace(".md", ".html")
    with open(os.path.join(OUTPUT_DIR, output_filename), 'w') as f:
        f.write(final_html)

    # Collect for index
    index_entries.append((date, title, output_filename))

# Sort entries by date descending
index_entries.sort(reverse=True)

# Generate index.html
index_html = "<!DOCTYPE html><html><head><title>My Essays</title><link rel='stylesheet' href='style.css'></head><body>"
index_html += "<h1>My Essays</h1><ul>"

for date, title, link in index_entries:
    index_html += f"<li><a href='{link}'>{title}</a> <i>{date}</i></li>"

index_html += "</ul></body></html>"

with open(os.path.join(OUTPUT_DIR, "index.html"), 'w') as f:
    f.write(index_html)

print("✅ Blog generated in /output")
