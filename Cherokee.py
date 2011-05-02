#!/usr/bin/env python


import urllib


CHEROKEE_INFO_URL = "http://localhost/about/info/py?type=connection_details"


class Cherokee:
    """
    Collects and returns server information and connection details from
    Cherokee.
    """
    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config

    def get_modules_stats(self, server_info):
        """
        Title: Modules
        loggers
        handlers
        encoders
        validators
        generic
        balancers
        rules
        cryptors
        vrules
        collectors
        """
        if not server_info.has_key("modules"):
            return {}
        modules = server_info["modules"]
        return {
            "loggers" : modules.get("loggers", None),
            "handlers" : modules.get("handlers", None),
            "encoders" : modules.get("encoders", None),
            "validators" : modules.get("validators", None),
            "generic" : modules.get("generic", None),
            "balancers" : modules.get("balancers", None),
            "rules" : modules.get("rules", None),
            "cryptors" : modules.get("cryptors", None),
            "vrules" : modules.get("vrules", None),
            "collectors" : modules.get("collectors", None),
        }

    def get_connections_stats(self, server_info):
        """
        Title: Connections
        number
        active
        reusable
        """
        if not server_info.has_key("connections"):
            return {}
        connections = server_info["connections"]
        return {
            "number" : connections.get("number", None),
            "active" : connections.get("active", None),
            "reusable" : connections.get("reusable", None)
        }

    def get_config_stats(self, server_info):
        """
        Title: Config
        threads
        """
        return {
            "threads" : server_info.get("config", {}).get("threads", None)
        }

    def get_uptime_stats(self, server_info):
        """
        Title: Uptime
        seconds
        """
        return {
            "seconds" : server_info.get("uptime", {}).get("seconds", None)
        }

    def get_traffic_stats(self, server_info):
        """
        Title: Traffic
        tx
        rx
        accepts
        timeouts
        """
        if not server_info.has_key("traffic"):
            return {}
        traffic = server_info["traffic"]
        return {
            "tx" : traffic.get("tx", None),
            "rx" : traffic.get("rx", None),
            "accepts" : traffic.get("accepts", None),
            "timeouts" : traffic.get("timeouts", None)
        }

    def run(self):
        stats = {}
        try:
            data = urllib.urlopen(CHEROKEE_INFO_URL).read()
            self.checks_logger.debug(data)
            server_info = eval(data)
            stats.update(self.get_uptime_stats(server_info))
            stats.update(self.get_config_stats(server_info))
            stats.update(self.get_traffic_stats(server_info))
            stats.update(self.get_connections_stats(server_info))
            stats.update(self.get_modules_stats(server_info))
        except IOError:
            stats = {}
        self.checks_logger.debug(stats)
        return stats


if __name__ == "__main__":
    import logging
    logger = logging.getLogger("Cherokee")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    cherokee = Cherokee(None, logger, None)
    cherokee.run()
