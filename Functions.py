import socket
import threading
import os
import logging
import datetime


def get_datetime():
    '''Returns a dictionary containing the date and time

    dt['time'] - contains current time in hh:mm format(24 hrs)
    dt['date'] - contains current date as dd-mm-yyyy format
    '''
    dt = {}

    now = datetime.datetime.now()
    dt['time'] = now.strftime('%H:%M')
    dt['date'] = now.strftime('%d-%m-%Y')

    return dt

def get_cmd(cmd, cmds_list):
    '''Search the command (cmd), eg. !twitter in the commands list (cmds_list)
    and try to import its module

    The return value is the function that represents the command or None if the
    command doesn't exist or it's not defined properly
    '''
    if cmd not in cmds_list:
        return None

    try: # the command's module needs to be imported from 'cmds/'
        mod = 'cmds.' + cmd
        mod = __import__(mod, globals(), locals(), [cmd])
    except ImportError as e: # inexistent module
        logging.error(err.C_INEXISTENT.format(cmd) + str(e))
        return None

    try:
        # the name of the command is translated into a function's name,
        # then returned
        callable_cmd = getattr(mod, cmd)
    except AttributeError as e:
        # function not defined in module
        logging.error(err.C_INVALID.format(cmd) + str(e))
        return None

    return callable_cmd
	
def run_cmd(sock, executor, to, cmd, arguments):
    '''Create a future object for running a command asynchronously and add a
    callback to send the response of the command back to irc
    '''
    def cb(f):
        try:
            response = f.result()
        except Exception as e: # TODO: raise a specific exception form the cmds
            response = err.C_EXCEPTION.format(cmd.__name__)
            logging.error(e)

        send_response(response, to, sock)

    future = executor.submit(cmd, arguments)
    future.add_done_callback(cb)
	
send_response_lock = threading.Lock()
def send_response(response, destination, s):
    '''Attempt to send the response to destination through the s socket
    The response can be either a list or a string, if it's a list then it
    means that the module sent a command on its own (eg. PART)

    The destination can be passed using the send_to function

    True is returned upon sending the response, None if the response was empty
    or False if an error occurred while sending the response
    '''
    if response is not None and len(response): # send the response and log it
        if type(response) == type(str()):
            # the module sent just a string so
            # I have to compose the command

            # a multi-line command must be split
            crlf_pos = response[:-2].find('\r\n')
            while -1 != crlf_pos:
                crlf_pos = crlf_pos + 2 # jump over '\r\n'
                response = response[:crlf_pos] + \
                        destination + response[crlf_pos:]

                next_crlf_pos = response[crlf_pos:-2].find('\r\n')
                if -1 != next_crlf_pos:
                    crlf_pos = crlf_pos + next_crlf_pos
                else:
                    crlf_pos = -1

            response = destination + response
        else: # the module sent a command like WHOIS or KICK
            response = ' '.join(response)

        # append CRLF if not already appended
        if '\r\n' != response[-2:]:
            response = response + '\r\n'

        try:
            with send_response_lock:
                s.send(response)
        except IOError as e:
            logging.error('Unexpected error while sending the response: {0}\n'
                .format(e))

            return False

        logging.debug(response)

        return True

    return None