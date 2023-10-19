import xml.etree.ElementTree as ET

def make_config(args, config_path = 'config.xml'):
    print(args)
    token = args['token']
    if not token:
        raise ValueError('token must be present')
    root = ET.Element('config')
    tokenElem = ET.SubElement(root, 'token')
    tokenElem.text = token
    tree = ET.ElementTree(root)
    tree.write(config_path, encoding='UTF-8', xml_declaration=True)

def load_token(config_path = 'config.xml'):
    with open(config_path) as f:
        data = f.read()
        tree = ET.fromstring(data)
        token = tree.findtext('token')
        return token