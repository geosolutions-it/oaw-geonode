from geonode.layers.metadata import set_metadata
from owslib.etree import etree
from geonode.layers.metadata import convert_keyword
from datetime import datetime
from geonode.base.models import HierarchicalKeyword


def xml_parser(xml, uuid="", vals={}, regions=[], keywords=[], custom={}):
    try:
        uuid, vals, regions, keywords, custom = set_metadata(xml, uuid, vals, regions, keywords, custom)
    except:
        vals, keywords, custom = custom_parsing(xml, vals, keywords)
    return uuid, vals, regions, keywords, custom


def custom_parsing(xml, vals, keywords):
    exml = etree.fromstring(xml.encode())
    date = (
        datetime.strftime(datetime.strptime(exml.find("date").text, "%Y"), "%Y-%m-%d")
        if not exml.find("date")
        else None
    )
    vals = {
        "title": exml.find("title").text if exml.find("title") is not None else None,
        "date": date or datetime.now(),
        "edition": exml.find("edition").text if exml.find("edition") is not None else None,
        "abstract": exml.find("abstract").text if exml.find("abstract") is not None else None,
        "purpose": exml.find("purpose").text if exml.find("purpose") is not None else None,
        "supplemental_information": exml.find("supplemental_information").text
        if exml.find("supplemental_information") is not None
        else None,
        "data_quality_statement": exml.find("data_quality_statement").text
        if exml.find("data_quality_statement") is not None
        else None,
        "typename": exml.find("typename").text if exml.find("typename") is not None else None,
    }

    kws = []
    for kw in exml.findall("keywords"):
        kws = [k.text for k in kw.findall("item")]

    '''
    Check if the keywords extracted from the XML are available in GeoNode.
    If the keyword is not available in GeoNode, is ignored
    '''
    valid_keywords = ['GeoTiff']

    for k in kws:
        is_available = HierarchicalKeyword.objects.filter(name=k).exists()
        if is_available:
            valid_keywords.append(k)

    keywords = convert_keyword(valid_keywords or [])
    return vals, keywords, keywords


def storer(layer, custom):
    '''
    Set as invalid all the keywords assigned to the layer that are not available in
    the keywords extracted from the XML.
    Deleting the Keywords that are invalid, since we want to have a specific
    set of keywords in GeoNode. The keywords automatically generated are deleted
    '''
    for lk in layer.keywords.all():
        if not lk.name in custom[0]['keywords']:
            k = HierarchicalKeyword.objects.get(name=lk.name)
            k.delete()

    return layer
