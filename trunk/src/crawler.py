import os.path
from xgoogle.BeautifulSoup import BeautifulSoup
import os, urllib2
#
# This file is part of fimap.
#
# Copyright(c) 2009 Iman Karim.
# http://fimap.googlecode.com
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#


__author__="imax"
__date__ ="$09.09.2009 21:52:30$"

class crawler():

    def __init__(self, config):
        self.goodTypes = ("html", "php", "php4", "php5", "jsp", "htm", "py", "pl", "asp", "cgi", "/")
        self.config = config
        self.urlpool = []
        

    def crawl(self):
        root_url = self.config["p_url"]
        outfile = open(self.config["p_write"], "a")


        idx = 0
        print "[%d] Going to root URL: '%s'..." %(idx, root_url)
        self.crawl_url(root_url)

        
        while(len(self.urlpool)-idx > 0):
            url = self.urlpool[idx]
            outfile.write(url + "\n")
            print "[Done: %d | Todo: %d] Going for next URL: '%s'..." %(idx, len(self.urlpool) - idx, url)
            self.crawl_url(url)
            idx = idx +1

        print "Harvesting done."
        outfile.close()

    def crawl_url(self, url):
        code = self.__simpleGetRequest(url)
        domain = "http://" + self.getDomain(url)

        if (code != None):
            soup = None
            
            try:
                soup = BeautifulSoup(code)
            except UnicodeEncodeError, err:
                pass

            if soup != None:
                for tag in soup.findAll('a'):
                    isCool = False
                    new_url = None
                    try:
                        new_url = tag['href']
                    except KeyError, err:
                        pass

                    if new_url != None and not new_url.startswith("#"):
                        if(new_url.startswith("http://") or new_url.startswith("https://")):
                            if (new_url.lower().startswith(domain.lower())):
                                isCool = True
                        else:
                            new_url = os.path.join(url, new_url)
                            isCool = True

                        if (isCool and new_url in self.urlpool):
                            isCool = False

                        if (isCool):
                            tmpUrl = new_url
                            if (tmpUrl.find("?") != -1):
                                tmpUrl = tmpUrl[:tmpUrl.find("?")]

                            for suffix in self.goodTypes:
                                if (tmpUrl.endswith(suffix)):
                                    self.urlpool.append(new_url)
                                    break


    def __simpleGetRequest(self, URL, TimeOut=10):
        try:
            try:
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', self.config["p_useragent"])]
                f = opener.open(URL, timeout=TimeOut) # TIMEOUT
                return(f.read())
            except TypeError, err:
                try:
                    # Python 2.5 compatiblity
                    socket.setdefaulttimeout(TimeOut)
                    f = opener.open(URL)
                    return(f.read())
                except Exception, err:
                    raise
            except:
                raise

        except Exception, err:
            print "Failed to to request to '%s'" %(Exception)
            print err
            return(None)

    def getDomain(self, url=None):
        if url==None:
            url = self.URL

        domain = url[url.find("//")+2:]
        domain = domain[:domain.find("/")]
        return(domain)