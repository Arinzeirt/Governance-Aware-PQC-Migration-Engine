"""
Development authentication configuration for EQMP.

This is a temporary development authentication layer.
Replace with persistent, hashed credentials before production.
"""

USERS = {
    "test@eqmp.local": {
        "password": "EQMP-Test-2026!",
        "role": "testing",
        "name": "EQMP Test Account",
    },

    "user@eqmp.local": {
        "password": "eqmp123",
        "role": "user",
        "name": "EQMP User",
    },

    "admin@eqmp.local": {
        "password": "eqmp123",
        "role": "admin",
        "name": "EQMP Administrator",
    },
}


def authenticate(identifier, password):

    identifier = identifier.strip().lower()

    account = USERS.get(
        identifier,
    )

    if not account:
        return None

    if account["password"] != password:
        return None

    return {
        "identifier": identifier,
        "role": account["role"],
        "name": account["name"],
    }


def is_admin():

    return (
        st.session_state.get(
            "eqmp_user_role"
        ) == "admin"
    )
