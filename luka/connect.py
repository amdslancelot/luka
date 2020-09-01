import os
import json
import base64
import logging
import requests
import luka.bash_config_reader as config_reader
#import luka.json_byteify as json_byteify
import luka.custom_log as mylog
import luka.utils as utils
import config

class APIRequest(object):
    """ 
    Per URL API request class
    Handle all cases to make RESTful API requests 
    """

    # Class variables (Share by all instances)
    #scope = config["scope"] if config else None
    #clientId = config["clientId"] if config else None
    #clientSecret = config["clientSecret"] if config else None
    #token_fname = config.TOKEN_FNAME
    #identity = None

    def __init__(self, function, url, headers=None):
        
        # logging
        self.logger = mylog.get_logger("Luka Connect")

        self.headers  = headers
        self.function = function
        self.method   = function[0]
        self.url      = url + function[1]
        self.payload  = function[2] if len(function) == 3 else None

        if not self.url or not self.function or not self.method:
            self.logger.error("Initialization failed!")
            self.logger.error("url=" + self.url)
            self.logger.error(self.function)
            exit(1)

        # Instance Variables (varies by all instances)
        self.r_json   = None
        self.r        = None

    def add_token(self, token, token_name="token"):
        self.token    = token
        if "?" not in self.url:
            self.url = self.url + "?" + token_name + "=" + token
        else:
            self.url = self.url + token_name + "=" + token

    def request(self):
        method  = self.method
        url     = self.url
        headers = self.headers
        payload = self.payload

        if method == "GET":
            self.r = self._send_request(lambda: requests.get(
                                                    url, 
                                                    headers=headers, 
                                                    params=payload),
                                        method)
        elif method == "POST":
            # Necessary for POST
            #self.headers["Content-Type"] = "application/x-www-form-urlencoded"
            
            self.r = self._send_request(lambda: requests.post(
                                                    url, 
                                                    headers=headers, 
                                                    data=payload),
                                        method)
        elif method == "PUT":
            self.r = self._send_request(lambda: requests.put(
                                                    url, 
                                                    headers=headers, 
                                                    json=payload),
                                        method)
        else:
            self.logger.error("Do not recognize method! " + method)
            return None
        return self._parse_api_response(method, self.r, payload)
            

    def query(self, url, query):
        """ Query """

        self.logger.info("QUERY")

        if not query:
            self.logger.error("QUERY - query JSON object is empty!")
            return None

        self.logger.debug("QUERY - query=%s", query)

        query_str = None
        try:
          query_str = json.dumps(query)
        except:
          self.logger.error("QUERY - Cannot convert query to json. query=%s", query)
          return None

        self.url = url
        self.logger.info("QUERY - url=%s", self.url)

        self.payload["data"] = '{"query":' + query_str + '}' # This data structure for QUERY only
        self.logger.debug("QUERY - payload=%s", self.payload)
        self.logger.debug("QUERY - headers=%s", self.headers)

        self.r = self._send_request(lambda: requests.get(
                                                self.url, 
                                                headers=self.headers, 
                                                params=self.payload),
                                    "QUERY")
        self.r_json = self._parse_api_response("QUERY", self.r, self.payload)
        if not self.r_json:
            return None
        
        return self.r_json

    def post(self, url, payload):
        """ POST """

        self.logger.info("POST")

        self.url = url
        self.logger.info("POST - url=%s", self.url)
        # Necessary for POST
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        self.logger.debug("POST - headers=%s", self.headers)
        # Have to assign to a variable "data"
        self.payload = "data=" + json.dumps(payload).replace(" ", "")
        self.logger.debug("POST - payload: %s", self.payload)

        self.r = self._send_request(lambda: requests.post(
                                                self.url, 
                                                headers=self.headers, 
                                                data=self.payload),
                                    "POST")
        return self._parse_api_response("POST", self.r, self.payload)
        if not self.r_json:
            return None
        
        return self.r_json


    def put(self, url, payload):
        """ PUT """

        self.logger.info("PUT")

        self.url = url
        self.logger.info("PUT - url=%s", self.url)
        self.payload = payload
        self.logger.debug("PUT - payload: %s", self.payload)
        self.logger.debug("PUT - headers=%s", self.headers)

        self.r = self._send_request(lambda: requests.put(
                                                self.url, 
                                                headers=self.headers, 
                                                json=self.payload),
                                    "PUT")
        self.r_json = self._parse_api_response("PUT", self.r, self.payload)
        if not self.r_json:
            return None
        
        return self.r_json


    def delete(self, url):
        """ DELETE """

        self.logger.info("DELETE")

        self.url = url
        self.logger.info("DELETE - url=%s", self.url)
        self.logger.debug("DELETE - headers=%s", self.headers)

        self.r = self._send_request(lambda: requests.delete(
                                                self.url, 
                                                headers=self.headers),
                                    "DELETE")
        self.r_json =  self._parse_api_response("DELETE", self.r, self.payload)
        if not self.r_json:
            return None
        
        return self.r_json


    def get(self, url, payload=None):
        """ GET """

        self.logger.info("GET")

        self.url = url
        self.logger.info("GET - url=%s", self.url)
        self.payload = payload
        self.logger.debug("GET - payload=%s", self.payload)
        self.logger.debug("GET - headers=%s", self.headers)

        self.r = self._send_request(lambda: requests.get(
                                                self.url, 
                                                headers=self.headers, 
                                                params=self.payload),
                                    "GET")
        self.r_json = self._parse_api_response("GET", self.r, self.payload)
        if not self.r_json:
            return None

        return self.r_json

    def _parse_api_response(self, req_type, r, payload):
        # HTTP level error (HTTP status code != 200)
        if not r:
            self.logger.error("%s - response, r: %s" % (req_type, r))
            self.logger.error("%s - response, status code: %s" % (req_type, r.status_code))
            utils.print_common_error(r)
            return None
        self.logger.debug("%s - response=%s" % (req_type, r.content))

        r_json = self._convert_response_to_json(r.text)
        # API level error
        if not r_json:
            self.logger.error("%s - Do not recognize response format!" % (req_type))
            self.logger.error("%s - response=%s" % (req_type, r.content))
            self.logger.error("%s - payload=%s" % (req_type, payload))
            utils.print_common_error(r.content)
            return None

        # API request successful but task failed
        if not self._check_error_code(r_json, r):
            return None

        return r_json

    def _convert_response_to_json(self, s):
        try:
            return json.loads(s)
            #return json_byteify.json_loads_byteified(s) # Don't need this anymore cause we now use json.dumps for output
        except (TypeError, ValueError) as e:
            self.logger.error(sys.exc_info())
            self.logger.error("The API returns unexpected msg:\n%s", s)

        return None

    def _send_request(self, f, req_type):
        try:
            return f()
        except requests.exceptions.SSLError as e:
            self.logger.error("SSL error when sending request(%s): %s", req_type, str(e))
            return None
        except Exception as e:
            self.logger.error("Unknown error when sending request(%s): %s", req_type, str(e))
            return None

    def _check_error_code(self, r_json, r):
        """ If API request successful but task failed """

        if ("error_code" in r_json and r_json["error_code"] != 1):
            utils.print_common_error(r.content)
            return False
        return True

  
