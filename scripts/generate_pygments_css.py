from pygments.formatters import HtmlFormatter

# Generate CSS for the Pygments style
formatter = HtmlFormatter(style='github-dark')  # Use theme 'github-dark'
css_string = formatter.get_style_defs('.codehilite') # Get the CSS for the 'codehilite' class
print(css_string)

# You might want to save this CSS to a file
with open('blog/static/blog/css/pygments.css', 'w') as f:
    f.write(css_string)