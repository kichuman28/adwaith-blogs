import os
import markdown

# Paths
POSTS_DIR = "posts"
OUTPUT_DIR = "output"
TEMPLATE_FILE = "template.html"
STYLE_FILE = "style.css"
COLORS_FILE = "colors.css"

# Read HTML template for individual posts
with open(TEMPLATE_FILE, 'r') as f:
    template = f.read()

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Copy CSS files to output
for css_file in [STYLE_FILE, COLORS_FILE]:
    if os.path.exists(css_file):
        with open(css_file, 'r') as f:
            css = f.read()
        with open(os.path.join(OUTPUT_DIR, css_file), 'w') as f:
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
    if lines and lines[0] == "---":
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

    # Apply template for post
    final_html = template.replace("{{ title }}", title)\
                         .replace("{{ date }}", date)\
                         .replace("{{ content }}", html_content)

    # Write post to output
    output_filename = filename.replace(".md", ".html")
    with open(os.path.join(OUTPUT_DIR, output_filename), 'w') as f:
        f.write(final_html)

    # Collect for index
    index_entries.append((date, title, output_filename))

# Sort entries by date descending
index_entries.sort(reverse=True)

# Generate new homepage layout
index_html = """<!DOCTYPE html>
<html>
<head>
  <title>Adwaith's Blog</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="container">
    <div class="sidebar">
      <img src="me.jpg" alt="Adwaith's photo">
    </div>
    <div class="main">
      <h1>Hi. My name is Adwaith.</h1>
      <p class="intro">I like to write about random stuff. Feel free to read my thoughts below :)</p>
      <ul>
"""

for date, title, link in index_entries:
    index_html += f"        <li><a href='{link}'>{title}</a> <i>{date}</i></li>\n"

index_html += """      </ul>
    </div>
  </div>
</body>
</html>
"""

# Write homepage
with open(os.path.join(OUTPUT_DIR, "index.html"), 'w') as f:
    f.write(index_html)

print("✅ Blog generated with new homepage in /output")
