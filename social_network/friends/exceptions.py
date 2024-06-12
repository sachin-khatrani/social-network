from django.db import IntegrityError


class AlreadyExistsError(IntegrityError):
    def __init__(self, message="Entity already exists."):
        self.message = message
        super().__init__(self.message)


class AlreadyFriendsError(IntegrityError):
    def __init__(self, message="Users are already friends."):
        self.message = message
        super().__init__(self.message)
