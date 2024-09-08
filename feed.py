import yaml
import xml.etree.ElementTree as xml_tree

def create_element(parent, tag, text=None, attrib=None):
    """Helper function to create an XML element with optional text and attributes."""
    elem = xml_tree.SubElement(parent, tag, attrib if attrib else {})
    if text:
        elem.text = text
    return elem

def main():
    # Load YAML data
    try:
        with open('feed.yaml', 'r') as file:
            yaml_data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(f"Error loading YAML: {e}")
        exit(1)

    # Create XML elements
    rss_element = xml_tree.Element('rss', {
        'version': '2.0',
        'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
    })

    channel_element = create_element(rss_element, 'channel')

    link_prefix = yaml_data.get('link', '')

    create_element(channel_element, 'title', yaml_data.get('title', ''))
    create_element(channel_element, 'format', yaml_data.get('format', ''))
    create_element(channel_element, 'subtitle', yaml_data.get('subtitle', ''))
    create_element(channel_element, 'itunes:author', yaml_data.get('author', ''))
    create_element(channel_element, 'description', yaml_data.get('description', ''))
    create_element(channel_element, 'itunes:image', None, {'href': link_prefix + yaml_data.get('image', '')})
    create_element(channel_element, 'language', yaml_data.get('language', ''))
    create_element(channel_element, 'link', link_prefix)

    category = yaml_data.get('category', {})
    if isinstance(category, dict):
        category_element = create_element(channel_element, 'itunes:category', category.get('main', ''))
        subcategory = category.get('subcategory', '')
        if subcategory:
            create_element(category_element, 'itunes:category', subcategory)
    else:
        create_element(channel_element, 'itunes:category', category)

    for item in yaml_data.get('item', []):
        item_element = create_element(channel_element, 'item')
        create_element(item_element, 'title', item.get('title', ''))
        create_element(item_element, 'itunes:author', yaml_data.get('author', ''))
        create_element(item_element, 'description', item.get('description', ''))
        create_element(item_element, 'itunes:duration', item.get('duration', ''))
        create_element(item_element, 'pubDate', item.get('published', ''))

        create_element(item_element, 'enclosure', None, {
            'url': link_prefix + item.get('file', ''),
            'type': 'audio/mpeg',
            'length': item.get('length', '0')
        })

    # Write XML to file
    output_tree = xml_tree.ElementTree(rss_element)
    output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)

if __name__ == "__main__":
    main()
