
    const itemsList = document.getElementById('popcartpr')
    //find the the cart from localstorage
    if (localStorage.getItem('cart') == null) {
        var cart = {};
    } else {
        cart = JSON.parse(localStorage.getItem('cart'));
        updateCart(cart);
    }
    function updatePopover(cart) {
        console.log("we are inside popover");
        var popStr = "";
        var i = 1;
        var total = 0;
        var price = 0
        console.log(cart)
        for (var item in cart) {
            if (cart[item].qyt == 0) {
                popStr = popStr + "";                
            } else {
                popStr = popStr + "<div class='card-mini-product rmdiv' id='rm" + item +
                    "'><div class='mini-product'><div class='mini-product__image-wrapper'><a class='mini-product__link' href='product-detail.html'><img class='u-img-fluid' src='" +
                        cart[item][2] +
                    "' alt=''></a></div><div class='mini-product__info-wrapper'><span class='mini-product__category'><a href='shop-side-version-2.html'>" +
                        cart[item][4] +
                    "</a></span><span class='mini-product__name'><a href='product-detail.html'>" + cart[item][1] + "</a></span><span class='mini-product__quantity' id='for_qty'>" +
                    cart[item][0] + " </span>x<span class='mini-product__price'>&#8377; " + cart[item][3] +
                    "</span></div></div><a class='mini-product__delete-link far fa-trash-alt popremove' id='rmdl" +
                    item + "' ></a></div><input type='hidden' name='prod_id_for_checkout[]' value='" +
                    cart[item][8] + "'><input type='hidden' name='prod_qty_for_checkout[]' value='" +
                    cart[item][0] + "'>";
            }
            i = i + 1;
            var qty = cart[item][0];
            price = cart[item][3]
            subtotal = qty * price;
            total = total + subtotal;
            console.log(price)
            console.log(subtotal)
            console.log(total)
        }
        document.getElementById('popcartpr').innerHTML = popStr;
        if (i == 1) {
            document.getElementById('popcartpr-total').innerHTML = "Cart is Empty "
        } else {
            console.log(cart)
            document.getElementById('popcartpr-total').innerHTML = `<div class="mini-total">

                <span class="subtotal-text">SUBTOTAL</span>
    
                <span class="subtotal-value">&#8377; ${total}</span></div>
            <div class="mini-action">
    
                <a class="mini-link btn--e-brand-b-2" href="/checkout">PROCEED TO CHECKOUT</a>
                <a class="mini-link btn--e-transparent-secondary-b-2" href="/cart" >View Cart</a></div>`;
        }

        document.getElementById('popcartpr').innerHTML = popStr;
    }

   
    //remove one element or product form cart 
    $('.popcartpr').on("click", "a.popremove", function () {
        a = this.id.slice(4, );
        console.log("inside remove fuction")
       
            if(user != 'AnonymousUser'){
                var url = "{% url 'add-to-cart' %}"
                fetch(url,{
                    method:'POST',
                    headers: {
                        'Content-Type':'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body:JSON.stringify({'item':cart[a][8],'quantity':0})
        
                })
                .then((response)=>{
                    return response.json()
                })
                .then((data)=>{
                    console.log('data:',data)
                })
            }
        delete cart[a]
        localStorage.setItem('cart', JSON.stringify(cart));
        console.log("now we are exit")
        updateCart(cart);

    });
    // Html Code replace with plus minus button updating cart in localStorage
    function updateCart(cart) {
        var sum = 0;
        console.log(cart)
        for (var item in cart) {
            sum = sum + cart[item][0];
        }
        localStorage.setItem('cart', JSON.stringify(cart));
        //document.getElementById('cart').innerHTML = Object.keys(cart).length; only for product added to cart item to display for instance product1 3 ,product4 6 total added 2 product only
        //Ajax
       
        //end Ajax
        //here is total number of item added likeproduct1 3 product4 5 and product2 6 total 14 display
        document.getElementById('cart').innerHTML = sum;
        updatePopover(cart);
    }
