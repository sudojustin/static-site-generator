def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    raise ValueError('No H1 header found in the markdown.')

