class PacingEngine:

    def __init__(self, max_calls_per_agent=2):
        self.max_calls_per_agent = max_calls_per_agent

    def calculate_progressive_calls(
        self,
        available_agents,
        queued_borrowers
    ):
        """
        Progressive dialing:
        One call is made for each available agent.
        """

        if available_agents <= 0:
            return 0

        if queued_borrowers <= 0:
            return 0

        return min(
            available_agents,
            queued_borrowers
        )

    def calculate_predictive_calls(
        self,
        available_agents,
        queued_borrowers
    ):
        """
        Predictive dialing:
        Multiple calls can be started per available agent.
        """

        if available_agents <= 0:
            return 0

        if queued_borrowers <= 0:
            return 0

        calls = (
            available_agents
            * self.max_calls_per_agent
        )

        return min(
            calls,
            queued_borrowers
        )