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

    "user": {
        "password": "12345",
        "role": "user",
        "name": "EQMP User",
    },

    "admin": {
        "password": "12345",
        "role": "admin",
        "name": "EQMP Administrator",
    },
}


def authenticate(identifier, password):

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
