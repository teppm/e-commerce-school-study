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
        var html = `
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
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    //get the boolean value of the saved info box by just looking at its checked attribute
    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    //We'll also need the CSRF token which we can get from the input that Django generates on our form.
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    //Then let's create a small object to pass this information to the new view.
    //And also pass the client secret for the payment intent.
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    }
    var url = '/checkout/cache_checkout_data/';
    // post this data to the view.
    //To do this we'll use our trusty post method built into jQuery
    $.post(url, postData).done(function() {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            },
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
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                card.update({ 'disabled': false }); //if there's an error. We'll also want to re-enable the card element and the submit button to allow the user to fix it.
                $('#submit-button').attr('disabled', false)
            } else {
                // The payment has been processed!
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit(); // if succesful submit form
                }
            }
        }); //attach a failure function, which will be triggered
        //if our view sends a 400 bad request response. And in that case, we'll just
        // reload the page to show the user the error message from the view.
    }).fail(function() {
        location.reload()
    })
});



// steps: 
//When the user clicks the submit button the event listener prevents the form from submitting
//and instead disables the card element and triggers the loading overlay.
//Then we create a few variables to capture the form data we can't put in
//the payment intent here, and instead post it to the cache_checkout_data view
//The view updates the payment intent and returns a 200 response, at which point we
//call the confirm card payment method from stripe and if everything is ok
//submit the form.
//If there's an error in the form then the loading overlay will
//be hidden the card element re-enabled and the error displayed for the user.
//If anything goes wrong posting the data to our view. We'll reload the page and
//display the error without ever charging the user.