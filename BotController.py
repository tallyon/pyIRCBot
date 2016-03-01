import redis
import os

class BotController:
    """Main bot logic. Gateway for all interaction with bot modules."""
    def __init__(self, configFile = "pyircbot.config"):
        self.configFilePath = configFile
        self.configFile = None
        self.configHeader = "#!pyIRCBot configuration file:"
        self.ReadConfigFile()
        # Redis connection
        self.Redis = None

    def ReadConfigFile(self):
        """Reads config from config file"""
        # Open set configuration file
        try:
            self.configFile = open(self.configFilePath, "r")
        except IOError as e:
            return "Cannot open {0}: {1}".format(self.configFilePath,e.strerror)

        splitConfigFile = self.configFile.read().split("\n")
        for line in splitConfigFile:
            # Set Bot class variables from config file
            # Omit empty lines, region indicators (starting with [) and comments (starting with #)
            if line != "" and line.find("[") != 0 and line.find("#") != 0:
                # Line that does not have X = Y is invalid and therefore ommmited
                if len(line.split('=')) < 2:
                    continue
                else:
                    varName = str.strip(line.split('=')[0])
                    varValue = str.strip(line.split('=')[1])
                    self.SetConfigVar(varName, varValue)

    def TestConfigurationFile(self):
        """Does complete check of configuration file provided while initializing BotController object"""
        # Open set configuration file
        try:
            self.configFile = open(self.configFilePath, "r")
        except IOError as e:
            return "Cannot open {0}: {1}".format(self.configFilePath,e.strerror)

        evaluatedConfig = "\nConfiguration OK"
        # Validate configuration file header
        headerLine = str.strip(self.configFile.readline())
        if headerLine != self.configHeader:
            print "{0} is not {1}".format(headerLine, self.configHeader)
            return "Invalid configuration file header!"

        splitConfigFile = self.configFile.read().split("\n")
        for line in splitConfigFile:
            # Set Bot class variables from config file
            # Omit empty lines, region indicators (starting with [) and comments (starting with #)
            if line != "" and line.find("[") != 0 and line.find("#") != 0:
                # Line that does not have X = Y is invalid and therefore ommmited
                if len(line.split('=')) < 2:
                    continue
                else:
                    varName = str.strip(line.split('=')[0])
                    varValue = str.strip(line.split('=')[1])
                    # Prints result of trying to set varName to varValue
                    varSetResult = self.SetConfigVar(varName, varValue)
                    print varSetResult

                    # If [ERROR] was returned by SetConfigVar return the function
                    if varSetResult.find("[ERROR]") != -1:
                        evaluatedConfig = "\nConfiguration Invalid!"
                        # Return configuration test string to output
                        return evaluatedConfig

        # Return configuration test string to output
        return evaluatedConfig

    def SetConfigVar(self, varName, varValue):
        """Sets /varName/ class variable to /varValue/ value."""
        if varName == "redisHost":
            self.redisHost = varValue
        elif varName == "redisPort":
            self.redisPort = varValue
        elif varName == "redisDB":
            self.redisDB = varValue
        else:
            return "=======================\r\n[ERROR]Invalid property: {0}!\r\n=======================\r\n".format(varName)

        return "{0} set to {1}".format(varName, varValue)

    def ConnectToRedis(self):
        """Establish connection to redis."""
        self.Redis = redis.StrictRedis(host=self.redisHost, port=self.redisPort, db=self.redisDB)
        return self.Redis

    def GetRedisInstance(self):
        """Returns instance of Redis connection."""
        return self.Redis
