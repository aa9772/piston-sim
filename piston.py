class Piston:
    """Minimal piston model with optional sensors and commands."""

    def __init__(self, stroke: float, speed: float):
        self.stroke = stroke
        self.speed = speed
        self.x = 0.0
        self.has_retract_sensor = True
        self.has_extend_sensor = True
        self.single_command = False  # True = single command
        # For visualization
        self.u_extend = False
        self.u_retract = False

    def step(self, u_extend: bool, u_retract: bool, dt: float):
        """Update piston position according to commands."""
        if u_extend and not u_retract:
            self.x += self.speed * dt
        elif u_retract and not u_extend:
            self.x -= self.speed * dt

        # Physical end-stops
        self.x = max(0.0, min(self.x, self.stroke))

    @property
    def y_extended(self) -> bool:
        return self.x >= self.stroke

    @property
    def y_retracted(self) -> bool:
        return self.x <= 0.0
