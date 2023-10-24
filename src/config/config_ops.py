import xml.etree.ElementTree as ET
from pathlib import Path

class ConfigError(Exception):
    pass

def make_config(args, config_path = 'config.xml'):
    """
    Generate config with key, value pairs from args

    Parameters
    ----------
    args : array(dictrionary)
        Key, value pairs
    config_path : str
        Path to config
    """
    root = ET.Element('config')
    tree = ET.ElementTree(root)
    for k, v in args.items():
        set_key(k, v, tree)
    tree.write(config_path, encoding='UTF-8', xml_declaration=True)

def add_key(key, value, tree):
    """
    Add key, value pair to tree

    skip if key already exist

    Parameters
    ----------
    key : str
        Tree node name
    value : str
        Tree node value
    tree : xml.etree.ElementTree
        Modified tree
    """
    root = tree.getroot()
    elem = root.find(key)
    if elem is None:
        elem = ET.SubElement(root, key)
        elem.text = value

def set_key(key, value, tree):
    """
    Set key, value pair in tree

    Create new node if such node not found

    Parameters
    ----------
    key : str
        Tree node name
    value : str
        Tree node value
    tree : xml.etree.ElementTree
        Modified tree
    """
    root = tree.getroot()
    elem = root.find(key)
    if elem is None:
        elem = ET.SubElement(root, key)
    elem.text = value

def load_config(config_path = 'config.xml'):
    """
    Load config from file

    Parameters
    ----------
    config_path : str
    
    Raises
    ------
    ConfigError
        If invalid config file
    OSError
        If file cannot be opened
    """
    with open(config_path) as f:
        data = f.read()
        try:
            root = ET.fromstring(data)
        except ET.ParseError as e:
            raise ConfigError('invalid config file: %s' % e)

        config = {}

        for elem in root.findall('./*'):
            config[elem.tag] = elem.text
        return config