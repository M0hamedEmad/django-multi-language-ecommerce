
var elements = stripe.elements();
var style = {
base: {
    color: "#32325d",
    }
};

var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', ({error}) => {
let displayError = document.getElementById('card-errors');
if (error) {
    displayError.textContent = error.message;
} else {
    displayError.textContent = '';
}
});


// Handle form submission.
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
    var payMethod = document.querySelector('input[name="pay_method"]:checked').value
    event.preventDefault();
    stripe.createPaymentMethod({
        type: 'card',
        card: card,
    }).then(function(result) {
        if (result.error & payMethod !== 'cash') {
            // Show error in `card-errors` element.
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
        } else {
            // Send paymentMethod.id to your server.
            // This is a PaymentMethod ID that you can use to complete the payment.
            console.log(payMethod)
            if (payMethod !== 'cash') {
                var paymentMethodId = result.paymentMethod.id;
            } else {
                var paymentMethodId = '';
            }
            document.getElementById('paymentMethodId').value = paymentMethodId
            form.submit()
            // Send the paymentMethodId to your server to complete the payment.
            // For example, you can use AJAX to send an HTTP request to your Django view.
        }
    });
});


document.querySelectorAll('input[name="pay_method"]').forEach(element => {
    element.addEventListener('click', () => {
        if (element.value === 'cash') {
            document.getElementById('card-element').classList.add('hidden')
            document.getElementById('card-errors').classList.add('hidden')
        } else {
            document.getElementById('card-element').classList.remove('hidden')
            document.getElementById('card-errors').classList.remove('hidden')
        }
    } )
});
