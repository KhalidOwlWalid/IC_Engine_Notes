from dataclasses import dataclass

from engine_lib.burn_fraction import BurnFraction

class Engine(BurnFraction):

    def __init__(self, V_bdc):
        self.V_bdc = V_bdc
