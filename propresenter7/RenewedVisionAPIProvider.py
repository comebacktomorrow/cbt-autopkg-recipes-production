#!/usr/bin/python
#
# Copyright 2013 Timothy Sutton
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
"""See docstring for RenewedVisionAPIProvider class"""

import ssl
import json

from autopkglib import ProcessorError
from autopkglib.URLGetter import URLGetter

__all__ = ["RenewedVisionAPIProvider"]


class RenewedVisionAPIProvider(URLGetter):
    """Provides a version and dmg download for the Barebones product given."""
    print("next phase")
    description = __doc__
    input_variables = {
    #    "product_name": {
    #        "required": True,
    #        "description": "Product to fetch URL for. ProPresenter.",
    #    }
    }
    output_variables = {
        "version": {"description": "Version of the product."},
        "url": {"description": "Download URL."},
        "build_number": {"description": "Build Number"},
        "release_date": {"description": "Date and time of release"},
        "release_notes": {"description": "Changes of release"},
        "minimum_os_version": {
            "description": "Minimum OS version supported according to product metadata."
        },
    }

    def main(self):
        """Find the download URL"""
        url = 'https://api.renewedvision.com/v1/pro/upgrade?platform=macos&osVersion=10.16&appVersion=7.4&buildNumber=000&includeNotes=true'
        res_body = self.download(url)
        api_response = json.loads(res_body.decode("utf-8"))

        self.env["version"] = api_response['upgrades'][0]['version']
        self.env["minimum_os_version"] = api_response['upgrades'][0]['minOSVersion']
        self.env["url"] = api_response['upgrades'][0]['downloadUrl']
        self.env["build_number"] = api_response['upgrades'][0]['buildNumber']
        self.env["release_date"] = api_response['upgrades'][0]['releaseDate']
        self.env["release_notes"] = api_response['releaseNotes']
        self.output("Found URL %s" % self.env["url"])

if __name__ == "__main__":
    PROCESSOR = RenewedVisionAPIProvider()
    PROCESSOR.execute_shell()