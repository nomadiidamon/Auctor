"""
@example auctor_environment_aggregate.py
Aggregate defaults from separate package namespaces into one mapping.
"""

from Auctor import EnvironmentDefaults

providers = [
    EnvironmentDefaults("Example.Logging", {"LEVEL": "info"}),
    EnvironmentDefaults("Example.Terminal", {"FORCE_COLOR": False}),
]

print(dict(EnvironmentDefaults.aggregate(providers)))
