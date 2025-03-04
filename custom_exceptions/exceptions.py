class OpenAIRequestError(Exception):
    """General error when making a request to OpenAI API."""

    def __init__(self, message="An error occurred while processing the OpenAI request"):
        self.message = message
        super().__init__(self.message)


class OpenAITimeoutError(Exception):
    """Custom timeout error for OpenAI API requests."""

    def __init__(self, message="OpenAI API request timed out"):
        self.message = message
        super().__init__(self.message)
