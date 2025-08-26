import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import uuid
import random

# Define review templates for different sentiments
POSITIVE_REVIEWS = [
    "Excellent quality and consistently fresh. The packaging keeps everything well-preserved, and the portion size is perfect for our family needs. Highly recommended!",
    "Outstanding product that exceeds expectations in every way. The quality is exceptional, and the price point makes it an incredible value for daily use.",
    "This has become our family favorite due to its consistent quality and great taste. The freshness lasts longer than other brands, making it worth every penny.",
    "Absolutely impressed with the premium quality and excellent packaging. The product stays fresh for days, and the taste is consistently delicious. Will keep buying!",
    "Superior product that delivers on all promises. The quality has been consistently high, and it's perfectly portioned. A fantastic addition to our regular shopping.",
    "Remarkable freshness and exceptional taste that lasts. The packaging is eco-friendly, and the product quality is outstanding. Definitely worth the premium price.",
    "Best quality I've found in the market. The freshness is unmatched, and the taste is consistently excellent. Perfect portion size for our needs.",
    "A game-changer in terms of quality and value. The product maintains freshness exceptionally well, and the taste is superior to other brands we've tried."
]

NEGATIVE_REVIEWS = [
    "Disappointing quality and freshness issues. The packaging was damaged upon arrival, and the product didn't meet basic quality standards. Not worth the premium price.",
    "Product quality has significantly declined recently. The portion size seems smaller, and the taste isn't what it used to be. Definitely not worth the current price.",
    "Very frustrated with inconsistent quality. Sometimes it's fresh, but lately it's been arriving close to expiration. The price is too high for such poor quality.",
    "Extremely disappointed with recent changes. The quality has dropped noticeably, and the packaging often arrives damaged. Will be switching to a different brand.",
    "Poor value for money and subpar quality. The product spoils quickly despite proper storage, and the taste is below average. Not recommended at current prices.",
    "Major quality control issues evident. The product arrives in varying states of freshness, and the packaging is often compromised. Looking for alternatives now.",
    "Unsatisfactory experience overall. The quality is inconsistent, and the price keeps increasing while portions seem to shrink. Not meeting basic expectations anymore.",
    "Completely disappointed with recent purchases. Quality has become unpredictable, and customer service hasn't been helpful. Looking for better alternatives now."
]

MIXED_REVIEWS = [
    "Decent quality but somewhat overpriced. While the product is fresh and tastes good, the recent price increase makes it less attractive for regular purchase.",
    "Good product overall, though packaging needs improvement. The quality is consistent, but the container often arrives damaged. Still worth buying when on sale.",
    "Like the product but concerned about price increases. Quality remains good, but becoming too expensive for regular purchase. Would buy more if price was better.",
    "Fresh and tasty, but portion size is disappointing. While quality is good, they've reduced the quantity significantly. Considering alternatives due to pricing.",
    "Quality is generally good but consistency is an issue. Sometimes excellent, sometimes just okay. Wish they would maintain better quality control.",
    "Satisfied with taste but not with packaging. Product is fresh and flavorful, but the container design leads to damage during transit. Needs improvement.",
    "Good quality product with room for improvement. Taste and freshness are reliable, but price point and packaging could be better. Still recommend with reservations.",
    "Mostly positive experience with minor issues. Product quality is good but shelf life is shorter than expected. Would rate higher if they improved preservation."
]

def generate_sales_and_reviews():
    # Read the most recent grocery demand data file
    demand_files = sorted([f for f in os.listdir('demand_data') if f.startswith('grocery_demand_data')])
    if not demand_files:
        raise FileNotFoundError("No demand data files found")
    
    df = pd.read_csv(f'demand_data/{demand_files[-1]}')
    
    # Get unique products with their categories and prices
    products_df = df.groupby(['product_id', 'product_category'])['price'].mean().reset_index()
    
    # Calculate 12-week sales
    df['sale_dollars'] = df['actual_sales'] * df['price']
    sales_by_product = df.groupby('product_id')['sale_dollars'].sum().reset_index()
    
    # Generate sales metrics
    sales_metrics = products_df.merge(sales_by_product, on='product_id')
    sales_metrics['inventory_status'] = np.random.choice(['Low', 'Medium', 'High'], size=len(sales_metrics))
    sales_metrics.columns = ['product_id', 'product_category', 'unit_price_dollars', '12_week_sale_dollars', 'inventory_status']
    
    # Round price and sales to 2 decimal places
    sales_metrics['unit_price_dollars'] = sales_metrics['unit_price_dollars'].round(2)
    sales_metrics['12_week_sale_dollars'] = sales_metrics['12_week_sale_dollars'].round(2)
    
    # Generate reviews
    reviews = []
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=12)
    
    for _, row in sales_metrics.iterrows():
        product_id = row['product_id']
        product_category = row['product_category']
        num_reviews = random.randint(3, 7)  # Random number of reviews per product
        for _ in range(num_reviews):
            review_date = start_date + timedelta(days=random.randint(0, 84))
            sentiment = random.choice(['positive', 'negative', 'mixed'])
            if sentiment == 'positive':
                review_text = random.choice(POSITIVE_REVIEWS)
            elif sentiment == 'negative':
                review_text = random.choice(NEGATIVE_REVIEWS)
            else:
                review_text = random.choice(MIXED_REVIEWS)
            
            reviews.append({
                'review_id': str(uuid.uuid4()),
                'product_id': product_id,
                'product_category': product_category,
                'review_text': review_text,
                'review_date': review_date.strftime('%Y-%m-%d')
            })
    
    reviews_df = pd.DataFrame(reviews)
    
    # Create review_data directory if it doesn't exist
    os.makedirs('review_data', exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save files
    sales_metrics.to_csv(f'review_data/product_sales_metrics_{timestamp}.csv', index=False)
    reviews_df.to_csv(f'review_data/product_reviews_{timestamp}.csv', index=False)
    
    return sales_metrics.shape[0], len(reviews)

if __name__ == "__main__":
    num_products, num_reviews = generate_sales_and_reviews()
    print(f"Generated sales metrics for {num_products} products")
    print(f"Generated {num_reviews} customer reviews")
    print("Files saved in review_data directory")