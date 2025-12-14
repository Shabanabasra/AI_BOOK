#!/usr/bin/env python3
"""
Simple Markdown to HTML converter for AI Book chapters
"""
import os
import re

def markdown_to_html(md_content):
    """Convert markdown content to HTML"""
    html = md_content

    # Convert headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # Convert bold text
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)

    # Convert code blocks
    html = re.sub(r'```bash\n(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)

    # Convert inline code
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)

    # Convert lists
    html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
    html = re.sub(r'</ul>\s*<ul>', r'', html)
    html = re.sub(r'(<ul>.*?</ul>)', lambda m: m.group(0).replace('</li>\n<ul>', '</li>').replace('<ul><li>', '<ul>\n<li>'), html)

    # Handle numbered lists
    html = re.sub(r'^\d+\.\s*(.*?)$', r'<li class="numbered">\1</li>', html, flags=re.MULTILINE)

    # Convert paragraphs
    lines = html.split('\n')
    result = []
    in_list = False
    in_code = False

    for line in lines:
        stripped = line.strip()

        if line.startswith('<pre>') or line.startswith('```'):
            in_code = not in_code
            result.append(line)
            continue

        if in_code:
            result.append(line)
            continue

        if stripped.startswith('<ul>') or stripped.startswith('<li>'):
            if not in_list:
                result.append('<ul>')
            in_list = True
            result.append(line)
        elif stripped == '':
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append('<br>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(f'<p>{line}</p>')

    html = '\n'.join(result)

    # Clean up multiple line breaks
    html = re.sub(r'<br>\s*<br>', r'<br>', html)

    return html

def create_html_page(title, content, prev_chapter=None, next_chapter=None):
    """Create a complete HTML page"""
    nav_links = ""
    if prev_chapter or next_chapter:
        nav_links = '<div class="chapter-nav">'
        if prev_chapter:
            nav_links += f'<a href="{prev_chapter[0]}">&laquo; Previous: {prev_chapter[1]}</a>'
        else:
            nav_links += '<span></span>'
        if next_chapter:
            nav_links += f'<a href="{next_chapter[0]}">Next: {next_chapter[1]} &raquo;</a>'
        nav_links += '</div>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AI Book</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>AI Book: Physical AI and Robotics</h1>
    </header>

    <nav>
        <a href="index.html">Table of Contents</a>
        <a href="01-Introduction-Physical-AI.html">Chapter 1</a>
        <a href="02-Basics-Humanoid-Robotics.html">Chapter 2</a>
        <a href="03-ROS2-Fundamentals.html">Chapter 3</a>
        <a href="04-Digital-Twin-Simulation.html">Chapter 4</a>
        <a href="05-AI-in-Robotics-Applications.html">Chapter 5</a>
        <a href="06-Future-Trends-in-Physical-AI.html">Chapter 6</a>
    </nav>

    <div class="container">
        {content}
        {nav_links}
    </div>

    <footer>
        <p>AI Book: Physical AI and Robotics - Educational Content</p>
    </footer>
</body>
</html>"""
    return html

def main():
    chapters_dir = "../chapters"
    output_dir = "."

    # Define chapters in order
    chapters = [
        ("01-Introduction-Physical-AI.md", "01-Introduction-Physical-AI.html", "Introduction to Physical AI"),
        ("02-Basics-Humanoid-Robotics.md", "02-Basics-Humanoid-Robotics.html", "Basics of Humanoid Robotics"),
        ("03-ROS2-Fundamentals.md", "03-ROS2-Fundamentals.html", "ROS 2 Fundamentals"),
        ("04-Digital-Twin-Simulation.md", "04-Digital-Twin-Simulation.html", "Digital Twin Simulation"),
        ("05-AI-in-Robotics-Applications.md", "05-AI-in-Robotics-Applications.html", "AI in Robotics Applications"),
        ("06-Future-Trends-in-Physical-AI.md", "06-Future-Trends-in-Physical-AI.html", "Future Trends in Physical AI")
    ]

    # Read and convert each chapter
    for i, (md_file, html_file, title) in enumerate(chapters):
        md_path = os.path.join(chapters_dir, md_file)

        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert markdown to HTML
        html_content = markdown_to_html(md_content)

        # Add special styling for specific sections
        html_content = html_content.replace('<h2>Learning Objectives</h2>', '<h2>Learning Objectives</h2><div class="learning-objectives">')
        html_content = html_content.replace('<h2>Key Concepts</h2>', '</div><h2>Key Concepts</h2><div class="key-concept">')
        html_content = html_content.replace('<h2>Hands-on Examples / Exercises</h2>', '</div><h2>Hands-on Examples / Exercises</h2><div class="exercise-box">')
        html_content = html_content.replace('<h2>Summary / Key Takeaways</h2>', '</div><h2>Summary / Key Takeaways</h2><div class="summary-box">')
        html_content = html_content.replace('<h2>Discussion / Thought Exercises</h2>', '</div><h2>Discussion / Thought Exercises</h2><div class="exercise-box">')

        # Add navigation links
        prev_chapter = None
        next_chapter = None

        if i > 0:
            prev_chapter = (chapters[i-1][1], chapters[i-1][2])
        if i < len(chapters) - 1:
            next_chapter = (chapters[i+1][1], chapters[i+1][2])

        # Create complete HTML page
        full_html = create_html_page(title, html_content, prev_chapter, next_chapter)

        # Write HTML file
        output_path = os.path.join(output_dir, html_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

        print(f"Converted {md_file} to {html_file}")

    # Create index.html (Table of Contents)
    toc_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Table of Contents - AI Book</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>AI Book: Physical AI and Robotics</h1>
        <p>Table of Contents</p>
    </header>

    <nav>
        <a href="index.html">Table of Contents</a>
        <a href="01-Introduction-Physical-AI.html">Chapter 1</a>
        <a href="02-Basics-Humanoid-Robotics.html">Chapter 2</a>
        <a href="03-ROS2-Fundamentals.html">Chapter 3</a>
        <a href="04-Digital-Twin-Simulation.html">Chapter 4</a>
        <a href="05-AI-in-Robotics-Applications.html">Chapter 5</a>
        <a href="06-Future-Trends-in-Physical-AI.html">Chapter 6</a>
    </nav>

    <div class="container">
        <div class="toc">
            <h1>Table of Contents</h1>
            <ul>
                <li><a href="01-Introduction-Physical-AI.html">Chapter 1: Introduction to Physical AI</a></li>
                <li><a href="02-Basics-Humanoid-Robotics.html">Chapter 2: Basics of Humanoid Robotics</a></li>
                <li><a href="03-ROS2-Fundamentals.html">Chapter 3: ROS 2 Fundamentals</a></li>
                <li><a href="04-Digital-Twin-Simulation.html">Chapter 4: Digital Twin Simulation</a></li>
                <li><a href="05-AI-in-Robotics-Applications.html">Chapter 5: AI in Robotics Applications</a></li>
                <li><a href="06-Future-Trends-in-Physical-AI.html">Chapter 6: Future Trends in Physical AI</a></li>
            </ul>
        </div>

        <h2>About This Book</h2>
        <p>This AI Book covers the fundamentals of Physical AI and Robotics, from basic concepts to advanced applications. Each chapter includes learning objectives, key concepts, hands-on exercises, and summaries to help you understand and apply these technologies.</p>

        <h2>How to Use This Book</h2>
        <p>You can read the chapters in sequence to build your knowledge progressively, or jump to specific topics that interest you. Each chapter is designed to be self-contained while building on concepts from previous chapters.</p>
    </div>

    <footer>
        <p>AI Book: Physical AI and Robotics - Educational Content</p>
    </footer>
</body>
</html>"""

    with open(os.path.join(output_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(toc_html)

    print("Created index.html (Table of Contents)")
    print("All conversions completed successfully!")

if __name__ == "__main__":
    main()