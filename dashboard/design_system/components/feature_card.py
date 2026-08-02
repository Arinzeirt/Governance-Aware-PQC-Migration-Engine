from .card import show as card


def show(
    icon,
    title,
    description,
):

    card(
        icon=icon,
        title=title,
        body=description,
    )
