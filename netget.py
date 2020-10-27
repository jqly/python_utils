import os
import sys
import json
import socket
import urllib.request
import base64
from distutils.dir_util import copy_tree
import zipfile
import tempfile
import logging


logger = logging.getLogger(__name__)

def retry_on_timeout(fn):
    def fn_with_retry(*args, **kwargs):
        max_retry = 5
        for __ in range(max_retry-1):
            try:
                return fn(*args, **kwargs)
            except urllib.error.URLError as err:
                if isinstance(err.reason, TimeoutError):
                    logger.debug('TimeoutError occured, retrying...')
                    continue
                else:
                    raise
        return fn(*args, **kwargs)
    return fn_with_retry

def http_basic_auth_credential(auth):
    cred = ('%s:%s' % auth).encode('ascii')
    cred = base64.b64encode(cred)
    cred = cred.decode("ascii")
    return cred

def url_request(url, auth=None):
    req = urllib.request.Request(url)
    if auth:
        req.add_header('Authorization', 
            'Basic %s' % http_basic_auth_credential(auth))
    return req

@retry_on_timeout
def get_zip_and_extract(url, save_to, auth=None, skip_first_folder=True):
    save_to = os.path.abspath(save_to)
    zip_name = 'temp.zip'
    logger.debug('downloading from %s...' % url)

    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor())
    req = url_request(url, auth)
    with opener.open(req) as zip_src:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_zip_path = os.path.join(temp_dir, zip_name)
            logger.debug('saving to temporary location %s...' 
                % temp_zip_path)
            with open(temp_zip_path, 'wb') as fp:
                fp.write(zip_src.read())
            with zipfile.ZipFile(temp_zip_path) as zf:
                if skip_first_folder:
                    member_name = zf.namelist()[0].strip('/')
                    logger.debug('extracting only %s to %s...' 
                        % (member_name, save_to))
                    zf.extractall(path=temp_dir)
                    member_path = os.path.join(temp_dir, member_name)
                    copy_tree(member_path, save_to)
                else:
                    logger.debug('extracting to %s...' % save_to)
                    zf.extractall(path=save_to)

@retry_on_timeout
def get_json(url, auth=None):
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor())
    req = url_request(url, auth)
    with opener.open(req) as s:
        html = s.read()
        return json.loads(html)

if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stdout, 
        level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # zip_url = 'an url required simple auth'
    # get_zip_and_extract(zip_url, '.\\q', ('xxxxx', 'xxxxx'), False)
    zip_url = 'https://github.com/jqly/python_utils/archive/main.zip'
    get_zip_and_extract(zip_url, '.\\q')