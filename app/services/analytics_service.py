from app.models.product import Product
from app import mongo, elastic
from elasticsearch import exceptions

class AnalyticsService:

  @staticmethod
  def generate_product_report():
      # Get the total number of products
      total_products = Product.count_all()

      # Get the most popular category
      category_group = mongo.db.products.aggregate([
        {"$group": {"_id": "$ProductCategory", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
      ])
      
      # Get the average price
      price_ave = mongo.db.products.aggregate([
          {
              '$group': {
                  '_id': 'average_price',
                  'average': {
                      '$avg': '$Price'
                  }
              }
          }
      ])

      # Get average wordcount from Elasticsearch
      query = {
        # "type": "_search",
        "size": 0,
        "aggs": {
            "avg_word_count": {
                "avg": {
                "field": "word_count"
                }
            }
        }
    }
      elastic.search(index="products", body=query)
      avg_word_count = elastic.search(index="products", body=query)
      word_count = avg_word_count['aggregations']['avg_word_count']['value']

      # Extract the results
      popular_category = list(category_group)
      if len(popular_category) > 0:
          popular_category = popular_category[0]['_id']
      else:
          popular_category = "N/A"

      avg_price = list(price_ave)
      if len(avg_price) > 0:
        avg_price = round(int(avg_price[0]['average']) / 100, 2)
        # avg_price = 0
      else:
          avg_price = "N/A"

      # Return the report
      report = {
          "total_products": total_products,
          "popular_category": popular_category,
          "avg_price": avg_price,
          "avg_description_word_count": word_count
      }
      return report
