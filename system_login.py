import auth_helpers

auth_helpers.verify_admin("admin")
print(auth_helpers.verify_admin("admin"))  # Output: True