import pandas as pd
import numpy as np

# Parameters
num_sessions = 100000
num_users = 5000
tv_sizes = [32, 40, 50, 55, 65, 75]
brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD']
resolutions = ['HD', 'Full HD', '4K', '8K']
price_range = {'low': [200, 500], 'mid': [501, 1000], 'high': [1001, 3000]}

# Generate sessions
sessions = []
for i in range(num_sessions):
    session_id = i + 1
    user_id = np.random.randint(1, num_users + 1)
    tv_size = np.random.choice(tv_sizes)
    brand = np.random.choice(brands)
    resolution = np.random.choice(resolutions)
    price = np.random.randint(*price_range[np.random.choice(['low', 'mid', 'high'])])
    action = np.random.choice(['view', 'click', 'purchase'], p=[0.7, 0.2, 0.1])
    timestamp = pd.Timestamp.now() - pd.to_timedelta(np.random.randint(0, 30*24*60), unit='m')
    
    sessions.append([session_id, user_id, tv_size, brand, resolution, price, action, timestamp])

# Create DataFrame
columns = ['session_id', 'user_id', 'tv_size', 'brand', 'resolution', 'price', 'action', 'timestamp']
df = pd.DataFrame(sessions, columns=columns)

# Save to CSV (optional)
df.to_csv('ecommerce_sessions.csv', index=False)