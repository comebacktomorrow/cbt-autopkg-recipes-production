#!/usr/bin/python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for SynologyURLProvider class"""

import json
import re
import urllib.request, urllib.error, urllib.parse

from distutils.version import LooseVersion, StrictVersion
from operator import itemgetter
from pprint import pprint

from autopkglib import Processor, ProcessorError, URLGetter

__all__ = ["SynologyURLProvider"]

DOWNLOADS_URL = "https://www.synology.com/api/support/findDownloadInfo?lang=en-global&product=RS2416%2B"

class SynologyURLProvider(URLGetter):
    """Provides a version and dmg download for the Barebones product given."""
    description = __doc__
    input_variables = {
    }
    output_variables = {
        "url": {
            "description": "Download URL.",
        },
    }


    def get_downloads_metadata(self):
        '''Return a deserialized json object from the BM downloads metadata.'''
        metadata = self.download(DOWNLOADS_URL)
        json_data = json.loads(metadata)
        self.output("Loading metadata")
        #self.output(json.dumps(json_data))
        return json_data

    def main(self):
        '''Find the download URL'''

        def compare_version(this, that):
            '''compare LooseVersions'''
            return cmp(LooseVersion(this), LooseVersion(that))

        metadata = self.get_downloads_metadata()

        # build our own list of matching products, filtering on criteria:
        # - relatedProductOverride element must contain our 'product_name'
        #   (this name gets POSTed back to request the download URL)
        # - name element must match our 'product_name_pattern' regex

        prods = []
        
        #self.output(json.dumps(metadata["info"]["utilities"]))
        self.output("Searching")
        
        for m_prod in metadata["info"]["utilities"]:
            self.output(m_prod)
            
            search_string = "Synology Drive Client"
            #match = re.search(self.env["product_name_pattern"], m_prod["name"])
            match = re.search(search_string, m_prod["dname"])
            self.output("Attempting to match        " + m_prod["dname"])
            self.output(match)
            if match:
                self.output("Found match        " + m_prod["dname"])
                
                #major = m_prod["urls"]["Mac OS X"][0]["major"]
                #minor = m_prod["urls"]["Mac OS X"][0]["minor"]
                #releaseNum = m_prod["urls"]["Mac OS X"][0]["releaseNum"]
                #version_string = str(major) + "." + str(minor) + "." + str(releaseNum)
                #self.output("Version String is " + version_string)
                
                #if not major and minor and releaseNum:
                #    self.output("WARNING: Regex matched but no "
                #                "named group 'version' matched!")
                p = m_prod.copy()
                
                # recording the version extracted by our named group in
                # 'product_name_pattern'
                #p["version"] = version_string
                #prods.append(p)
            else:
                self.output("No match")
        latest_prod = p
        
        
        self.output("this is the data we are working with")
        #self.output(json.dumps(latest_prod)) #full data
        self.output(json.dumps(latest_prod["files"]["Mac"][0]["url"]))
        self.output(json.dumps(latest_prod["descr"]))
        version_string = re.search(r'(?:SynologyDriveClient\/)(([01234567890\.\-])*)', latest_prod["files"]["Mac"][0]["url"]).group(1)
        #version_string = re.search(r'SynologyDriveClient', latest_prod["files"]["Mac"][0]["url"])
        self.output(version_string)
        

        
        self.env["version"] = version_string
        self.env["url"] = latest_prod["files"]["Mac"][0]["url"]
        self.env["description"] = latest_prod["descr"]
        self.output("Found download URL for %s, version %s: %s" %
                    (self.env["product_name"],
                    self.env["version"],
                    self.env["url"]))


if __name__ == "__main__":
    PROCESSOR = BlackMagicURLProvider()
    PROCESSOR.execute_shell()