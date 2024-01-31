import matplotlib.pyplot as plt

# Data for the chart
categories = ["Web", "System", "Malware"]
values = [33.33, 33.33, 33.33]
colors = ["skyblue", "limegreen", "tomato"]

# Create a pie chart with equal aspect ratio
wedges, texts = plt.pie(values, colors=colors, startangle=90, wedgeprops=dict(width=0.65))

# Create a circle for the donut hole
centre_circle = plt.Circle((0, 0), 0.4, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Add labels for each segment
plt.legend(wedges, categories, loc="best")

# Add title
plt.title("Distribution of Security Threats", fontsize=16)

# Equal aspect ratio ensures a circular shape
plt.axis('equal')

# Display the chart
plt.show()