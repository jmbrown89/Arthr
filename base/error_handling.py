__author__ = 'james'


class RegistrationError(Exception):

    def __init__(self, msg):
        super(RegistrationError, self).__init__(msg)