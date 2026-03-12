class User:

    def __init__(self, first_name, last_name, location, age):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.location = location.title()
        self.age = age
        self.login_attempts = 0

    def increment_login_attempts(self):
        """Increment the value of login_attempts by 1."""
        self.login_attempts += 1

    def reset_login_attempts(self):
        """Reset login_attempts to 0."""
        self.login_attempts = 0

class Privileges:
    """A class to store admin privileges."""

    def __init__(self, privileges=[]):
        if not privileges:
            self.privileges = ["can add post", "can delete post", "can ban user"]
        else:
            self.privileges = privileges

    def show_privileges(self):
        """Display the privileges."""
        print("\nAdmin privileges:")
        for privilege in self.privileges:
            print(f"- {privilege}")

class Admin(User): # Using User class from earlier
    """A user with administrative privileges."""

    def __init__(self, first_name, last_name, location, age):
        super().__init__(first_name, last_name, location, age)
        # Initialize an empty set of privileges
        self.privileges = Privileges()

admin_user = Admin('grace', 'hopper', 'new york', 85)
admin_user.privileges.show_privileges()

