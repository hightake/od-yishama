"""Inline every image the HIGHTAKE presentation uses, so the HTML works as one file."""
import base64, json, re, pathlib
here = pathlib.Path(__file__).parent
s = (here / 'index.html').read_text(encoding='utf-8')
MIME = {'.png': 'image/png', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.webp': 'image/webp'}
def uri(rel):
    p = here / rel
    return 'data:%s;base64,%s' % (MIME[p.suffix], base64.b64encode(p.read_bytes()).decode())
s = re.sub(r'src="(img/[^"\']+)"', lambda m: 'src="%s"' % uri(m.group(1)), s)
logos = json.loads(re.search(r'const LOGOS = (\[.*?\]);', s).group(1))
s = s.replace(re.search(r'const LOGOS = \[.*?\];', s).group(0), 'const LOGOS = ' + json.dumps([uri('img/logos/' + f) for f in logos]) + ';')
s = s.replace("src=\"img/logos/' + f + '\"", "src=\"' + f + '\"")
(here / 'hightake-presentation.html').write_text(s, encoding='utf-8')
print('ok', len(s) // 1024, 'KB', 'img/' in s.replace('data:image', ''))
