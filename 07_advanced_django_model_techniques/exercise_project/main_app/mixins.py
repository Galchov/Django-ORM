from django.db import models


class RechargeEnergyMixin:
    ENERGY_LIMIT: int = 100
    
    def recharge_energy(self, amount: int) -> None:
        self.energy += amount

        if self.energy > self.ENERGY_LIMIT:
            self.energy = self.ENERGY_LIMIT

        self.save()
