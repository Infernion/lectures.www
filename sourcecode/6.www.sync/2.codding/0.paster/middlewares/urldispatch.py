#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Example from Ian Bicking WSGI presantation.
"""
import re


class URLDispatch(object):

    def __init__(self, app_list):
        self.app_list = app_list

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        for prefix, app in self.app_list:
            if path_info in [prefix, prefix + '/']:
                return app(environ, start_response)
        start_response('404 Not Found',
                       [('content-type', 'text/plain')])
        return ['not found']


class RegexDispatch(object):

    def __init__(self, app_list):
        self.app_list = app_list

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        for prefix, app in self.app_list:
            if path_info in [prefix, prefix + '/']:
                return app(environ, start_response)
            match = re.match(prefix, path_info) or\
                re.match(prefix, path_info+'/')
            if match and match.groupdict():
                environ['url_params'] = match.groupdict()
                return app(environ, start_response)
        start_response('404 Not Found', [('content-type', 'text/plain')])
        return ['not found']
