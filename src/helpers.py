from xml.dom.minidom import parseString

from dicttoxml import dicttoxml
from flask_api.renderers import BaseRenderer


def normalise_duration(periodType, timeToElapse):
    if periodType == "days":
        return timeToElapse
    elif periodType == "weeks":
        return timeToElapse * 7
    else:
        return timeToElapse * 30


class XMLRenderer(BaseRenderer):
    media_type = "application/xml"

    def render(self, data, media_type, **options):
        return parseString(dicttoxml(data, attr_type=False)).toprettyxml()


def open_log_file():
    try:
        with open("src/logs.txt", "r+") as f:
            logs = f.read()
        return logs
    except IOError:
        return None


def elapsed_ms(old, now):

    diff = now - old
    ms = (diff.seconds * 1000) + (diff.microseconds / 1000)

    return ms
