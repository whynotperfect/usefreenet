import base64
import json
import urllib.parse

def create_config(base_config, new_value):
    scheme, _, data = base_config.partition('://')
    if scheme.lower() == 'vmess':
        config = json.loads(base64.b64decode(data))
        if config['port'] == 80:
            config['host'] = new_value
        elif config['port'] == 443:
            config['sni'] = new_value
            config['tlsSettings'] = config.get('tlsSettings', {})
            config['tlsSettings']['allowInsecure'] = True
        new_config_json = json.dumps(config, ensure_ascii=False).encode('utf-8')
        new_config_base64 = base64.b64encode(new_config_json).decode('utf-8')
        return scheme + '://' + new_config_base64
    elif scheme.lower() == 'vless':
        url = urllib.parse.urlparse(base_config)
        netloc, port = url.netloc.rsplit(':', 1)
        port = int(port)
        query = urllib.parse.parse_qs(url.query, keep_blank_values=True)
        if port == 80:
            query['host'] = new_value
        elif port == 443:
            query['sni'] = new_value
            query['allowInsecure'] = '1'
        new_query = urllib.parse.urlencode(query, doseq=True)
        new_url = urllib.parse.urlunparse((scheme, netloc + ':' + str(port), url.path, url.params, new_query, url.fragment))
        return new_url
    else:
        raise ValueError("Unsupported configuration scheme")

range_file_name = 'range.txt'
output_file_name = 'output.txt'

user_input = input('Введите конфигурацию (в формате vmess://... или vless://...): ').strip()

with open(range_file_name, 'r') as range_file, open(output_file_name, 'w') as output_file:
    for line in range_file:
        new_value = line.strip()
        if new_value:
            try:
                new_config = create_config(user_input, new_value)
                output_file.write(new_config + '\n')
            except ValueError as e:
                print(e)
                break

print('Конфигурации с измененными параметрами записаны в файл output.txt')
