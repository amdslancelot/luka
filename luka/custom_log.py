import os
import json
import logging.config
import pathlib

dir_path = os.path.dirname(os.path.realpath(__file__))

def get_logger(logger_name, desired_log_path=dir_path, log_config_path=dir_path+"/logging.json", default_level=logging.INFO):
    """ Use this function to import log"""
    
    if os.path.exists(log_config_path):
        with open(log_config_path, 'rt') as f:
            config = json.load(f)

        # add absolut path for log files
        pathlib.Path(desired_log_path+"/log").mkdir(parents=True, exist_ok=True)
        config["handlers"]["info_file_handler"]["filename"] = \
            desired_log_path + "/" + config["handlers"]["info_file_handler"]["filename"]
        config["handlers"]["debug_file_handler"]["filename"] = \
            desired_log_path + "/" + config["handlers"]["debug_file_handler"]["filename"]
        config["handlers"]["error_file_handler"]["filename"] = \
            desired_log_path + "/" + config["handlers"]["error_file_handler"]["filename"]

        logging.config.dictConfig(config)
        #print "log config", path, "loadded!"
    else:
        logging.basicConfig(level=default_level)
        print("Luka is using basic log config")
    return logging.getLogger(logger_name)
