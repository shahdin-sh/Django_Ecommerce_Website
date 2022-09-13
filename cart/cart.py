from product.models import Product


class ShoppingCart:
    def __init__(self, request):
        # Initializing Cart Functionality
        self.request = request
        self.session = request.session
        shopping_cart = self.session.get('shopping_cart')

        if not shopping_cart:
            # getting cart info from this dic below
            self.session['shopping_cart'] = {}
        self.shopping_cart = self.session['shopping_cart']

    def add_to_cart(self, product, quantity=1, replace_current_quantity=False):
        # add specific product to the shopping cart
        product_id = str(product.id)
        if product_id not in self.shopping_cart:
            self.shopping_cart[product_id] = {'quantity': 0}
        if replace_current_quantity:
            self.shopping_cart[product_id]['quantity'] = quantity
        else:
            self.shopping_cart[product_id]['quantity'] += quantity
        self.save()

    def delete_from_cart(self, product):
        # delete a product from cart
        product_id = str(product.id)
        if product_id in self.shopping_cart:
            del self.shopping_cart[product_id]
            self.save()

    def emptying_the_cart(self):
        del self.session['shopping_cart']
        self.save()

    def save(self):
        # save the shopping cart after every change in session
        self.session.modified = True

    def __iter__(self):
        product_ids = self.shopping_cart.keys()
        products = Product.product_manager.filter(id__in=product_ids)

        shopping_cart = self.shopping_cart.copy()

        for product in products:
            # added product_obj key                        this key_value came from DB
            shopping_cart[str(product.id)]['product_obj'] = product
        for item in shopping_cart.values():
            item['total_price'] = item['product_obj'].product_price * item['quantity']
            yield item

    def __len__(self):
        # return all amount of products that would save in shopping cart
        return sum(item['quantity'] for item in self.shopping_cart.values())

    def clear(self):
        del self.session['shopping_cart']
        self.save()

    def get_total_price(self):
        product_ids = self.shopping_cart.keys()

        return sum(item['quantity'] * item['product_obj'].product_price for item in self.shopping_cart.values())

    def is_cart_empty(self):
        if self.shopping_cart == {}:
            return True
        else:
            return False