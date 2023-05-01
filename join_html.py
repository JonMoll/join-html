import re

def replace(line, regex_path, tag_start, tag_end):
    regex_indent = r'^\s*<'
    num_spaces = re.search(regex_indent, line).group()
    num_spaces = len(num_spaces) - 1
    indent_outside = ' ' * num_spaces
    indent_inside = ' ' * 2

    if tag_start is None or tag_end is None:
        indent_inside = ''

    path = re.search(regex_path, line).group(1)
    with open(path, 'r') as f:
        lines_file = f.readlines()

    lines_file = [f'{indent_outside}{indent_inside}{l}' for l in lines_file]

    if tag_start is not None and tag_end is not None:
        lines_file = [f'{indent_outside}{tag_start}\n'] + lines_file
        lines_file = lines_file + [f'{indent_outside}{tag_end}\n']

    comment = f'<!-- start: "{path}" -->'
    lines_file = [f'{indent_outside}{comment}\n'] + lines_file
    comment = f'<!-- end: "{path}" -->'
    lines_file = lines_file + [f'{indent_outside}{comment}\n']

    lines_file = ''.join(lines_file)

    return lines_file

patterns = {
    'style': {
        'regex_tag': r'^\s*<link\s+rel="stylesheet"\s+href="\.[^"]*">\s*$',
        'regex_path': r'href="(.+)"',
        'tag_start': '<style type="text/css">',
        'tag_end': '</style>',
    },
    'script': {
        'regex_tag': r'^\s*<script\s+type="text\/javascript"\s+src="\.[^"]*"><\/script>\s*$',
        'regex_path': r'src="(.+)"',
        'tag_start': '<script type="text/javascript">',
        'tag_end': '</script>',
    },
    'html': {
        'regex_tag': r'^\s*<object\s+type="text\/html"\s+data="\.[^"]*"><\/object>\s*$',
        'regex_path': r'data="(.+)"',
        'tag_start': None,
        'tag_end': None,
    },
}

path = './index.html'
with open(path, 'r') as f:
    lines_html = f.readlines()

for i, line in enumerate(lines_html):
    for group in patterns:
        regex_tag = patterns[group]['regex_tag']
        regex_path = patterns[group]['regex_path']
        tag_start = patterns[group]['tag_start']
        tag_end = patterns[group]['tag_end']

        if re.match(regex_tag, line):
            lines_file = replace(line, regex_path, tag_start, tag_end)
            lines_html[i] = lines_file

path = './app.html'
with open(path, 'w') as f:
    for line in lines_html:
        f.write(line)
