from Auctor import EnvironmentDefaults


class TTYEnvironmentDefaults(EnvironmentDefaults):
    """Default settings contributed by Stylus.TTY."""

    def __init__(self) -> None:
        super().__init__(
            "Stylus.TTY",
            {
                "FORCE_COLOR": False,
                "NO_COLOR": False,
                "TERM": "",
            },
        )