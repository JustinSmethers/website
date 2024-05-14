## TODO
add documentation

## Utility Scripts

### Generating Syntax Highlighting CSS

I'm using Pygments for syntax highlighting in our application. The CSS required for this is generated using the Python script located at `scripts/generate_pygments_css.py`. To regenerate the CSS (e.g., to change styles or update Pygments), run the following command:

```bash
python scripts/generate_pygments_css.py
