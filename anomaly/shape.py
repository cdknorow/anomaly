import numpy as np
from scipy import signal


class Sinusoidal(object):
    def _shape(self):

        x = np.arange(
            0, self.num_cycles / (self.anomaly_frequency), 1 / self.sample_rate
        )

        y = np.sin(2 * np.pi * x * self.anomaly_frequency + self.phase)

        return y


class Peak(object):
    def _shape(self):
        x = np.arange(
            0, self.num_cycles / (self.anomaly_frequency), 1 / self.sample_rate
        )

        y = abs(np.sin(2 * np.pi * x * self.anomaly_frequency) + self.phase)

        return y


class Square(object):
    def _shape(self):

        x = np.arange(
            0, self.num_cycles / (self.anomaly_frequency), 1 / self.sample_rate
        )

        y = signal.square(2 * np.pi * x * self.anomaly_frequency + self.phase)

        return y
