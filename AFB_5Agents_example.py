from Agent import Agent


def main():
    # Main definition will AFB
    # Number of agents
    agent_n = 5

    # Predefined hashing function
    hash_1_4 = {'R,R': 16, 'R,B': 89, 'B,R': 47, 'B,B': 10}
    hash_2_4 = {'R,R': 92, 'R,B': 27, 'B,R': 91, 'B,B': 100}
    hash_2_5 = {'R,R': 87, 'R,B': 22, 'B,R': 82, 'B,B': 73}
    hash_3_4 = {'R,R': 21, 'R,B': 28, 'B,R': 86, 'B,B': 71}

    # Domain per agent
    domain_agent_1 = ["R", "B"]
    domain_agent_2 = ["R", "B"]
    domain_agent_3 = ["R", "B"]
    domain_agent_4 = ["R", "B"]
    domain_agent_5 = ["R", "B"]

    # Hash list used per agent
    agent1_hash = [hash_1_4]
    agent2_hash = [hash_2_4, hash_2_5]
    agent3_hash = [hash_3_4]
    agent4_hash = [hash_1_4, hash_2_4, hash_3_4]
    agent5_hash = [hash_2_5]

    # Contraints per agent
    agent1_cons = [4]
    agent2_cons = [4,5]
    agent3_cons = [4]
    agent4_cons = [1, 2, 3]
    agent5_cons = [2]

    # Domain list per agent
    agent1_domains = [domain_agent_1, domain_agent_4]
    agent2_domains = [domain_agent_2, domain_agent_4, domain_agent_5]
    agent3_domains = [domain_agent_3, domain_agent_4]
    agent4_domains = [domain_agent_4, domain_agent_1, domain_agent_2, domain_agent_3]
    agent5_domains = [domain_agent_5, domain_agent_2]

    # fill in hash
    agent_list = [None,
                  Agent(1, agent_n, agent1_domains, agent1_cons, agent1_hash),
                  Agent(2, agent_n, agent2_domains, agent2_cons, agent2_hash),
                  Agent(3, agent_n, agent3_domains, agent3_cons, agent3_hash),
                  Agent(4, agent_n, agent4_domains, agent4_cons, agent4_hash),
                  Agent(5, agent_n, agent5_domains, agent5_cons, agent5_hash)]

    # converged(boolean)
    converged = False  # Hasn't converged yet
    cpa_msg_count = 0
    while not converged:
        for agent in agent_list:
            if agent is None:  # Skip first index
                continue
            # do something with agent
            msg_list = agent.step()  # step through one full unit

            # Skip any further execution
            if msg_list is None:
                continue

            # process messages by adding to agent queues
            for msg in msg_list:
                if msg.get_type() == 'TERMINATE':
                    converged = True  # We have converged.
                print("[Agent: %d] %s"%(agent._id, msg))
                if msg.get_type() == 'CPA_MSG' and msg.get_destination() > msg.get_source():
                    cpa_msg_count += 1
                agent_list[int(msg.get_destination())].receive(msg)

    # Print out result
    # Select first Agent
    print(agent_list[agent_n].solution())
    print(cpa_msg_count)

# Execute Simulator
if __name__ == "__main__":
    main()
