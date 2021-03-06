#!/usr/bin/python

#
# Proxy class
# Simple web application for proxying to the web
# Accepts "GET /resource", and returns the content of
#   http://resource. For example, if /gsyc.es is used,
#   it returns the content of http://gsyc.es
#
# Copyright Jesus M. Gonzalez-Barahona 2009
# jgb @ gsyc.es
# SARO and SAT subjects (Universidad Rey Juan Carlos)
# March 2015
#

import webapp
import urllib

class proxyApp (webapp.webApp):
    """Simple web application for proxying to the web."""
    #Diccionario cache["gsyc.es"]
    def ponerhola(self, httpBody):
        pos1 = httpBody.find("<body");
        if (pos1):
            pos2 = httpBody.find(">",pos1)
            addhtml = httpBody[:(pos2+1)] + " HOLA " + httpBody[(pos2+1):] 
            return addhtml

    def ponerurlpropia(self, httpBody, urlpropia):
        pos1 = httpBody.find("<body");
        if (pos1):
            pos2 = httpBody.find(">",pos1)
            addhtml = httpBody[:(pos2+1)] + "<a href='" + urlpropia + "'>url propia</a>" + httpBody[(pos2+1):] 
            return addhtml

    def recargarurl(self, httpBody, parsedRequest):
        pos1 = httpBody.find("<body")
        if (pos1):
            pos2 = httpBody.find(">",pos1)
            addhtml = httpBody[:(pos2+1)] + "<a href='" + "http://localhost:1234/" + parsedRequest +"'>recargar-</a>" + "<br>" + httpBody[(pos2+1):] 
            return addhtml

	def guardarcache(self, parsedRequest):
	    pos1 = parsedRequest.find(".")
        if (pos1):
	        info = parsedRequest[:pos1]
	        self.cache[info] = "<a href='http://" + parsedRequest + "'>'http://'" + parsedRequest + "</a>"

    def parse (self, request):
        """Return the resource name (/ removed)"""

        return request.split(' ',2)[1][1:]


    def process (self, resourceName):
        """Process the relevant elements of the request.
        """

        try:
            urlpropia = "http://" + resourceName
            f = urllib.urlopen (urlpropia)
            httpBody = f.read()
            httpCode = "200 OK"
            webHola = self.ponerhola(httpBody)
            ponerurlpropia = self.ponerurlpropia(httpBody,urlpropia)
            recargaurl = self.recargarurl(httpBody, resourceName)
            guardarencache = self.guardarcache(resourceName)
            return ("200 OK", "<html><body><h1>" + recargaurl + "</h1></body></html>")
        except IOError:
            httpBody = "Error: could not connect"
            httpCode = "404 Resource Not Available"
        return (httpCode, httpBody)


if __name__ == "__main__":
    testProxyApp = proxyApp ("localhost", 1234)
