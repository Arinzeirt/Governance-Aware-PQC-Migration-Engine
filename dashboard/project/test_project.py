from dashboard.project.manager import manager


manager.create_assessment(
    name="Assessment One",
    repository="repo-one",
    repository_type="Git Repository",
)

manager.create_assessment(
    name="Assessment Two",
    repository="repo-two",
    repository_type="Git Repository",
)

print()
print("Assessment Registry")
print("-------------------")

for project in manager.list_assessments():

    print(
        project.name,
        "|",
        project.status,
    )

print()
print("Current Assessment")
print("------------------")
print(manager.current.name)
