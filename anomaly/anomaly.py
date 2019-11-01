import random
import copy
import numpy as np


class Anomaly(object):
    """Creates an capture object from the given filename and filepath.
        Args:
            frequency_range (list): range of frequencies the anomalies can be generated at
            cycle_range (list): range of cycle lengths the anomalies can have
            amplitude_range (list): range of amplitudes the anomalies can have
            anomaly_rate (float): percent chance of an anomaly occuring at each sample
            anomaly_locations (list): default: None means any location is available. Otherwise a list of indxes 
                where anomalies could occur. Set anomaly rate to 1 in order for all locations to be used
            noise_range (list): A random noise factor that is introduced accross the dataset. List of possible values

    """

    def __init__(
        self,
        frequency_range,
        cycle_range,
        amplitude_range,
        anomaly_rate=0.001,
        anomaly_locations=None,
        noise_range=None,
        **kwargs
    ):
        self._anomaly_rate = anomaly_rate
        self._frequency_range = frequency_range
        self._cycle_range = cycle_range
        self._amplitude_range = amplitude_range
        self._noise_range = noise_range
        self._anomaly_locations = anomaly_locations
        self._extra_params = kwargs

        self._amplitude = None
        self._anomaly_frequency = None
        self._num_cycles = None
        self._noise_scale = None
        self._property_log = []

    def _update_properties(self):
        self._amplitude = np.random.choice(self._amplitude_range)
        self._anomaly_frequency = np.random.choice(self._frequency_range)
        self._num_cycles = np.random.choice(self._cycle_range)

        if self._noise_range:
            self._noise_scale = np.random.choice(self._noise_range)
        else:
            self._noise_scale = None

    @property
    def noise_scale(self):
        return self._noise_scale

    @property
    def anomaly_rate(self):
        return self._anomaly_rate

    @property
    def anomaly_locations(self):
        return self._anomaly_locations

    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def amplitude(self):
        return self._amplitude

    @property
    def anomaly_frequency(self):
        return self._anomaly_frequency

    @property
    def num_cycles(self):
        return self._num_cycles

    @property
    def anomaly_description(self):
        return self._property_log

    def _reset_property_log(self):
        self._property_log = []

    def _log_properties(self, index, duration):
        self._property_log.append(
            {
                "amplitude": self.amplitude,
                "anomaly_frequency": self.anomaly_frequency,
                "num_cycles": self.num_cycles,
                "index": index,
                "duration": duration,
            }
        )

    def _shape(self):
        """ Determines the shape of the anomaly, this function can be overidden for different shapes cases """
        x = np.arange(
            0, self.num_cycles / (self.anomaly_frequency), 1 / self.sample_rate
        )

        y = np.sin(2 * np.pi * x * self.anomaly_frequency)

        return y

    def _adjust_amplitude(self, y):
        """ Takes an anomaly and modifies the amplitude. 
        This function can be overwritten with a spcific amplitude function """

        return y * self.amplitude

    def _add_noise(self, y):
        """ add a noise factor to the data set """
        if not self._noise_scale:
            return y

        y += np.array(
            [
                np.random.choice(range(-self._noise_scale, self._noise_scale))
                for i in range(len(y))
            ]
        )
        return y

    def _get_input_data_type(self, y):
        return type(y[0])

    def _cast_anomaly_type(self, anomaly, y):
        return anomaly.astype(self._get_input_data_type(y))

    def _generate(self, y):
        self._reset_property_log()

        i = 0
        while i < len(y):
            if not self.anomaly_locations or i in self.anomaly_locations:

                if random.random() < self.anomaly_rate:
                    self._update_properties()
                    anomaly = self._shape()
                    anomaly = self._adjust_amplitude(anomaly)
                    anomaly = self._cast_anomaly_type(anomaly, y)
                    if len(anomaly) + i > len(y):
                        i += 1
                        continue
                    self._log_properties(i, len(anomaly))
                    y[i : i + len(anomaly)] += anomaly
                    i += len(anomaly)
                else:
                    i += 1

        y = self._add_noise(y)

        return y

    def modify_signal(self, y, sample_rate):
        """
        modifies an input signal with anomalies. 
        Args:
            y (array): input time-series data that contains the raw signal values
            sample_rate (int): the sample rate of the raw signal
        """

        self._sample_rate = sample_rate
        return self._generate(copy.deepcopy(y))

    def set_shape(self, func):
        if hasattr(func, "_shape"):
            self._shape = func._shape.__get__(self, Anomaly)

        else:
            self._shape = func

    def set_adjust_amplitude(self, func):
        if hasattr(func, "_adjust_amplitude"):
            self._adjust_amplitude = func._adjust_amplitude.__get__(self, Anomaly)

        else:
            self._adjust_amplitude = func
