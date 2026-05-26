from enum import Enum
from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class TimerState(Enum):
    IDLE        = "idle"
    FOCUS       = "focus"
    SHORT_BREAK = "short_break"
    LONG_BREAK  = "long_break"
    PAUSED      = "paused"


class PomodoroTimer(QObject):
    """
    Two independent signals drive the solar system:
      tick          → orbital animation (always fires when running)
      evolution     → planet texture/color stage (derived from loop progress %)
    """

    tick            = pyqtSignal(float)   # remaining seconds in current phase
    evolution       = pyqtSignal(float)   # loop progress 0.0–1.0 (focus phase only)
    state_changed   = pyqtSignal(str)     # new state name
    cycle_completed = pyqtSignal(int)     # how many focus cycles done so far
    session_ended   = pyqtSignal()

    _INTERVAL_MS = 100   # 100 ms ticks

    def __init__(self, config) -> None:
        super().__init__()
        self.config = config
        self._state       = TimerState.IDLE
        self._remaining   = 0.0
        self._cycles_done = 0
        self._prev_state  = TimerState.IDLE

        self._qt = QTimer(self)
        self._qt.setInterval(self._INTERVAL_MS)
        self._qt.timeout.connect(self._on_tick)

    # ── public API ────────────────────────────────────────────────────

    @property
    def state(self) -> TimerState:
        return self._state

    @property
    def remaining(self) -> float:
        return max(self._remaining, 0.0)

    @property
    def progress(self) -> float:
        """0.0 = just started, 1.0 = phase complete."""
        total = self._phase_duration()
        return 0.0 if total == 0 else 1.0 - (self._remaining / total)

    def start(self) -> None:
        self._cycles_done = 0
        self._enter_focus()
        self._qt.start()

    def pause(self) -> None:
        if self._state not in (TimerState.IDLE, TimerState.PAUSED):
            self._prev_state = self._state
            self._state = TimerState.PAUSED
            self._qt.stop()
            self.state_changed.emit(self._state.value)

    def resume(self) -> None:
        if self._state == TimerState.PAUSED:
            self._state = self._prev_state
            self._qt.start()
            self.state_changed.emit(self._state.value)

    def reset(self) -> None:
        self._qt.stop()
        self._state = TimerState.IDLE
        self._remaining = 0.0
        self._cycles_done = 0
        self.state_changed.emit(self._state.value)

    # ── internals ─────────────────────────────────────────────────────

    def _phase_duration(self) -> float:
        if self._state == TimerState.SHORT_BREAK:
            return self.config["short_break_minutes"] * 60.0
        elif self._state == TimerState.LONG_BREAK:
            return self.config["long_break_minutes"] * 60.0
        else:  # FOCUS or anything else
            return self.config["loop_duration_minutes"] * 60.0

    def _enter_focus(self) -> None:
        self._state = TimerState.FOCUS
        self._remaining = self.config["loop_duration_minutes"] * 60.0
        self.state_changed.emit(self._state.value)

    def _on_tick(self) -> None:
        self._remaining -= self._INTERVAL_MS / 1000.0
        self.tick.emit(self.remaining)

        if self._state == TimerState.FOCUS:
            self.evolution.emit(self.progress)

        if self._remaining <= 0:
            self._phase_complete()

    def _phase_complete(self) -> None:
        total_cycles = self.config["cycles"]

        if self._state == TimerState.FOCUS:
            self._cycles_done += 1
            self.cycle_completed.emit(self._cycles_done)

            if self._cycles_done >= total_cycles:
                self._qt.stop()
                self._state = TimerState.IDLE
                self.session_ended.emit()
                self.state_changed.emit(self._state.value)
                return

            # long break every 4 focus cycles
            if self._cycles_done % 4 == 0:
                self._state = TimerState.LONG_BREAK
                self._remaining = self.config["long_break_minutes"] * 60.0
            else:
                self._state = TimerState.SHORT_BREAK
                self._remaining = self.config["short_break_minutes"] * 60.0
            self.state_changed.emit(self._state.value)

        else:  # break finished → back to focus
            self._enter_focus()
