import re


EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


def valid_email(email):

    return bool(re.match(EMAIL_REGEX, email))


def overview_complete(data):

    required = [

        "organisation_name",
        "organisation_email",
        "industry",
        "country",
        "organisation_size",
        "critical_infrastructure",

    ]

    completed = 0

    for field in required:

        if data.get(field):

            completed += 1

    return completed, len(required)
