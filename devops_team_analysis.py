cloud_engineers = {"Hritik", "Bhuwan", "Rakhsha", "Sharman"}
security_testers = {"Joey", "Chandler", "Ross", "Monica", "Hritik"}

both_roles = cloud_engineers.intersection(security_testers)

entire_team = cloud_engineers.union(security_testers)

print("Cloud Engineers:", cloud_engineers)
print("Security Testers:", security_testers)
print("Both Roles:", both_roles)
print("Entire Team:", entire_team)