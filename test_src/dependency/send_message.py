# -*- coding:utf-8 -*-

'''
Send message to WebSocket client
'''

import json
import logging
import constants

# Init logger
logger = logging.getLogger(constants.LOGGER_CLIENT_MAIN)

RPL_SENDER      = "sender"
RPL_STATUS      = "status"
RPL_TESTID      = "test_id"
RPL_CASEID      = "case_id"
RPL_DESC        = "description"
RPL_DATA        = "data"
RPL_DATA_NAME   = "data_name"

RPL_STATUS_OK              = "200"
RPL_STATUS_MESSAGE_ERROR   = "300"
RPL_STATUS_STATUS_ERROR    = "301"
RPL_STATUS_DOWNLOAD_ERROR  = "302"
RPL_STATUS_COMMAND_ERROR   = "303"
RPL_STATUS_SERVER_ERROR    = "400"

def response_message(test_id, case_id, status, description="", sender="vm"):
    message = {}
    message[RPL_SENDER] = sender
    message[RPL_STATUS] = status
    message[RPL_TESTID] = test_id
    message[RPL_CASEID] = case_id
    message[RPL_DESC]   = description
    json_message = json.dumps(message)
    logger.info(json_message)
    return json_message

def data_message(test_id, case_id, data_name, data, sender, description="data"):
    message = {}
    message[RPL_SENDER]     = sender
    message[RPL_DATA]       = data
    message[RPL_TESTID]     = test_id
    message[RPL_CASEID]     = case_id
    message[RPL_DESC]       = description
    message[RPL_DATA_NAME]  = data_name
    json_message = json.dumps(message)
    #logger.debug(json_message)
    return json_message

def send_message(request, message):
    try:
        request.ws_stream.send_message(message)
    except:
        logger.error('send message error: %s' % (message))
