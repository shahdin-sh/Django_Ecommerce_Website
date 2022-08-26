from product.models import Product


class ShoppingCart:
    def __init__(self, request):
        # Initializing Cart Functionality
        self.request = request
        self.session = request.session
        shopping_cart = self.session.get('cart')

        if not shopping_cart:
            # getting cart info from this dic below
            self.session['cart'] = {}

        self.shopping_cart = shopping_cart

    def add_to_cart(self, product, quantity=1):
        # add specific product to the shopping cart
        product_id = str(product.id)
        if product_id not in self.shopping_cart:
            self.shopping_cart[product_id] = {'quantity': quantity}
        else:
            self.shopping_cart[product_id]['quantity'] += quantity
        self.save()

    def delete_from_cart(self, product):
        # delete a product from cart
        product_id = str(product.id)
        if product_id in self.shopping_cart:
            del self.shopping_cart[product_id]
            self.save()

    def save(self):
        # save the shopping cart after every change in session
        self.session.modified = True

    def __iter__(self):
        product_ids = self.shopping_cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        shopping_cart = self.shopping_cart.copy()

        for product in products:
            # added product_obj key                        this key_value came from DB
            shopping_cart[str(product.id)]['product_obj'] = product
        for item in shopping_cart.values():
            yield item
