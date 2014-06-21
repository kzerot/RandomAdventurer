__author__ = 'murre'
import json


def safe_loads(raw):
    if '}{' in raw:
        try:
            return [json.loads(t)
                    for t in raw.replace('}{', '}||{').split('||')]
        except:
            print 'failed to parse ', raw
            return []
    else:
        return [json.loads(raw)]