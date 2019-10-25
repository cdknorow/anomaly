
from anomaly import Anomaly, shape, amplitudes

a = Anomaly(frequency_range=[10,20,30], 
                cycle_range=[2,5],
                amplitude_range=[10, 50, 1000],
                anomaly_rate=.01,
                noise_range=[40, 20],
               anomaly_locations = None)

a.modify_signal(np.arange(0,1000), sample_rate=100))


a.set_shape(shape.Square)
a.set_adjust_amplitude(shape.Pyramid)


a.modify_signal(np.arange(0,1000), sample_rate=100))
