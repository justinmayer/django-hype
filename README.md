# Hype

A Django module that implements referral link logic.


## Concepts


This library implements two models:

- The `ReferralLink`. This object represents a user's referral link, or invitation link.
  It has a string identifier which allows the user to share their link as `/ref/<refid>/`.
- The `ReferralHit`. This is an instance of a user (logged in or anonymous) actually following
  a referral link.

## The Anonymous Cookie

When a ReferralLink is followed, a `ReferralHit` object is created. If the link was followed
by a logged in user, that user will be available on the ReferralHit object as a foreign key.
If the link was followed by an anonymous user, a cookie will be set on the user for future
reference.

The cookie contains a random UUID which is set on the ReferralHit. At any time, you may get
that cookie and, should the user log in, update all ReferralHit objects with that matching
UUID.
The library includes a middleware which will automatically do this for every logged in users,
see `hype.middleware.AnonymousReferralMiddleware`.


## Confirming Referrals

You may wish to implement a `SuccessfulReferral` model which is created when a user who
previously followed a `ReferralLink` (and thus created a `ReferralHit`) actually completes
whichever steps the referral system requires referred users to complete (for example:
Register to the website, make their first purchase, post their first comment, ...).

The `ReferralHit` model also has a `confirmed` DateTimeField which you may use for this purpose.


## Supporting Referral Links on Any URL

Implementers may find it useful to allow a referral on any URL. This is implemented in the
`hype.middleware.ReferralLinkMiddleware` middleware, which looks at all GET requests
and, should a valid referral link be present in the GET parameters, redirects to that referral
link's URL with the `next` parameter set to the original URL, without the referral link present.

Example:
 - `/accounts/signup/?ref=abc123def` redirects to...
 - `/ref/abs123def?next=/accounts/signup/` which redirects to...
 - `/accounts/signup/`, after creating a ReferralHit.


## Setup and configuration

1. Install via `python -m pip install django-hype`
2. Add `hype` to your `INSTALLED_APPS`
3. Include `hype.urls` in your URLs. Example: `url(r"^ref/", include("hype.urls"))`
4. Add `hype.middleware.AnonymousReferralMiddleware` to your `MIDDLEWARE`.
   This is required to update referrals for anonymous users when they log in.
5. (optional) Add `hype.middleware.ReferralLinkMiddleware` to your `MIDDLEWARE`.
   This is required if you want `?ref=...` to redirect properly.

These steps are enough to start gathering referral information.
You create a referral link, and watch the `ReferralHit` table fill up as users follow it.

In addition to having that data, you may want to "confirm" referrals. The `ConfirmedReferral`
model is there as a convenience model to allow you to filter down the referral hits in question.
Upon creating a ConfirmedReferral you may also want to do something else, such as crediting a
user some points.
The atomicity and idempotency of such events is left as an exercise for the reader.


## License

This project is licensed under the MIT license. The full license text is
available in the LICENSE file.
