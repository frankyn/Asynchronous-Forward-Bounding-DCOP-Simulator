# CPA Class
import copy


class CPA:
    def __init__(self, cpa_value, cpa):
        self._cpa_value = copy.deepcopy(cpa_value)
        self._cpa = copy.deepcopy(cpa)

    def get_cpa(self):
        return self._cpa

    def get_cost(self):
        return self._cpa_value

    def set_cost(self, cpa_value):
        self._cpa_value = copy.deepcopy(cpa_value)

    def set_cpa(self,cpa):
        self._cpa = copy.deepcopy(cpa)

    def is_full(self):
        # Iterate through all possible agent ranges
        # Check if any are None return False
        for x in range(1,len(self._cpa)):
            if self._cpa[x] is None:
                return False

        # If all agents are assigned return True
        return True

    def __str__(self):
        return "%s -> %d"%(str(self._cpa), self._cpa_value)
