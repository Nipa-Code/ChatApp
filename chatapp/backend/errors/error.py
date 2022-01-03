class NonExistentValueError(ValueError):
    """
    Raised when invalid key is given while authentication or value dies nit exist
        `message` -- the value that does not exist
    """

    def __init__(self, message: str):
        super().__init__(f"Could not fetch data | {message}")

        self.message = message
