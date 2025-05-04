def cart_item_count(request):
    cart = request.session.get('cart', [])
    return {'cart_item_count': len(cart)}
