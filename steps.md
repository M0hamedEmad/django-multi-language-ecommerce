
# Product App
    - collection page
    - products page
    - product page
    - wishlist
    - cart

## models:
    collection:
        image
        name
        created
        slug

    category:
        image
        name
        created
        slug
        collection

    product:
        name
        dicsription
        category
        price
        image
        created
        updated
        slug
        size_and_qunatiy
        tags


    size and qunatity
        *avilabe_sizes
        *availabl_quantity

#Store
    home page
    wishlist
    carts

    models:

    
    carts:
        user
        product
        size
        quantity
        created

    whishlist:
        user
        product

    shippers:
        name
        phone


    order:
        customer
        status
        shipping
        paid
        payment_data
        created_at

    

    order_item:
        product
        size
        quantity
        price
        order
