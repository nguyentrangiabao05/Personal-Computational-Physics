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

class Admin(User):
    """A user with administrative privileges."""

    def __init__(self, first_name, last_name, location, age):
        """Initialize parent attributes, then admin specific attributes."""
        super().__init__(first_name, last_name, location, age)
        self.privileges = ["can add post", "can delete post", "can ban user"]

    def show_privileges(self):
        """Display the privileges this administrator has."""
        print(f"\nPrivileges for {self.first_name} {self.last_name}:")
        for privilege in self.privileges:
            print(f"- {privilege}")

admin_user = Admin('ada', 'lovelace', 'london', 36)
admin_user.show_privileges()