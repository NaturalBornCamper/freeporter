class Log(object):
    DEBUG = 'd'
    WARNING = 'w'
    ERROR = 'e'

    __messages = {DEBUG: [], WARNING: [], ERROR: []}

    @staticmethod
    def __append_message(channel, message):
        # print(channel, ": ", message)
        Log.__messages[channel].append(message)

    @staticmethod
    def d(message):
        Log.__append_message(Log.DEBUG, message)

    @staticmethod
    def w(message):
        Log.__append_message(Log.WARNING, message)

    @staticmethod
    def e(message):
        Log.__append_message(Log.ERROR, message)


    #
    # def __append_message(self, channel, message):
    #     print(channel, ": ", message)
    #     self.__messages[channel].append(message)
    #
    # def d(self, message):
    #     self.__append_message(self.DEBUG, message)
    #
    # @staticmethod
    # def w(self, message):
    #     self.__append_message(self.WARNING, message)
    #
    # def e(self, message):
    #     self.__append_message(self.ERROR, message)