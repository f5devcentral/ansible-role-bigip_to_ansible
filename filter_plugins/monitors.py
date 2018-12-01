#!/usr/bin/python

import re


def monitors_list(monitors):
    if monitors is None or len(monitors) == 0:
        return []
    try:
        result = re.findall(r'/\w+/[^\s}]+', monitors)
        result.sort()
        return result
    except Exception:
        return monitors


class FilterModule(object):
    def filters(self):
        return {
            'monitors_list': monitors_list
        }
