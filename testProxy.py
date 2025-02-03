#!/usr/bin/env python3

import requests

def test_proxy(proxy):
    test_url = "http://www.google.com"
    try:
        response = requests.get(test_url, proxies=proxy, timeout=5)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        return False
    return False