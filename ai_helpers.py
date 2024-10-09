from langchain_core.output_parsers import StrOutputParser



class MarkdownOutputParser(StrOutputParser):
    def parse(self, text):
        # Preserve the original text, including Markdown formatting
        return text