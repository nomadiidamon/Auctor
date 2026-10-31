"""Runtime: initialization and shutdown of Auctor-wide infrastructure."""

from .runtime import (
	Runtime,
	get_auctor_environment,
	initialize_auctor,
	is_auctor_initialized,
	set_auctor_environment_value,
	shutdown_auctor,
	update_auctor_environment,
)

__all__ = [
	"Runtime",
	"initialize_auctor",
	"shutdown_auctor",
	"is_auctor_initialized",
	"get_auctor_environment",
	"set_auctor_environment_value",
	"update_auctor_environment",
]
