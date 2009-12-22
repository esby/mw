###
# mw - VCS-like nonsense for MediaWiki websites
# Copyright (C) 2009  Ian Weller <ian@ianweller.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
###

import cookielib
import gzip
import json
from StringIO import StringIO
import urllib
import urllib2


class API(object):

    def __init__(self, api_url):
        self.api_url = api_url
        self.cookiejar = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
                urllib2.HTTPCookieProcessor(self.cookiejar))
        self._high_limits = None

    def call(self, data):
        data['format'] = 'json'
        request = urllib2.Request(self.api_url, urllib.urlencode(data))
        request.add_header('Accept-encoding', 'gzip')
        response = self.opener.open(request)
        if response.headers.get('Content-Encoding') == 'gzip':
            compressed = StringIO(response.read())
            gzipper = gzip.GzipFile(fileobj=compressed)
            data = gzipper.read()
        else:
            data = response.read()
        return json.loads(data)

    def limits(self, low, high):
        if self._high_limits == None:
            result = self.call({'action': 'query',
                                'meta': 'userinfo',
                                'uiprop': 'rights'})
            self._high_limits = 'apihighlimits' in \
                    result['query']['userinfo']['rights']
        if self._high_limits:
            return high
        else:
            return low


def pagename_to_filename(name):
    name = name.replace(' ', '_')
    name = name.replace('/', '!')
    return name


def filename_to_pagename(name):
    name = name.replace('!', '/')
    name = name.replace('_', ' ')
    return name
