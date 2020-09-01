"""
Bash Config Reader
"""
import logging
import luka.utils as utils
import luka.custom_log as mylog
logger = mylog.get_logger("Luka Config Reader")

def read_bash_config(fname):
    """ Read bash config and return """

    config = None

    try:
        with open(fname, 'r') as config_file:
            config = {}
            for line in config_file:
                # Get rid of \n
                line = line.rstrip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue
                (name, value) = line.split("=")
                name = name.strip().replace("\"", "")
                config[name] = value.replace("\"", "")
    except:
        err_msg = "Failed to open file: %s. Please check if oauth file exists" % (fname)
        logger.error(err_msg)
        utils.print_common_error(err_msg)
        exit(0)
    return config
