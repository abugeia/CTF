import json
import random
from pwn import *

# Set up the remote connection
HOST = 'chal.sunshinectf.games'
PORT = 25201

def solve():
    # Connect to the remote service
    conn = remote(HOST, PORT)

    try:
        # Receive the initial banner
        initial_banner = conn.recvuntil(b'science!\n\n').decode()
        log.info(f"Initial banner:\n{initial_banner}")

        # Start with a random population
        population = [[random.uniform(0, 1) for _ in range(10)] for _ in range(100)]

        for generation in range(1, 101):
            # Format and send the payload
            payload = json.dumps({"samples": population}).encode()
            conn.sendline(payload)
            log.info(f"Generation {generation}: Sent population.")

            # Receive and parse the response
            response_data = conn.recvline().strip().decode()
            try:
                response = json.loads(response_data)
            except json.JSONDecodeError:
                log.success(f"Received non-JSON response, probably the flag: {response_data}")
                # Try to receive more data just in case
                log.info(conn.recvall(timeout=1).decode())
                break

            log.info(f"Generation {generation}: Average score = {response['average']:.4f}")

            # Check for the flag in the JSON
            if "flag" in response:
                log.success(f"Flag found: {response['flag']}")
                break

            # Genetic algorithm: selection and mutation
            scores = response['scores']
            
            # Combine population and scores for sorting
            scored_population = sorted(zip(population, scores), key=lambda x: x[1], reverse=True)
            
            # Select the top 10 performers as parents for the next generation
            parents = [ind for ind, score in scored_population[:10]]
            
            # Create the next generation through mutation
            next_population = []
            for _ in range(100):
                parent = random.choice(parents)
                # Mutate the parent's genes by a small amount
                mutated_child = [
                    min(max(gene + random.uniform(-0.05, 0.05), 0), 1) for gene in parent
                ]
                next_population.append(mutated_child)
            
            population = next_population

    except Exception as e:
        log.error(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()
        log.info("Connection closed.")

if __name__ == "__main__":
    solve()