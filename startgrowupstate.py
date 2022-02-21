from driver import Driver


class StartGrowUpstate(Driver):

    def __init__(self):
        super().__init__()
        self.url = "https://www.startgrowupstate.com/explore-events"
        self.events = []

    def get_events(self):
        self.driver.get(self.url)
