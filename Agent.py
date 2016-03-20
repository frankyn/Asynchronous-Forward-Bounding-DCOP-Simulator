import sys
import copy
from Message import Message
from CPA import CPA
from Timestamp import Timestamp


class Agent:
    # Init Defined in the AFB DisCOP Paper
    def __init__(self, agent_id, total_agents, domain, constraints, cost_functions):
        # Solution CPA and Bound
        self._CPA_SOLUTION = None
        self._B = sys.maxsize

        # Agent information
        self._id = agent_id
        self._constraints = constraints
        self._domain = domain
        self._cost_functions = cost_functions
        self._total_agents = total_agents
        # self._timestamp = [0] * (total_agents + 1)
        self._timestamp = Timestamp(self._total_agents + 1)

        # Instance variables
        self._received_cpa = None
        self._current_cpa = None
        self._next_assignment = 0  # index of value in domain
        self._current_assignment = 0
        self._estimate_value = 0  # scalar value of this agents estimate
        self._queue = []  # A python list can be used a queue
        self._converged = False

        # Only for first Agent
        if self._id == 1:
            cpa = self._generate_cpa()

            # start events
            self._queue.append(Message('CPA_MSG', self._timestamp, 0, self._id, cpa))

    # Return Solution
    def solution(self):
        return self._CPA_SOLUTION

    # Run a sequence of actions once
    def step(self):
        return self._handle_message()

    # Incoming Message
    def receive(self, msg):
        # Check Timestamp
        if self._timestamp < msg.get_timestamp() or msg.get_type() == 'TERMINATE':
            # Add into queue
            self._queue.append(msg)
        else:
            print('failed')

    # Handle message in queue
    def _handle_message(self):
        # Dequeue message from queue
        if len(self._queue) is not 0 and self._converged is not True:
            # Pop message
            msg = self._queue.pop()

            if msg.get_type() == 'FB_CPA':
                # print('Event: FB_CPA')
                return self._calculate_estimate(msg)

            elif msg.get_type() == 'CPA_MSG':
                # print('Event: CPA_MSG')
                return self._handle_cpa(msg)

            elif msg.get_type() == 'FB_ESTIMATE':
                # print('Event: FB_ESTIMATE')
                return self._handle_estimate(msg)

            elif msg.get_type() == 'NEW_SOLUTION':
                # print('Event: NEW_SOLUTION')
                # Update current CPA solution
                self._CPA_SOLUTION = msg.get_payload()
                # Update current Agent B
                self._B = self._CPA_SOLUTION.get_cost()
                return []

            elif msg.get_type() == 'TERMINATE':
                # print('Event: TERMINATE')
                # Status
                self._converged = True
                self._queue = []
                return []

    # Handle CPA
    def _handle_cpa(self, msg):
        # Store incoming CPA
        cpa = msg.get_payload()

        # If higher priority
        if msg.get_source() < self._id:
            self._current_assignment = 0
            self._next_assignment = 0
            self._received_cpa = copy.deepcopy(cpa)
            self._current_cpa = copy.deepcopy(cpa)
            self._timestamp = copy.deepcopy(msg.get_timestamp())

            # Reset future timestamp for lower priority agents
            # relate to this agent
            self._timestamp.reset_timestamp(self._id)

        return self._assign_cpa()

    # Handle creating an estimate value
    # Should return a message if estimate causes a backtrack
    def _handle_estimate(self, msg):
        # do we need to wait for all messages to be received
        # save estimate
        self._estimate_value += msg.get_payload()
        if (self._estimate_value + self._current_cpa.get_cost()) >= self._B:
            return self._assign_cpa()

    # Talk about this one tomorrow!!!
    def _calculate_estimate(self, msg):
        # msg = Message('FB_ESTIMATE', msg.timestamp(), self._id, msg.source(), 30)
        # Find best estimate value based on received cpa and possible combinations of unresolved constraints.
        # msg = FB_CPA
        fb_cpa = msg.get_payload()

        min_cost = sys.maxsize  # cost difference
        est_value = None
        for x in range(0, len(self._domain[0])):
            # assignment_cost = self._current_cost(self._current_assignment)
            # f_v =  assignment_cost + self._future_cost(self._current_assignment)
            tmp = self._possible_cpa_assignment_cost(fb_cpa.get_cpa(), x) + self._future_cpa_cost(x)

            if tmp < min_cost:
                min_cost = tmp
                est_value = x

        # Generate a FB_ESTIMATE
        # print('[Agent-%d] Estimate: %d %s'%(self._id, min_cost, self._domain[0][est_value]))
        msg = Message('FB_ESTIMATE', msg.get_timestamp(), self._id, msg.get_source(), min_cost)
        return [msg]

    # Select next value for this agent
    # Currently using an iterative method
    # If we have exhausted all possible values then
    #   return None
    def _next_domain_assignment(self):

        if self._next_assignment == len(self._domain[0]):
            return None
        else:
            assn = self._next_assignment
            self._next_assignment += 1
            return assn

    # Clear Estimates
    def _clear_estimates(self):
        self._estimate_value = 0

    # Define the hashing key
    # Select the higher priority first
    def _key(self, priority1, priority2, val1, val2):
        if priority1 > priority2:
            return '%s,%s' % (val2, val1)
        else:
            return '%s,%s' % (val1, val2)

    # Check constraints and calculate cost in local constraint graph
    # local constraint graph - constrained agents to this agent...(duh, right?)
    def _possible_cpa_assignment_cost(self, cpa, value):
        assignment_cost = 0
        hash_id = 0
        for constraint in self._constraints:
            # Check if constraint is assigned... if not ignore.
            if cpa[constraint] is not None:

                # Get hash table key
                key = self._key(self._id, constraint, self._domain[0][value], cpa[int(constraint)])

                # Add cost to assignment cost
                assignment_cost += self._cost_functions[hash_id][key]

            # Hash Id
            hash_id += 1

        return assignment_cost

    # Get most recent CPA cost provided by higher priority agent
    def _past_cpa_cost(self):
        # Check if current is first
        if self._id == 1:
            # We are in the first agent
            return 0
        else:
            # Not first agent then return receive CPA_Cost
            return self._received_cpa.get_cost()

    # Estimate future cost based on constrained lower priority agents
    def _future_cpa_cost(self, value):
        # Try all possible domain values
        # Case 1: No Lower Priority Constraints
        lower_priority = False
        for x in self._constraints:
            if x > self._id:
                lower_priority = True

        if lower_priority is not True:
            return 0

        # Case 2: Constraints, but we only consider lower priority agents
        # Summation of h functions
        h_sum = 0

        # Iterate over all constraints
        for constraint in self._constraints:
            if constraint > self._id:
                h_sum += self._min_assignment(value, constraint)

        return h_sum

    # Find best assignment for constrained agent given possible assignment value
    def _min_assignment(self, value, j_id):
        min_cost = sys.maxsize
        # For each value in the jth domain
        j_hash_function_index = self._constraints.index(j_id)
        # index of jth hash
        j_hash_function = self._cost_functions[j_hash_function_index]
        j_domain_index = j_hash_function_index + 1
        j_domain = self._domain[j_domain_index]

        for v in j_domain:
            # create a key for the jth hash table
            key = self._key(self._id, j_id, self._domain[0][value], v)

            # access value
            current_cost = j_hash_function[key]
            if current_cost < min_cost:
                min_cost = current_cost

        return min_cost

    # Create the first CPA :D
    def _generate_cpa(self):
        # Generate a CPA class to maintain the problem
        cpa = [None] * (self._total_agents + 1)

        return CPA(0, cpa)

    # Assign next possible domain value for this agent
    def _assign_cpa(self):
        # clear estimates
        self._clear_estimates()

        # if CPA contains an assignment A_i = w_i remove it
        if self._current_cpa.get_cpa()[self._id] is not None:
            self._current_cpa.get_cpa()[self._id] = None  # Add method to modify assignment

        # find a new value (v)
        while True:
            self._current_assignment = self._next_domain_assignment()
            if self._current_assignment is None:
                return self._backtrack()

            assignment_cost = self._possible_cpa_assignment_cost(self._received_cpa.get_cpa(), self._current_assignment)
            f_v = assignment_cost + self._future_cpa_cost(self._current_assignment)

            # Assign Variable
            if (self._past_cpa_cost() + f_v) < self._B:
                # Assign the possible value
                # Update CPA
                self._current_cpa = copy.deepcopy(self._received_cpa)
                self._current_cpa.get_cpa()[self._id] = self._domain[0][self._current_assignment]
                self._current_cpa.set_cost(self._past_cpa_cost() + assignment_cost)

                # Increase timestamp
                self._timestamp.increase_timestamp(self._id)
                break

        # Add value to CPA and calculate cost
        if self._current_cpa.is_full():
            self._CPA_SOLUTION = copy.deepcopy(self._current_cpa)
            self._B = self._current_cpa.get_cost()

            msg_list = []  # broadcast to all agents updated B
            for x in range(1, self._total_agents + 1):
                msg = Message('NEW_SOLUTION', self._timestamp, self._id, x, self._CPA_SOLUTION)
                msg_list.append(msg)

            return msg_list + self._assign_cpa()
        else:
            # send cpa message to next agent in order
            msg_list = [Message('CPA_MSG', self._timestamp, self._id, self._id + 1, self._current_cpa)]

            for x in range(self._id + 1, self._total_agents + 1):
                msg = Message('FB_CPA', self._timestamp, self._id, x, self._current_cpa)
                msg_list.append(msg)
            return msg_list

    # No more possible domain values or pruning search space
    def _backtrack(self):
        # clear estimates
        # Check if in first agent
        self._clear_estimates()

        if self._id == 1:
            # Broadcast Terminate
            msg_list = []
            for x in range(2, self._total_agents + 1):
                msg = Message('TERMINATE', self._timestamp, self._id, x, None)
                msg_list.append(msg)

            return msg_list

        else:
            # send CPA_MSG message to A_i-1
            msg = Message('CPA_MSG', self._timestamp, self._id, self._id - 1, self._received_cpa)
            return [msg]
