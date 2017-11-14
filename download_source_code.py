#!/usr/bin/env python

import json
import boto3
import requests
import zipfile
import os
import io
from urllib.parse import urljoin
from functools import reduce

def download_source_code(repo_slug,ssm_name):
    '''
        this function will:
        - acquire Github token from parameter store
        - go to github repo to download
          source code as a zip file to this Lambda box
        - unzip the file and save unzipped file to local box
    '''
    print("downloading source code...")

    # get ssm api tokens
    try:
        token = _get_github_api_token(ssm_name)
    except IndexError:
        raise IndexError("unable to get token")
    _download_code(token,repo_slug)
    print("all done...")

def _get_github_api_token(ssm_name):
    """get ssm api_tokens"""
    ssm = boto3.client('ssm',region_name='ap-southeast-2')
    try:
        response = ssm.get_parameter(Name=ssm_name,WithDecryption=True)
    except IndexError:
        print("GitHubApiToken can't be located")
        raise IndexError
    try:
        token = response["Parameter"]["Value"]
    except IndexError:
        raise IndexError("token can't be found a ssm response, sorry")
    return token

def _unzip_zip_object(file_obj,dest="."):
    """
        given a valid ZIP object, write it into a zipfile then unpack it to a
        destination location, default: 'current location'
    """
    # https://code.tutsplus.com/tutorials/compressing-and-extracting-files-in-python--cms-26816
    try:
        with zipfile.ZipFile(file_obj) as z:
            z.extractall(dest)
    except Exception as e:
        print(e)

def _download_code(token,repo_slug=""):
    """
        download code from github
        ref: 'GET /repos/:owner/:repo/:archive_format/:ref'
    """
    github_api = "https://api.github.com"
    owner = "MYOB-Technology"
    archive_format = "zipball"
    repo_slug = repo_slug
    ref = "master"
    s3_path = ""
    auth_header={}
    auth_header["Authorization"] = "token {}".format(token)
    url_join_items = [
            'repos',
            owner,
            repo_slug,
            archive_format,
            ref
        ]
    relative_url = reduce(os.path.join, url_join_items)
    url = urljoin(github_api,relative_url)
    headers = {""}
    resp = requests.head(url, headers=auth_header, allow_redirects=True)
    file_obj = io.BytesIO(requests.get(resp.url).content)
    _unzip_zip_object(file_obj)

if __name__ == '__main__':
    download_source_code("songjin-deleteme-bk-test","/ops/bk/github-api-token")
