def _start_stop_step_validate(stmt):
    if not isinstance(stmt.step, int) or stmt.step != 1:
        raise ValueError(f"step other then 1 isn't supported, but it is {stmt.step}")
    if isinstance(stmt.start, int) and isinstance(stmt.stop, int) and stmt.start >= stmt.stop:
        raise ValueError(f"start({stmt.start}) should be smaller then stop({stmt.stop})")
