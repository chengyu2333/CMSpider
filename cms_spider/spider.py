import json


class Spider:
    def __init__(self, config=None):
        if config:
            try:
                self.config = json.loads(config)
            except Exception as e:
                raise

    def run(self):
        print("run", self.config)

    def stop(self):
        print("stop")

    def catch_url(self):
        pass

    def catch_article(self):
        pass

    def catch_file(self):
        pass

    def recover_status(self):
        pass

