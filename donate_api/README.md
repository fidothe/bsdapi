Blue State Digital Donate API (version 1)
=========================================

The BSD donate API allows you to construct your own donation form, submit
contributions via AJAX and get back a JSON response.

Request and Response Formats
----------------------------

### Request ###

Requests to this API must be made with *HTTPS POST*.

The REST endpoint URL is:

    https://DOMAIN/page/cde/Contribution/Api/v1

The POST params will be exactly the same as what is currently on BSD hosted
contribution pages. All validation rules as set in the Control Panel will be run
so be sure to create and submit all required fields.

We can only support SSL encrypted POSTs to the above endpoint due to PCI
requirements. Card numbers must never be sent via GET.

### Response ###

Responses will be in JSON format. JSONP is not supported for PCI and security
reasons.

API Methods
-----------

This API only supports one method. The method is processing a donation. Since 
there is only one method, you do not need to specify a method. To process a 
donation, send an HTTPS POST request to the endpoint mentioned above with the 
following arguments.

### Arguments ###

* **`slug`** (required)

  The slug of the BSD donation form under which the donation should be
  processed.

* **`submission_key`** (optional)

  A unique per page view key that the system will de-dupe on. If nothing is
  submitted the dupe checker is disabled.

* **`firstname`** (required)

  The user's first name.

* **`lastname`** (required)

  The user's last name.

* **`addr1`** (required)

  The first line of the user's billing address.

* **`addr2`** (optional)

  The second line of the user's billing address.

* **`city`** (required)

  The city of the user's billing address.

* **`state_cd`** (required)

  The state of the user's billing address. For United States this is the two
  letter state abbreviation, rules for international addresses vary. 

* **`zip`** (required/local specific)

  The zip or postal code of the user's billing address. This is required unless
  the local specified by the `country` and `state_cd` fields does not have a
  post code.

* **`country`** (required)

  The two letter [ISO 3166-1 alpha-2] country code of the user's address. (US
  for United States)

[ISO 3166-1 alpha-2]: http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

* **`email`** (conditional)

  The user's email address.
  
  If this is set to required in the BSD donation form, then it should be 
  required.

* **`phone`** (conditional)

  The user's phone number.

  If this is set to required in the BSD donation form, then it should be 
  required.

* **`amount`** (required)

  Because of the BSD payment processor this must be set to a value of a 
  preconfigured amount in the BSD donation form or to the value of `other`
  and the amount must be passed as the `amount_other` argument mentioned below.
  
  When using the donate API it is best practice to always set this as `other` 
  and use the `amount_other` argument (below) to specify the donation amount for 
  maximum flexibility.

* **`amount_other`** (required)

  The donation amount selected by the user. Float value to the hundredth decimal 
  point. Examples: 10.00, 20.12

* **`quick_donate_populated`** (optional)

  The user's temporary, encoded payment token that is returned with the BSD 
  getToken JSONP endpoint. Required if no credit card information will be 
  passed.

* **`cc_number`** (required)

  The user's credit card number. If using a payment token the value should be 
  the last four of the user's credit card (retrieved from the getToken BSD 
  endpoint). Otherwise it should be the full credit card number.

* **`cc_type_cd`** (required)

  The type of card from the user. If using a payment token the value should be 
  what is specified in the getToken endpoint. Otherwise it should be what the 
  user selects.

* **`cc_expir_month`** (required)

  The expiration month of the user's credit card. If using a payment token the 
  value should be what is specified in the getToken endpoint. Otherwise it 
  should be what the user selects.

* **`cc_expir_year`** (required)

  The expiration year of the user's credit card. If using a payment token the 
  value should be what is specified in the getToken endpoint. Otherwise it 
  should be what the user selects.

* **`employer`** (conditional)

  The user's employer.

  If this is set to required in the BSD donation form, then it should be 
  required.

* **`occupation`** (conditional)

  The user's occupation.

  If this is set to required in the BSD donation form, then it should be 
  required.

* **`source`** (optional)

  This is typically used for tracking campaign success and can be set to any 
  arbitrary comma delimited list of values.

* **`subsource`** (optional)

  This is just a sub category to use similar to the source argument listed 
  above.

* **`no_reporting_url`** (optional)

  When set to true, omits the `action_code` and `td` URL parameters form the 
  `success_url` in the response. These parameters contains the same tracking 
  data included in the response, but they are encoded. They are used to report 
  contributions on donation thank you page, but are sometimes not necessary for 
  the Donate API.

* **`recurring_acknowledge`** (required for recurring contributions)

  To submit a recurring contribution you need to create a BSD donate page that 
  is set to type "recurring". Currently, you cannot have a recurring and
  non-recurring BSD donate page. If POSTing to a BSD donate form slug that is a 
  recurring page, this parameter must be set to "1".

* **`custom1`, `custom2`, `custom3`** (optional)

  These are all fields to hold custom data. They don't do anything except hold 
  data associated with the donation in the BSD database.

### Responses ###

The follow are possible responses from the Donate API:

* **successful response**

  JSON status code: 200
  
  The response will contain a JSON object with the API version number,
  reporting data for the contribution as well as a success URL. The success URL
  contains the page that the user should be redirected because of the successful
  donation.
  
  When the email address used for the donation is not already associated with a
  saved payment token and the BSD form's "enable Quick Donate enroll process"
  setting is enabled, the response will contain a cookie header that sets the
  required cookies for the success url (which in this case would be the quick 
  donate opt-in page) to function correctly.
  
  A cookie for duplicate detection (`contribution_resubmission`) will also be
  set on the responses for all successful contributions.

* **missing slug error response**

  JSON status code: 400
  
  This occurs when the slug is missing entirely. The response contains an API
  version number, status ("fail"), and a failure code ("noslug"). We do not try
  to contribute to the default contribution page in this instance as this is an
  obvious development error.

* **invalid slug error response**

  JSON status code: 400

  This occurs when the given slug does not exist. The response contains an API
  version number, status ("fail"), and a failure code ("invalidslug"). We
  currently do not try to contribute to the default contribution page, that may
  happen in a later version of the API.

* **validation failure response**

  JSON status code: 400

  This occurs when one of the user info. arguments in the request does not
  validate correctly. (e.g. the user's email is malformed, there was no phone
  number when that field is required, etc.) The response contains an API version
  number, status ("fail"), a failure code ("validation"), and an array of
  errors.

* **gateway error response**

  JSON status code: 400

  This occurs when the gateway declines the transaction. The response contains
  an API version number, status ("fail"), a failure code ("gateway"), and a
  `gateway_response` object that has more details passed back from the gateway
  about the failure. That object will contain the following elements:

  * **status** - The status of the transaction this can be one of the following 
    values: "error", "decline", "review", or "unknown"
  * **code** - The raw status code from the gateway for the failure
  * **message** - The corresponding error message for the given error code 
    according to the API docs of the gateway
  * **failed_avs** - Whether AVS (address verification) check failed
  * **failed_cvv** - Whether CVV (card security code) check failed

* **server error response**

  JSON status code: 500

  This occurs when the server is unable to process the request for any reason.
  The response contains an API version number, status ("fail"), a failure code
  ("unhandled").