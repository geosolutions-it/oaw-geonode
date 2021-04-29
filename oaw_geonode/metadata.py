from geonode.layers.metadata import set_metadata
from owslib.etree import etree
from geonode.layers.metadata import convert_keyword
from datetime import datetime


def xml_parser(xml, uuid="", vals={}, regions=[], keywords=[], custom={}):
    try:
        set_metadata(xml, uuid, vals, regions, keywords, custom)
    except:
        vals, keywords = custom_parsing(xml, vals, keywords)
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
    keywords = convert_keyword(kws or [])
    return vals, keywords
