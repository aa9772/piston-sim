class SimplePLC:
    """
    Very simple PLC logic.
    The PLC does NOT know piston position,
    only discrete feedback signals.
    """


    def __init__(self):
        self.u_extend = False
        self.u_retract = False


    def step(self, y_extended: bool, y_retracted: bool):
        """
        PLC decision logic.
        Example: cyclic extend / retract.
        """
        if y_retracted:
            self.u_extend = True
            self.u_retract = False
        elif y_extended:
            self.u_extend = False
            self.u_retract = True