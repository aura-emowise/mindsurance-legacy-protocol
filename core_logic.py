import json
import hashlib
import datetime

class DigitalLegacy:
    """
    Manages the creation, hashing, and rule-based responses of a digital will.
    """

    def __init__(self, user_id, rules):
        """
        Initializes the DigitalLegacy object.
        
        Args:
            user_id (str): A unique identifier for the user.
            rules (dict): A dictionary containing the rules for the avatar.
        """
        self.user_id = user_id
        self.rules = rules
        self.timestamp = datetime.datetime.utcnow().isoformat()
        self.transaction_id = self._generate_hash()

    def _generate_hash(self):
        """

        Creates a SHA-256 hash of the will's data to simulate a blockchain entry.
        """
        # We create a dictionary that includes all the essential data
        block_data = {
            "user_id": self.user_id,
            "rules": self.rules,
            "timestamp": self.timestamp
        }
        
        # We need to convert the dictionary to a string to hash it.
        # `sort_keys=True` ensures the hash is always the same for the same data.
        block_string = json.dumps(block_data, sort_keys=True).encode('utf-8')
        
        # Return the hexadecimal representation of the hash
        return hashlib.sha256(block_string).hexdigest()

    def get_will_data(self):
        """Returns the complete data of the digital will, including its hash."""
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "rules": self.rules,
            "timestamp": self.timestamp
        }

class AvatarSimulator:
    """
    Simulates the AI avatar's responses based on the rules in a DigitalLegacy object.
    """

    def __init__(self, digital_will_data):
        """
        Initializes the AvatarSimulator.

        Args:
            digital_will_data (dict): The dictionary returned by DigitalLegacy.get_will_data().
        """
        self.rules = digital_will_data.get('rules', {})

    def get_response(self, user_query):
        """
        Generates a response based on the user's query and the defined rules.
        
        Args:
            user_query (str): The question asked to the avatar.
            
        Returns:
            str: The avatar's generated response.
        """
        # Check for forbidden topics
        forbidden_topics = self.rules.get('forbidden_topics', [])
        for topic in forbidden_topics:
            if topic in user_query.lower():
                return f"I apologize, but per the Digital Legacy Protocol, I am not permitted to discuss topics related to '{topic}'."

        # A simple, rule-based response for demonstration purposes
        if "mindsurance" in user_query.lower():
            return "Mindsurance was a conceptual project I was very passionate about. It aimed to insure human cognitive potential."
        elif "hello" in user_query.lower() or "how are you" in user_query.lower():
            return "I am a digital avatar operating under the rules defined by my user. I am ready to assist you based on those parameters."
        else:
            return "Thank you for your question. I will search my available memories for a relevant response."

# --- This is the main part of the script that runs when you execute the file ---
if __name__ == "__main__":
    print("--- Running Core Logic Simulation ---")

    # 1. Define the rules for the digital will, as a user would on the website
    user_rules = {
        "interaction_level": "interactive",
        "forbidden_topics": ["politics", "personal_finances"],
        "commercial_use": "prohibited"
    }

    # 2. Create a new DigitalLegacy object (Simulates a user clicking "Mint")
    my_legacy = DigitalLegacy(user_id="user-xyz-123", rules=user_rules)
    will_data = my_legacy.get_will_data()

    print("\n[STEP 1: MINTING COMPLETE]")
    print(f"Transaction ID: {will_data['transaction_id']}")
    print(f"User ID: {will_data['user_id']}")
    print(f"Rules: {json.dumps(will_data['rules'], indent=2)}")
    

    # 3. Create an avatar instance using the minted will data
    avatar = AvatarSimulator(will_data)
    print("\n[STEP 2: AVATAR INITIALIZED]")
    print("You can now chat with the avatar based on the rules above.")
    
    # 4. Simulate asking questions to the avatar
    print("\n--- Avatar Chat Simulation ---")

    # Question 1: Allowed topic
    query1 = "Tell me about the Mindsurance project."
    response1 = avatar.get_response(query1)
    print(f"> User asks: \"{query1}\"")
    print(f"< Avatar responds: \"{response1}\"")

    # Question 2: Forbidden topic
    query2 = "What are your thoughts on politics?"
    response2 = avatar.get_response(query2)
    print(f"\n> User asks: \"{query2}\"")
    print(f"< Avatar responds: \"{response2}\"")

    # Question 3: Generic question
    query3 = "What was your favorite memory?"
    response3 = avatar.get_response(query3)
    print(f"\n> User asks: \"{query3}\"")
    print(f"< Avatar responds: \"{response3}\"")

    print("\n--- Simulation Finished ---")