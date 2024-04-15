function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
    }
    return "";
}

let productCards = document.querySelectorAll('.product-card')

productCards.forEach(element => {

    // Add Product To WishLoist
    let wishListIcon = element.querySelector('.wishlist-icon')
        wishListIcon.addEventListener('click', (e)=> {
            e.preventDefault();
            let slug = wishListIcon.dataset.productslug

            wishListIcon.querySelector('svg').classList.toggle('text-gray-800')
            wishListIcon.querySelector('svg').classList.toggle('text-red-500')
            wishListIcon.classList.toggle('bg-green-50')
            wishListIcon.classList.toggle('bg-red-100')

            let wishlist = getCookie('wish_list')
            
            if (wishlist == '') {
                setCookie('wish_list', JSON.stringify([slug]), 3000)
            } else {
                let wishListProducts = JSON.parse(wishlist)
                let whishListCounter = document.querySelector('.wish-list-counter')
                
                if (wishListProducts.indexOf(slug) != -1) {
                    wishListProducts.splice( wishListProducts.indexOf(slug), 1 )
                    whishListCounter.textContent =  parseInt(whishListCounter.textContent) -1
                } else {
                    wishListProducts.push( slug )
                    whishListCounter.textContent =  parseInt(whishListCounter.textContent) +1
                }
                setCookie('wish_list', JSON.stringify(wishListProducts), 3000)
            }
        })
    
    
        // Add Product To Cart
    let addToCartBtns = element.querySelector('.submit-btn')
    addToCartBtns.addEventListener('click', (e) => {
        e.preventDefault()
        let slug = addToCartBtns.dataset.productslug
        let product_id = addToCartBtns.dataset.productid
        let cartProductCount = document.querySelector('.carts-icon span')

        let sizeSelect = element.querySelector('#sizeSelect')
        let sizeSelectId = ''
        if (sizeSelect) {
            sizeSelectId = sizeSelect.options[sizeSelect.selectedIndex].dataset.sizeid    
        }

        addToCartBtns.classList.toggle('text-white')
        addToCartBtns.classList.toggle('bg-blue-500')
        addToCartBtns.classList.toggle('hover:bg-gray-400')
        
        if (user == 'AnonymousUser') {
            addToCartBtns.classList.toggle('px-5')
            let cartProducts = getCookie('cartProduct')
            if (cartProducts == '') {
                setCookie('cartProduct', JSON.stringify([slug]), 3000)
                cartProductCount.textContent = 1
                addToCartBtns.textContent = 'Remove From Cart'
            } else {
                let allCartProducts = JSON.parse(cartProducts)
                
                if (allCartProducts.indexOf(slug) != -1 ) {
                    cartProductCount.textContent = parseInt(cartProductCount.textContent) - 1
                    allCartProducts.splice( allCartProducts.indexOf(slug), 1 )
                    addToCartBtns.textContent = 'Add To Cart'
                } else {
                    allCartProducts.push(slug)
                    cartProductCount.textContent = parseInt(cartProductCount.textContent) + 1
                    addToCartBtns.textContent = 'Remove From Cart'
                    
                }
                setCookie('cartProduct', JSON.stringify(allCartProducts), 3000)
            }
        } else {
            fetch(create_cart_url, {
            method: "post",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken':csrftoken
            },
            //make sure to serialize your JSON body
            body: JSON.stringify({
                'product': product_id,
                'sizeSelectId':sizeSelectId
            })
            })
            .then( (response) => { 
                if (response.status === 201) {
                    addToCartBtns.textContent = 'Remove From Cart'
                    addToCartBtns.classList.toggle('px-5')
                    cartProductCount.textContent = parseInt(cartProductCount.textContent) + 1
                } else if (response.status === 200) {
                    addToCartBtns.textContent = 'Add To Cart'
                    addToCartBtns.classList.toggle('px-5')
                    cartProductCount.textContent = parseInt(cartProductCount.textContent) - 1
                }
            });
        }
    })
});

// Add To Cart 

let calcTotalProductsPrice = () =>{
    let productsTable = document.querySelector('.products-table')
    let total = 0
    if (!productsTable) {return}
    productsTable.querySelectorAll('tbody tr').forEach(element => {
        total += parseInt(element.querySelector(".total").textContent)
    });
    document.querySelector('.subtotal').textContent = total
    document.querySelector('.total-pay').textContent = total + parseInt(document.querySelector(".shipping").textContent)
}
calcTotalProductsPrice()

let calcRowProductPrice = (element) =>{
    let row = element.parentNode.parentNode.parentNode
    let cells = row.querySelectorAll('td')
    cells[3].textContent = cells[1].textContent  * cells[2].querySelector('span').textContent
}


let btns = document.querySelectorAll('.product-qunatity-change ')

btns.forEach(element => {
    element.addEventListener('click', (e) => {
        e.preventDefault()

        let product_id = element.dataset.productid
        let action = element.dataset.action
        let instance = element.dataset.instance
        
        if (user == 'AnonymousUser') {
            addToCartBtns.classList.toggle('px-5')
            let cartProducts = getCookie('cartProduct')
            if (cartProducts == '') {
                setCookie('cartProduct', JSON.stringify([slug]), 3000)
                cartProductCount.textContent = 1
                addToCartBtns.textContent = 'Remove From Cart'
            } else {
                let allCartProducts = JSON.parse(cartProducts)
                
                if (allCartProducts.indexOf(slug) != -1 ) {
                    cartProductCount.textContent = parseInt(cartProductCount.textContent) - 1
                    allCartProducts.splice( allCartProducts.indexOf(slug), 1 )
                    addToCartBtns.textContent = 'Add To Cart'
                } else {
                    allCartProducts.push(slug)
                    cartProductCount.textContent = parseInt(cartProductCount.textContent) + 1
                    addToCartBtns.textContent = 'Remove From Cart'
                    
                }
                setCookie('cartProduct', JSON.stringify(allCartProducts), 3000)
            }
        } else {
            fetch(edit_cart, {
            method: "post",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken':csrftoken
            },
            //make sure to serialize your JSON body
            body: JSON.stringify({
                'product': product_id,
                'action':action,
                'instance':instance
            })
            }).then(response=>response.json())
            .then( (data) => { 
                let msg = data.msg
                let errorMsg = document.getElementById('errorMsg')
                errorMsg.classList.add('hidden')
                if (msg === 'edit') {
                    let quantity_span = element.parentNode.querySelector('span')
                    if (action == 'plus') {
                        quantity_span.textContent = parseInt(quantity_span.textContent) + 1
                    } else {
                        quantity_span.textContent = parseInt(quantity_span.textContent) - 1
                    }
                } else if (msg === 'delete') {
                    element.parentNode.parentNode.parentNode.remove()
                } else if (msg === 'quantityNotAvailalbe') {
                    errorMsg.classList.remove('hidden')
                    errorMsg.textContent = data.msgContent
                    element.querySelectorAll('td')[2].querySelector('span').textContent = data.quatityo
                } else {
                    // TODO Return Error Message
                    errorMsg.classList.remove('hidden')
                    errorMsg.textContent = 
                    errorMsg.textContent = data.msgContent
                }
                calcTotalProductsPrice()
                calcRowProductPrice(element)
            });
        }
    })
});

