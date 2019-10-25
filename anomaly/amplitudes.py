import numpy as np


class Pyramid(object):
    def _adjust_amplitude(self, anomaly):
        half_length = (len(anomaly) + 1) / 2
        amplitude_shift = np.linspace(0, self.amplitude, num=half_length)
        amplitude_shift = np.concatenate((amplitude_shift, amplitude_shift[::-1]))[
            : len(anomaly)
        ]

        anomaly = np.multiply(anomaly, amplitude_shift)

        return anomaly


class LinearSpike(object):
    def _adjust_amplitude(self, anomaly):
        amplitude_shift = np.linspace(0, self.amplitude, num=len(anomaly))
        anomaly = np.multiply(anomaly, amplitude_shift)

        return anomaly


class Constant(object):
    def _adjust_amplitude(self, anomaly):

        return anomaly * self.amplitude
