# Django Reflinks

A Django module that implements referral link logic.


## Concepts


This library implements three models:

- The `ReferralLink`. This object represents a user's referral link, or invitation link.
  It has a string identifier which allows the user to share their link as `/ref/<refid>/`.
- The `ReferralHit`. This is an instance of a user (logged in or anonymous) actually following
  a referral link.
- The `ConfirmedReferral`. This is created when a user who previously followed a `ReferralLink`
  (and thus created a `ReferralHit`) actually completes whichever steps the referral system
  requires referred users to complete (for example: Register to the website, make their first
  purchase, post their first comment, ...).


## The Anonymous Cookie

When a ReferralLink is followed, a `ReferralHit` object is created. If the link was followed
by a logged in user, that user will be available on the ReferralHit object as a foreign key.
If the link was followed by an anonymous user, a cookie will be set on the user for future
reference.

The cookie contains a random UUID which is set on the ReferralHit. At any time, you may get
that cookie and, should the user log in, update all ReferralHit objects with that matching
UUID.
The library includes a middleware which will automatically do this for every logged in users,
see `django_reflinks.middleware.AnonymousReferralMiddleware`.


## Confirming referrals

ConfirmedReferral is created at the implementer's discretion.


## Supporting referral links on any URL.

Implementers may find it useful to allow a referral on any URL. This is implemented in the
`django_reflinks.middleware.ReferralLinkMiddleware` middleware, which looks at all GET requests
and, should a valid referral link be present in the GET parameters, redirects to that referral
link's URL with the `next` parameter set to the original URL, without the referral link present.

Example:
 - `/accounts/signup/?ref=abc123def` redirects to...
 - `/ref/abs123def?next=/accounts/signup/` which redirects to...
 - `/accounts/signup/`, after creating a ReferralHit.
