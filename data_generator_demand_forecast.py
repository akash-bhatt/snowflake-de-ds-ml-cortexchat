import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_grocery_demand_data(num_weeks=52, num_products=30):
    """
    Generate synthetic grocery store demand data for a single store.
    
    Parameters:
    - num_weeks: Number of weeks of historical data to generate (counting backwards from today)
    - num_products: Number of different products (default 30)
    """
    
    # Calculate date range
    end_date = pd.Timestamp.today()
    start_date = end_date - pd.Timedelta(weeks=num_weeks)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Define product categories with their characteristics and real products
    category_specs = {
        'Dairy': {
            'is_perishable': True,
            'shelf_life': (5, 14),
            'base_price': (2.99, 8.99),
            'products': [
                'Organic Whole Milk 1gal',
                'Greek Yogurt 32oz',
                'Cheddar Cheese Block 8oz',
                'Heavy Cream 16oz',
                'Butter Unsalted 16oz',
                'Cottage Cheese 16oz'
            ]
        },
        'Produce': {
            'is_perishable': True,
            'shelf_life': (3, 10),
            'base_price': (1.99, 12.99),
            'products': [
                'Organic Bananas 1lb',
                'Roma Tomatoes 1lb',
                'Russet Potatoes 5lb',
                'Baby Spinach 10oz',
                'Avocado',
                'Red Bell Pepper'
            ]
        },
        'Bakery': {
            'is_perishable': True,
            'shelf_life': (1, 5),
            'base_price': (2.99, 15.99),
            'products': [
                'Artisan Sourdough Bread',
                'Whole Wheat Bread',
                'Chocolate Croissant',
                'Bagels 6pk',
                'Blueberry Muffins 4pk'
            ]
        },
        'Meat': {
            'is_perishable': True,
            'shelf_life': (3, 7),
            'base_price': (5.99, 25.99),
            'products': [
                'Ground Beef 80/20 1lb',
                'Chicken Breast 1lb',
                'Pork Chops 1lb',
                'Salmon Fillet 1lb',
                'Turkey Breast 1lb'
            ]
        },
        'Household': {
            'is_perishable': False,
            'shelf_life': (90, 365),
            'base_price': (3.99, 19.99),
            'products': [
                'Paper Towels 6rolls',
                'Dish Soap 16oz',
                'Laundry Detergent 100oz',
                'Trash Bags 30ct',
                'All-Purpose Cleaner 32oz'
            ]
        },
        'Canned Goods': {
            'is_perishable': False,
            'shelf_life': (180, 730),
            'base_price': (1.99, 9.99),
            'products': [
                'Diced Tomatoes 14.5oz',
                'Black Beans 15oz',
                'Tuna in Water 5oz',
                'Corn 15.25oz',
                'Chicken Soup 10.5oz'
            ]
        }
    }
    
    # Generate product information
    products = []
    remaining_products = num_products
    categories = list(category_specs.keys())
    
    # Distribute products across categories
    while remaining_products > 0:
        for category in categories:
            if remaining_products <= 0:
                break
            # Select 1-3 products from each category, but not more than remaining
            num_from_category = min(random.randint(1, 3), remaining_products)
            available_products = category_specs[category]['products']
            
            # Randomly select products from this category
            selected_products = random.sample(available_products, min(num_from_category, len(available_products)))
            specs = category_specs[category]
            
            for product_name in selected_products:
                shelf_life = random.randint(*specs['shelf_life'])
                base_price = round(random.uniform(*specs['base_price']), 2)
                products.append({
                    'product_id': product_name,
                    'category': category,
                    'is_perishable': specs['is_perishable'],
                    'shelf_life': shelf_life,
                    'base_price': base_price
                })
                remaining_products -= 1
    products_df = pd.DataFrame(products)
    
    # Generate data
    data = []
    
    for date in dates:
        # Get day of week
        day_of_week = date.dayofweek
        is_weekend = 1 if day_of_week >= 5 else 0
        
        # Weather factors (simplified)
        temperature = 20 + 15 * np.sin(2 * np.pi * (date.dayofyear / 365)) + random.uniform(-5, 5)
        is_rainy = random.random() < 0.3
        
        for _, product in products_df.iterrows():
            # Base demand calculation
            base_demand = random.randint(10, 50)
            
            # Adjust for weekends
            if is_weekend:
                base_demand *= 1.3
            
            # Seasonal adjustments
            seasonal_factor = 1.0 + 0.2 * np.sin(2 * np.pi * (date.dayofyear / 365))
            
            # Weather impact - only affects perishables
            weather_factor = 1.0
            if product['is_perishable']:
                weather_factor = 0.9 if is_rainy else 1.0
                if product['category'] in ['Dairy', 'Produce']:
                    weather_factor *= 1.0 + (temperature - 20) / 50
            
            # Promotional status (random)
            is_promotional = random.random() < 0.1
            promo_discount = round(random.uniform(0.1, 0.3), 2) if is_promotional else 0
            
            # Final demand calculation with some randomness
            final_demand = int(base_demand * seasonal_factor * weather_factor * (1.3 if is_promotional else 1.0))
            final_demand = max(0, int(np.random.normal(final_demand, final_demand * 0.1)))
            
            # Calculate actual sales (might be less than demand due to stock limitations)
            stock_level = int(final_demand * random.uniform(0.8, 1.2))
            actual_sales = min(final_demand, stock_level)
            
            # Calculate price
            price = product['base_price'] * (1 - promo_discount)
            
            # Calculate waste (only for perishable items)
            waste = max(0, stock_level - actual_sales) if product['is_perishable'] else 0
            
            data.append({
                'date': date,
                'product_id': product['product_id'],
                'product_category': product['category'],
                'is_perishable': product['is_perishable'],
                'shelf_life': product['shelf_life'],
                'temperature': round(temperature, 2),
                'is_rainy': is_rainy,
                'is_weekend': is_weekend,
                'is_promotional': is_promotional,
                'discount_pct': promo_discount * 100,
                'price': round(price, 2),
                'demand': final_demand,
                'stock_level': stock_level,
                'actual_sales': actual_sales,
                'waste': waste
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # Generate 12 weeks of data with 30 products
    df = generate_grocery_demand_data(
        num_weeks=12,
        num_products=30
    )
    
    # Convert date to YYYY-MM-DD format
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    
    # Create demand_data directory if it doesn't exist
    output_dir = 'demand_data'
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'grocery_demand_data_{timestamp}.csv'
    filepath = os.path.join(output_dir, filename)
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    print(f"Generated {len(df)} records of demand data for the last {12} weeks")
    print(f"Saved to file: {filepath}")
    
    # Print category distribution
    print("\nProduct distribution across categories:")
    category_dist = df.groupby('product_category')['product_id'].nunique()
    print(category_dist)
    
    print("\nSample data:")
    print(df.head())
    
    print("\nData summary:")
    print(df.describe())
