##############################################################################
# Copyright (c) 2003 Zope Corporation and Contributors.
# All Rights Reserved.
# 
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
##############################################################################
"""HTTP method OPTIONS

$Id$
"""
__metaclass__ = type

_allowed_methods = ['PUT', 'DELETE', 'CONNECT', \
           'OPTIONS', 'PATCH', 'PROPFIND', 'PROPPATCH', 'MKCOL', \
           'COPY', 'MOVE', 'LOCK', 'UNLOCK', 'TRACE']
           # XXX 'GET', 'HEAD', 'POST' are always available?

from zope.component import queryView

class OPTIONS:
    """OPTIONS handler for all objects
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def OPTIONS(self):
        allowed = ['GET', 'HEAD', 'POST']
        for m in _allowed_methods:
            view = queryView(self.context, m, self.request, None)
            if view is not None:
                allowed.append(m)

        self.request.response.setHeader('Allow', ', '.join(allowed))
        # XXX Most of the time, this is a lie. We not fully support
        # DAV 2 on all objects, so probably an interface check is needed.
        self.request.response.setHeader('DAV', '1,2', literal=True)
        # XXX UGLY! Some clients rely on this. eg: MacOS X
        self.request.response.setHeader('MS-Author-Via', 'DAV', literal=True)
        self.request.response.setStatus(200)
        return ''

