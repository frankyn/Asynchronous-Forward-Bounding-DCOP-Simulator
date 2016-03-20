
class Timestamp:
    def __init__(self, total_agents):
        self._total_agents = total_agents
        self._timestamp = [0] * total_agents

    def get_timestamp(self):
        return self._timestamp

    # Increase Timestamp
    def increase_timestamp(self, agent_id):
        self._timestamp[agent_id] += 1

    # Reset all future timestamp valus relative to current agent_id
    def reset_timestamp(self, agent_id):
        for x in range(agent_id + 1, self._total_agents):
            self._timestamp[x] = 0

    # Define size of Timestamp
    def __len__(self):
        return len(self._timestamp)

    # Overload the operator Timestamp[]
    def __getitem__(self, item):
        return self._timestamp[item]

    # Check if this timestamp is smaller than incoming
    def __lt__(self, incoming):
        # Check timestamps are of equal size
        if len(self) != len(incoming):
            return False

        for index in range(1, len(incoming)):
            if incoming[index] == self._timestamp[index]:
                continue
            elif incoming[index] < self._timestamp[index]:
                return False
            elif incoming[index] > self._timestamp[index]:
                return True

        return True

    # Check if this timestamp is greater than incoming
    def __gt__(self, incoming):
        # Check timestamps are of equal size
        if len(self) != len(incoming):
            return False

        return not self < incoming

    def __str__(self):
        return str(self._timestamp)

# Unit Test
if __name__ == "__main__":
    timestamp1 = Timestamp(5)
    timestamp2 = Timestamp(5)

    timestamp1.increase_timestamp(1)

    if timestamp1 > timestamp2:
        print('Greater')
    else:
        print('Smaller')




