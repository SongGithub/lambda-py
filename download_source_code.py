#!/usr/bin/env python

import json
import boto3
import requests
import zipfile
import os
import io
import urllib.parse as urljoin

def download_source_code(repo_slug, ssm_keyname):
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
        token = _get_github_api_token()
    except IndexError:
        raise IndexError("unable to get token")
    _download_code(token,"songjin-deleteme-bk-test")
    print("all done...")

def _get_github_api_token():
    """get ssm api_tokens"""
    ssm = boto3.client('ssm',region_name='ap-southeast-2')
    try:
        response = ssm.get_parameters(Names=["GitHubApiToken"],WithDecryption=True)
    except IndexError:
        print("GitHubApiToken can't be located")
        raise IndexError
    try:
        token = response["Parameters"][0]["Value"]
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
    # finally:
    #     os.remove("downloaded.zip")

def _download_code(token,repo_slug=""):
    """
        download code from github
            input: api_token, repo_slug
            output: a folder in nominated S3 bucket
        ref: 'GET /repos/:owner/:repo/:archive_format/:ref'
    """
    github_api = "https://api.github.com"
    owner = "MYOB-Technology"
    archive_format = "zipball"
    ref = "master"
    s3_path = ""
    auth_header={}
    auth_header["Authorization"] = "token {}".format(token)

    # url = "{}/repos/{}/{}/{}/{}" \
    # .format(
    #     github_api,
    #     owner,
    #     repo_slug,
    #     archive_format,
    #     ref)

    url = urljoin(
        github_api,
        owner,
        repo_slug,
        archive_format,
        ref)
    print(url)
    headers = {""}
    resp = requests.head(url, headers=auth_header, allow_redirects=True)
    file_obj = io.BytesIO(requests.get(resp_url).content)
    _unzip_zip_object(file_obj)

if __name__ == '__main__':
    download_source_code('abcrepo', 'blah key')
