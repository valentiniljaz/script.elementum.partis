# -*- coding: utf-8 -*-

import urllib2
from urllib import urlencode
from cookielib import CookieJar
from parser.ehp import Html
import os

_Partis__NAME = 'Partis'
_Partis__USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36'
_Partis__BASE_URL = 'https://www.partis.si'
_Partis__BASE_URL_INSECURE = 'http://www.partis.si'
_Partis__LOGIN_URL = _Partis__BASE_URL + '/user/login'
_Partis__LOGIN_OK_URL = _Partis__BASE_URL + '/prva'
_Partis__LOGIN_OK_URL_INSECURE = _Partis__BASE_URL_INSECURE + '/prva'
_Partis__SHOW_URL = _Partis__BASE_URL + '/torrent/show'
_Partis__NFO_URL = _Partis__BASE_URL + '/torrent/nfo'
_Partis__SEARCH_URL = _Partis__BASE_URL + '/brskaj'
_Partis__CATEGORIES = { 
    'movies': ['40', '42', '44', '45', '20', '4', '7', '54', '59'], 
    'series': ['51', '52', '53', '38', '60']
}

class _Partis__NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response
    https_response = http_response

class Partis:

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def __request(self, url, params = {}, cookiesIn = {}, headers = {}, data = None, method = None):
        if params:
            url = "".join([url, "?", urlencode(params)])
        
        req = urllib2.Request(url)
        req.get_method = lambda: method

        req.add_header('User-Agent', _Partis__USER_AGENT)
        for k, v in headers.items():
            req.add_header(k, v)

        cookieStr = ''
        for cookie in cookiesIn:
            cookieStr += cookie.name + '=' + cookie.value + ';'

        req.add_header('Cookie', cookieStr)

        if data:
            req.add_data(data)

        cookiesOut = CookieJar()
        opener = urllib2.build_opener(__NoRedirection, urllib2.HTTPCookieProcessor(cookiesOut))
        urllib2.install_opener(opener)
        response = urllib2.urlopen(req)

        return response, cookiesOut

    def __login(self):
        response, cookies = self.__request(_Partis__LOGIN_URL, {}, {}, {}, 'user[username]='+self.__username+'&user[password]='+self.__password, 'POST')
        if response.code == 302:
            redirection_target = response.headers['Location']
            if redirection_target == _Partis__LOGIN_OK_URL  or redirection_target == _Partis__LOGIN_OK_URL_INSECURE:
                return cookies
        raise Exception('Login failed!')

    def search(self, searchTerm, category = None):
        results = []
        # Login
        cookies = self.__login()
        # Prepare cookie string for resolving torrent links
        cookieStr = ''
        for cookie in cookies:
            if cookie.name == 'auth_token' or cookie.name == '_partis16':
                cookieStr += cookie.name+'='+cookie.value+';'
        # First request to /torrent/show, otherwise it forces a redirect
        showResponse, _ = self.__request(_Partis__SHOW_URL, {}, cookies, {}, None, 'GET')
        # Do actual search
        categories = ''
        if category:
            categories = ','.join(_Partis__CATEGORIES[category])
        params = { 'keyword': searchTerm, 'category': categories, 'offset': '0', 'option': '0', 'ns': 'true', 'rnd': '0.' }
        searchResponse, _ = self.__request(_Partis__SEARCH_URL, params, cookies, { 'X-Requested-With': 'XMLHttpRequest' }, None, 'GET')
        # Fix HTML before parsing
        searchHtml = searchResponse.read().replace('/></div>', '></div>')
        # Parse torrents
        searchDom = Html().feed(searchHtml)
        listeks = searchDom.find_all(tag='div', select=('class', 'listek'))
        for listek in listeks:
            # Parse basic info
            tId = listek(tag='div', select=('class', 'likona'), attribute='id')
            listeklink = listek.find_once(tag='div', select=('class', 'listeklink'))
            tName = listeklink(tag='a')
            # Get donwload link
            data3t = listek.find_once(tag='div', select=('class', 'data3t'))
            tDldLink = data3t(tag='a', attribute='href')
            size = listek(tag='div', select=('class', 'datat'), order=1)
            try:
            	seeders = int(listek(tag='div', select=('class', 'datat'), order=2))
            except Exception:
            	seeders = 0
            try:
            	peers = int(listek(tag='div', select=('class', 'datat'), order=3))
            except Exception:
            	peers = 0

            results.append({
                "name": tName,
                "uri": _Partis__BASE_URL+tDldLink+'|Cookie='+cookieStr,
                "info_hash": 'PARTIS_'+tId,
                "size": size,
                "provider": _Partis__NAME,
                "icon": 'logo.png',
                "seeds": seeders,
                "peers": peers,
                "is_private": True,
                "Multi": False
            })

        return results

    def updateIconPath(self, torrents, iconPath):
        for torrent in torrents:
            torrent['icon'] = os.path.join(iconPath,  torrent['icon'])
        return torrents
