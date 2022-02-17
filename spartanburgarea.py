from driver import Driver


class SpartanburgArea(Driver):

    def __init__(self):
        super().__init__()
        self.url = "http://spartanburgareasc.chambermaster.com/events/"
