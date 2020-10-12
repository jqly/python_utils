import os
import sys
import json
import socket
import urllib.request
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

@retry_on_timeout
def get_zip_and_extract(url, save_to, skip_first_folder=True):
    save_to = os.path.abspath(save_to)
    zip_name = 'temp.zip'
    logger.debug('downloading from %s...' % url)
    with urllib.request.urlopen(url) as zip_src:
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
def get_json(url):
    with urllib.request.urlopen(url) as s:
        html = s.read()
        return json.loads(html)

if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stdout, 
        encoding='utf-8', 
        level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    zip_url = 'https://github.com/jqly/python_utils/archive/main.zip'
    get_zip_and_extract(zip_url, '.\\')
