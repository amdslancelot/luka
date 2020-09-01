import re
import pprint
import logging
import json
import luka.custom_log as mylog

""" logging """
logger = mylog.get_logger("Luka Utils")

# pprint
pp = pprint.PrettyPrinter(indent=4)



def append_url(url_str1, url_str2):
    return url_str1 + "/" + url_str2


# Printer
def print_error(args, msg="Unknown error"):
    """ Use this function to print all error msgs """

    logger.error(args)
    logger.error(msg)
    print("[ERROR]", msg)


def print_common_error(msg):
    print("[ERROR]", msg)


def print_result(r, pp=True):
    """ Use this function to print all results """

    if r is None:
        print("[ERROR]", "request failed.")
    else:
        logger.info("result: %s" % (pp.pformat(json.dumps(r))))
        if pp:
            print(json.dumps(r, indent=4))
        else:
            print(pp.pformat(json.dumps(r)))
