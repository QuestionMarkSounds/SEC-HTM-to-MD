from markdownify import markdownify as md
import re
from markdownify import MarkdownConverter

def sec_to_md_local(ticker="goog"):
    class ConvertDiv(MarkdownConverter):
        """
        Create a custom MarkdownConverter that ignores paragraphs
        """
            
        def convert_div(self, el, text, convert_as_inline):
            return text+'\n'

    # Create shorthand method for conversion
    def md(html, **options):
        return ConvertDiv(**options).convert(html)


    with open(ticker+'.htm', 'r') as f:
        html_text = f.read()

    # rePrompt = '(?!<div id=\".+\">).(?=<\/div>\n)'
    html_text = clean_header_garbage(html_text)

    markdown_text = md(html_text)

    mardown_text = re.sub('http:\/\/fasb.org\/.+\n', "", markdown_text)


    with open(ticker+'.md', 'w', encoding="utf-8") as f:
        f.write(markdown_text)

    return markdown_text

def sec_to_md_file(file):
    class ConvertDiv(MarkdownConverter):
        """
        Create a custom MarkdownConverter that ignores paragraphs
        """
        def convert_div(self, el, text, convert_as_inline):
            return text+'\n'

    # Create shorthand method for conversion
    def md(html, **options):
        return ConvertDiv(**options).convert(html)


    # with open(file, 'r') as f:
    html_text = file.read()
    html_text = clean_header_garbage(html_text.decode("utf-8", errors="ignore"))

    # rePrompt = '(?!<div id=\".+\">).(?=<\/div>\n)'
    # html_text = re.sub(rePrompt, "><h1>Header</h1>", html_text)

    markdown_text = md(html_text)
    markdown_text.replace("\n\n\n", "\n")
    mardown_text = re.sub('http:\/\/fasb.org\/.+\n', "", markdown_text)

    with open('sample.md', 'w', encoding="utf-8") as f:
        f.write(markdown_text)

    return markdown_text

def sec_to_md_from_html(html):
    class ConvertDiv(MarkdownConverter):
        """
        Create a custom MarkdownConverter that ignores paragraphs
        """
        def convert_div(self, el, text, convert_as_inline):
            return text+'\n'

    # Create shorthand method for conversion
    def md(html, **options):
        return ConvertDiv(**options).convert(html)


    # with open(file, 'r') as f:
    html_text = html
    html_text = clean_header_garbage(html_text)

    # rePrompt = '(?!<div id=\".+\">).(?=<\/div>\n)'
    # html_text = re.sub(rePrompt, "><h1>Header</h1>", html_text)

    markdown_text = md(html_text)
    markdown_text.replace("\n\n\n", "\n")
    mardown_text = re.sub('http:\/\/fasb.org\/.+\n', "", markdown_text)

    with open('sample.md', 'w', encoding="utf-8") as f:
        f.write(markdown_text)

    return markdown_text

def sec_to_md_path(file):
    class ConvertDiv(MarkdownConverter):
        """
        Create a custom MarkdownConverter that ignores paragraphs
        """
        def convert_div(self, el, text, convert_as_inline):
            return text+'\n'

    # Create shorthand method for conversion
    def md(html, **options):
        return ConvertDiv(**options).convert(html)


    # with open(file, 'r') as f:
    html_text = file.read()
    html_text = clean_header_garbage(html_text)

    # rePrompt = '(?!<div id=\".+\">).(?=<\/div>\n)'
    # html_text = re.sub(rePrompt, "><h1>Header</h1>", html_text)

    markdown_text = md(html_text)
    markdown_text.replace("\n\n\n", "\n")
    mardown_text = re.sub('http:\/\/fasb.org\/.+\n', "", markdown_text)

    with open('sample.md', 'w', encoding="utf-8") as f:
        f.write(markdown_text)

    return markdown_text

def clean_header_garbage(html_text):
    html_text = re.sub("<ix:header>.+<\/ix:header>", "", html_text)
    return html_text

# sec_to_md_file(ticker="nvda")

