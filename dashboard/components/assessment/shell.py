from components.assessment.header import show as header


def show(content):

    step = content["step"]

    #
    # Compact assessment header
    #

    header(step)

    #
    # Current assessment workspace.
    # The Summary panel owns Back / Continue.
    #

    content["renderer"]()
