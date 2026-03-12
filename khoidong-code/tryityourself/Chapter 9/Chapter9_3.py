class User:
    """A simple profile of a user."""

    def __init__(self, first_name, last_name, location, age):
        """Initialize user attributes."""
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.location = location.title()
        self.age = age

    def describe_user(self):
        """Display a summary of the user's information."""
        print(f"\nUser Profile: {self.first_name} {self.last_name}")
        print(f"  Location: {self.location}")
        print(f"  Age: {self.age}")

    def greet_user(self):
        """Print a personalized greeting."""
        print(f"Welcome back, {self.first_name} {self.last_name}!")

user_1 = User('hoa', 'huynh', 'thu dau mot', 21)
user_2 = User('linh', 'nguyen', 'tan uyen', 20)

user_1.describe_user()
user_1.greet_user()

user_2.describe_user()
user_2.greet_user()