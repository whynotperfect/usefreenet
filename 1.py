import base64, json, urllib.parse

def create_config(b, v):
    s, _, d = b.partition('://')
    if s.lower() == 'vmess':
        c = json.loads(base64.b64decode(d))
        c['host' if c['port'] == 80 else 'sni'] = v
        if c['port'] == 443: c['tlsSettings'] = c.get('tlsSettings', {'allowInsecure': True})
        return s + '://' + base64.b64encode(json.dumps(c).encode()).decode()
    elif s.lower() == 'vless':
        u = urllib.parse.urlparse(b)
        n, p = u.netloc.rsplit(':', 1)
        q = urllib.parse.parse_qs(u.query, True)
        q['host' if int(p) == 80 else 'sni'] = v
        if int(p) == 443: q['allowInsecure'] = '1'
        return urllib.parse.urlunparse((s, n + ':' + p, u.path, u.params, urllib.parse.urlencode(q, True), u.fragment))
    else: raise ValueError("Unsupported configuration scheme")

with open('range.txt') as f, open('output.txt', 'w') as o:
    for l in f:
        v = l.strip()
        if v: o.write(create_config(input().strip(), v) + '\n')