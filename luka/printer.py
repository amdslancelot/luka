import re
import pprint
import logging
import json
import luka.log as mylog

""" logging """
logger = mylog.get_logger("Utils")

# pprint
pp = pprint.PrettyPrinter(indent=4)



def append_url(url_str1, url_str2):
    return url_str1 + "/" + url_str2


# Printer
def print_error(*args, user_args=None, msg="Unknown error"):
    """ Use this function to print all error msgs """

    if user_args:
        logger.error(user_args)
    logger.error(msg)
    print("[ERROR]", msg, *args)


def print_text_error(msg):
    print("[ERROR]", msg)


def print_json_result(r, is_pp=True):
    """ Use this function to print all results """

    if r is None:
        print("[ERROR]", "request failed.")
    else:
        logger.info("result: %s" % (pp.pformat(json.dumps(r))))
        if is_pp:
            print(json.dumps(r, indent=4))
        else:
            print(pp.pformat(json.dumps(r)))
