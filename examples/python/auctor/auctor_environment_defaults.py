"""
@example auctor_environment_defaults.py
Declare namespaced Auctor settings without changing process environment variables.
"""

from Auctor import EnvironmentDefaults


defaults = EnvironmentDefaults(
    "Example.Feature",
    {
        "ENABLED": True,
        "MODE": "automatic",
    },
)

print(dict(defaults.qualified_values()))
