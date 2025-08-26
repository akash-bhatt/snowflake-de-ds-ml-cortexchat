import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import uuid

def generate_product_description(product_name, category):
    """Generate a natural-sounding description for a product."""
    
    quality_terms = {
        'Dairy': ['Fresh', 'Organic', 'Farm-fresh', 'Premium', 'All-natural'],
        'Produce': ['Fresh', 'Organic', 'Local', 'Hand-picked', 'Seasonal'],
        'Bakery': ['Freshly baked', 'Artisanal', 'Homestyle', 'Hand-crafted', 'Traditional'],
        'Meat': ['Fresh', 'Premium', 'Farm-raised', 'All-natural', 'Hand-selected'],
        'Household': ['Premium', 'Heavy-duty', 'Long-lasting', 'Professional-grade', 'Extra-strength'],
        'Canned Goods': ['Premium', 'All-natural', 'Preservative-free', 'Organic', 'High-quality']
    }
    
    benefit_terms = {
        'Dairy': ['rich in calcium', 'protein-packed', 'essential nutrients', 'probiotic-rich', 'vitamin D fortified'],
        'Produce': ['locally sourced', 'nutrient-rich', 'vitamin-packed', 'farm to table', 'pesticide-free'],
        'Bakery': ['made fresh daily', 'no preservatives', 'whole grain', 'traditional recipe', 'naturally leavened'],
        'Meat': ['lean protein', 'hormone-free', 'ethically raised', 'premium cut', 'grass-fed'],
        'Household': ['eco-friendly', 'biodegradable', 'long-lasting', 'tough on dirt', 'gentle on surfaces'],
        'Canned Goods': ['no additives', 'BPA-free can', 'packed at peak freshness', 'ready to serve', 'sustainable sourced']
    }
    
    quality = random.choice(quality_terms[category])
    benefit = random.choice(benefit_terms[category])
    
    description = f"{quality} {product_name}, {benefit}"
    return description

def generate_promotional_data(num_products=30):
    """
    Generate promotional data for grocery store products.
    
    Parameters:
    - num_products: Number of different products (default 30)
    """
    
    # Define product categories with their characteristics and real products
    category_specs = {
        'Dairy': {
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
    
    # Calculate promotion dates
    today = datetime.now().date()
    # Find next Monday
    days_ahead = 0 - today.weekday() + 7  # +7 to get next week's Monday
    promo_start = today + timedelta(days=days_ahead)
    promo_end = promo_start + timedelta(days=6)
    
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
                base_price = round(random.uniform(*specs['base_price']), 2)
                
                # Generate promotional details
                discount_type = random.choice(['percentage', 'fixed', 'bogo'])
                if discount_type == 'percentage':
                    discount_pct = random.choice([10, 15, 20, 25, 30])
                    discount_price = round(base_price * (1 - discount_pct/100), 2)
                    promo_text = f"{discount_pct}% off"
                elif discount_type == 'fixed':
                    discount_amount = round(random.uniform(0.5, 2), 2)
                    discount_price = max(round(base_price - discount_amount, 2), 0.99)
                    promo_text = f"${discount_amount:.2f} off"
                else:  # BOGO
                    discount_price = base_price
                    promo_text = random.choice(['Buy One Get One Free', 'Buy 2 Get 1 Free'])
                
                products.append({
                    'promo_id': str(uuid.uuid4()),
                    'product_id': product_name,
                    'category': category,
                    'description': generate_product_description(product_name, category),
                    'regular_price': base_price,
                    'promo_price': discount_price,
                    'promo_text': promo_text,
                    'promo_type': discount_type,
                    'start_date': promo_start,
                    'end_date': promo_end,
                    'quantity_limit': random.choice([0, 2, 4, 6]) if discount_type == 'bogo' else 0,  # 0 means no limit
                    'featured_item': random.random() < 0.2,  # 20% chance to be featured
                    'member_only': random.random() < 0.3,  # 30% chance to be member-only deal
                    'aisle_number': random.randint(1, 20),
                    'inventory_status': random.choice(['High', 'Medium', 'Low'])
                })
                remaining_products -= 1
    
    # Convert to DataFrame
    df = pd.DataFrame(products)
    return df

if __name__ == "__main__":
    # Generate promotional data for 30 products
    df = generate_promotional_data(num_products=30)
    
    # Create promo_data directory if it doesn't exist
    output_dir = 'promo_data'
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'grocery_promo_data_{timestamp}.csv'
    filepath = os.path.join(output_dir, filename)
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    print(f"Generated promotional data for {len(df)} products")
    print(f"Saved to file: {filepath}")
    
    # Print category distribution
    print("\nProduct distribution across categories:")
    category_dist = df.groupby('category')['product_id'].count()
    print(category_dist)
    
    # Print promotion types distribution
    print("\nPromotion types distribution:")
    promo_dist = df.groupby('promo_type')['product_id'].count()
    print(promo_dist)
    
    print("\nSample data:")
    print(df[['product_id', 'description', 'regular_price', 'promo_price', 'promo_text', 'start_date', 'end_date']].head())
