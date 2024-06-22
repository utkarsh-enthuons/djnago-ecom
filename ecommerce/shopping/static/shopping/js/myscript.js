$('#slider1, #slider2, #slider3, #slider4, #slider5').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


// order qty started...
$(".plus-cart").on("click",function(){
    var pid = $(this).attr('data-id')
    var qty = $(this).prev()
    $.ajax({
        type: 'GET',
        url : '/pluscart',
        data: {
            prod_id:pid
        },
        success: function(data){
            qty.text(data.quantity)
            $('.card .card-body .list-group .list-group-item:nth-child(1) span').text("Rs. " + data.amount+".0")
            $('.card .card-body .list-group .list-group-item:nth-child(2) span').text("Rs. " + data.shipping_amount+".0")
            $('.card .card-body .list-group .list-group-item:nth-child(4) span strong').text("Rs. " + data.total_amt+".0")
        }
    })
})
$(".minus-cart").on("click",function(){
    var pid = $(this).attr('data-id')
    var qty = $(this).next()
    var value = parseInt($(this).next().text())
    if (value > 1){
        $.ajax({
            type: 'GET',
            url : '/minuscart',
            data: {
            prod_id:pid
        },
        success: function(data){
            qty.text(data.quantity)
            $('.card .card-body .list-group .list-group-item:nth-child(1) span').text("Rs. " + data.amount+".0")
            $('.card .card-body .list-group .list-group-item:nth-child(2) span').text("Rs. " + data.shipping_amount+".0")
            $('.card .card-body .list-group .list-group-item:nth-child(4) span strong').text("Rs. " + data.total_amt+".0")
            }
        })
    }else{
        alert("Product's quantity can not be less than one.")
    }
})
$(".remove-cart").on("click",function(){
    var pid = $(this).attr('data-id')
    var this_ = $(this).closest(".row")
    $.ajax({
        type: 'GET',
        url : '/removeCart',
        data: {
        prod_id:pid
    },
        success: function(data){
            $('.card .card-body .list-group .list-group-item:nth-child(1) span').text("Rs. " + data.amount+".0")
            $('.card .card-body .list-group .list-group-item:nth-child(2) span').text("Rs. " + data.shipping_amount+".0")
            $('.card .card-body .list-group .list-group-item:nth-child(4) span strong').text("Rs. " + data.total_amt+".0")
            $("#nav_cart span").text(data.cart_len)
            this_.prev().remove()
            this_.remove()
            if (data.cart_len < 1){
                $("#nav_cart span").text(data.cart_len)
                $("#empty-cart .row:nth-child(1)").remove()
                $("#empty-cart").append(data.HTML)
            }
        }
    })
})