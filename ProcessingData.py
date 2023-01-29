import os
import matplotlib.pyplot as plt
import ProcessingUtilities as Pu

# plt.plot(os.listdir("./Reports/"), Pu.return_mean_price_history(oras="Cluj-Napoca", no_camere=3))

plt.plot(os.listdir("./Reports/"), Pu.return_mean_price_mp_history(oras="Cluj-Napoca", no_camere=3))

plt.show()
