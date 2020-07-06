/*
core logic /payment flow for this comes from:
https://stripe.com/docs/payments/accept-a-payment

CSS from: 
https://stripe.com/docs/stripe-js   

*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1)
var clientSecret = $('#id_client_secret').text().slice(1, -1)
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

// Set up Stripe.js and Elements to use in checkout form
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};


var card = elements.create('card', { style: style });
card.mount('#card-element');


// Handle real time validation on the card element

// stripe payment process : Stripe works with what are called payment intents.
//The process will be that when a user hits the checkout page
//the checkout view will call out to stripe and create a payment intent
//for the current amount of the shopping bag.
//When stripe creates it. it'll also have a secret that identifies it.
//Which will be returned to us and we'll send it to the template as the client secret variable.
//Then in the JavaScript on the client side.
//We'll call the confirm card payment method from stripe js.
//Using the client secret which will verify the card number.

//below code renders error from stripe and displays it in the card-errors section in checkout.html
card.addEventListener('change', function(event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html =
            `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);

    } else {
        errorDiv.textContent = '';
    }
});

// handle form submit 

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true });
    $('#submit-button').attr('disabled', true)
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            // Show error to your customer (e.g., insufficient funds)
            var errorDiv = document.getElementById('card-errors');
            var html =
                `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            card.update({ 'disabled': false }); //if there's an error. We'll also want to re-enable the card element and the submit button to allow the user to fix it.
            $('#submit-button').attr('disabled', false)
        } else {
            // The payment has been processed!
            if (result.paymentIntent.status === 'succeeded') {
                form.submit(); // if succesful submit form
            }
        }
    });
});