def ProductSerializer(name,item_link, image_path, price, prev_price, item_reviews,rating, per_discount):
    return{"product_name":name, "item_link":item_link, 
           "image_src":image_path, "price":price, 
           "prev_price":prev_price, "item_review":item_reviews,
           "rating":rating, 'per_discount':per_discount
          }


def fillForm(message_box, message):
    for i in range(len(message)):
        message_box.send_keys(message[i])
        time.sleep(0.05)