import matplotlib.pyplot as plt
import numpy as np

# Data
tasks = ['100 Emails', '1000 Emails']
ai_water_ml = np.array([10*100, 10*1000])       # 10 mL per email × number of emails
non_ai_water_ml = np.array([0.3*100, 0.3*1000]) # 0.3 mL per email × number of emails

# Convert to liters
ai_water_l = ai_water_ml / 1000
non_ai_water_l = non_ai_water_ml / 1000

x = np.arange(len(tasks))
width = 0.35

fig, ax = plt.subplots(figsize=(8,5))  # Original size
bars1 = ax.bar(x - width/2, ai_water_l, width, label='AI Emails', color='#4C72B0')  # ChatGPT color
bars2 = ax.bar(x + width/2, non_ai_water_l, width, label='Non-AI Emails', color='#55A868')

# Labels and title
ax.set_ylabel('Water Usage (Liters)')
ax.set_title('Water Usage: AI vs Non-AI Emails')
ax.set_xticks(x)
ax.set_xticklabels(tasks)
ax.set_ylim(0, 11)  # Extend y-axis to 11 L
ax.legend()

# Add bar labels (ml and liters) with smaller fontsize
for b, ml in zip(bars1, ai_water_ml):
    ax.text(b.get_x() + b.get_width()/2, b.get_height(), f'{ml} mL\n{b.get_height():.2f} L', 
            ha='center', va='bottom', fontsize=9)
for b, ml in zip(bars2, non_ai_water_ml):
    ax.text(b.get_x() + b.get_width()/2, b.get_height(), f'{ml} mL\n{b.get_height():.2f} L', 
            ha='center', va='bottom', fontsize=9)

plt.tight_layout()

# Save and show
plt.savefig('Emails_BarChart.png')
plt.show()
