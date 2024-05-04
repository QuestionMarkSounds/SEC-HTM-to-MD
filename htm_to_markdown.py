from markdownify import markdownify as md
import re
from markdownify import MarkdownConverter

class ConvertDiv(MarkdownConverter):
    """
    Create a custom MarkdownConverter that ignores paragraphs
    """
    def convert_div(self, el, text, convert_as_inline):
        return text+'\n'

# Create shorthand method for conversion
def md(html, **options):
    return ConvertDiv(**options).convert(html)


with open('aapl-20230930.html', 'r') as f:
    html_text = f.read()

# rePrompt = '(?!<div id=\".+\">).(?=<\/div>\n)'
# html_text = re.sub(rePrompt, "><h1>Header</h1>", html_text)

markdown_text = md(html_text)

with open('sample.md', 'w', encoding="utf-8") as f:
    f.write(markdown_text)