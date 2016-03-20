from Agent import Agent


def main():
    # Main definition will AFB

    # Number of agents
    agent_n = 3

    # Predefined hashing function
    hash_1_2 = {'R,R': 10, 'R,B': 6, 'B,R': 27, 'B,B': 20}
    hash_1_3 = {'R,R': 5, 'R,B': 3, 'B,R': 34, 'B,B': 16}
    hash_2_3 = {'R,R': 1, 'R,B': 9, 'B,R': 8, 'B,B': 15}

    # Domain per agent
    domain_agent_1 = ["R", "B"]
    domain_agent_2 = ["R", "B"]
    domain_agent_3 = ["R", "B"]

    # Hash list used per agent
    agent1_hash = [hash_1_2, hash_1_3]
    agent2_hash = [hash_1_2, hash_2_3]
    agent3_hash = [hash_1_3, hash_2_3]

    # Contraints per agent
    agent1_cons = [2, 3]
    agent2_cons = [1, 3]
    agent3_cons = [1, 2]

    # Domain list per agent
    agent1_domains = [domain_agent_1, domain_agent_2, domain_agent_3]
    agent2_domains = [domain_agent_2, domain_agent_1, domain_agent_3]
    agent3_domains = [domain_agent_3, domain_agent_1, domain_agent_2]

    # fill in hash
    agent_list = [None,
                  Agent(1, agent_n, agent1_domains, agent1_cons, agent1_hash),
                  Agent(2, agent_n, agent2_domains, agent2_cons, agent2_hash),
                  Agent(3, agent_n, agent3_domains, agent3_cons, agent3_hash)]

    # converged(boolean)
    converged = False  # Hasn't converged yet

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

                agent_list[int(msg.get_destination())].receive(msg)

    # Print out result
    # Select first Agent
    print(agent_list[agent_n].solution())


# Execute Simulator
if __name__ == "__main__":
    main()
