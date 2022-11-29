# -*- coding: utf-8 -*-
# BEGIN_HEADER
# END_HEADER


class DOIRequest:
    '''
    Module Name:
    DOIRequest

    Module Description:
    A KBase module: DOIRequest
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.1.0"
    GIT_URL = "ssh://git@github.com/eapearson/kbase-sdk-module-doi-request"
    GIT_COMMIT_HASH = "e83605b9b231c890a7826915e80cfbf8a1212605"

    # BEGIN_CLASS_HEADER
    # END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        # BEGIN_CONSTRUCTOR
        # END_CONSTRUCTOR
        pass

    def run_DOIRequest(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        # BEGIN run_DOIRequest
        # END run_DOIRequest

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_DOIRequest return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def status(self, ctx):
        # BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        # END_STATUS
        return [returnVal]
