#!/usr/bin/env python3
import httpx
import json
from pprint import pprint
import time
import datetime
import sys
from param import *
from common import *


def main():
    resp = httpx.request(method="get",url=f'{BASE_URL}/api/content', headers=HEADERS)
    for i in param.contents:
        resp = httpx.request(method="post",url=f'{BASE_URL}/api/content', headers=HEADERS, json=i)
        print_resp(resp=resp, allow_error=True)






if __name__ == "__main__":
    main()