"""
@example runtime_initialize.py
Initialize Auctor explicitly and shut it down when done.
"""

from Auctor import initialize_auctor, is_auctor_initialized, shutdown_auctor

print("before:", is_auctor_initialized())
initialize_auctor()
print("after:", is_auctor_initialized())
shutdown_auctor()
print("shutdown:", not is_auctor_initialized())
