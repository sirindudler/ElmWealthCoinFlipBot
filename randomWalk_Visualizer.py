from matplotlib import ticker
import matplotlib.pyplot as plt

# Read data from file
with open("CoinFlipGameData.txt", "r") as file:
    data = file.read()

# Split the data into lines
lines = data.split("\n")

# Filter out empty lines and the header
lines = [line for line in lines if line and not line.startswith("#")]

# Parse the values
values = [float(line) for line in lines[::2]]

# Format y-axis labels
formatter = ticker.FuncFormatter(lambda x, pos: f'{x*1e-3:.0f}k')
plt.gca().yaxis.set_major_formatter(formatter)


# Plot the data
plt.plot(values)
plt.show()