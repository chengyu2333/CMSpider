import json


class Spider:
    def __init__(self, config):
        try:
            self.config = json.loads(config)
        except Exception as e:
            raise

    @staticmethod
    def run(self):
        print("run", self.config)

    @staticmethod
    def stop(self):
        print("stop")

    @staticmethod
    def catch_url():
        pass

    @staticmethod
    def catch_article():
        pass

    @staticmethod
    def catch_file():
        pass

    @staticmethod
    def recover_status():
        pass

