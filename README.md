## Django-invitations - Generic invitations app

[![Build Status](https://travis-ci.org/bee-keeper/django-invitations.svg?branch=master)](https://travis-ci.org/bee-keeper/django-invitations)

[![Coverage Status](https://coveralls.io/repos/bee-keeper/django-invitations/badge.svg?branch=master&service=github)](https://coveralls.io/github/bee-keeper/django-invitations?branch=master)

## Warning

**I've made this fork from [bee-keeper/django-invitations](https://github.com/bee-keeper/django-invitations) to customize the package for my particular needs.**

**Therefore the code will not have in mind public distribution. DO NOT USE "AS IS"**

**I do not consider the changes made here fit the source repo, which is why I don't plan on making pull requests.**

### About

Generic invitations solution with adaptable backend and support for django-allauth. All emails and messages are fully customisable.

Originally written as an invitations solution for the excellent [django-allauth](https://github.com/pennersr/django-allauth), this app has been refactored to remove the allauth dependency whilst retaining 100% backwards compatibility.

Generic Invitation flow:

- Priviledged user invites prospective user by email (via either Django admin, form post, JSON post or programmatically)
- User receives invitation email with confirmation link
- User clicks link and is redirected to a preconfigured url (default is accounts/signup)

Allauth Invitation flow:

- As above but..
- User clicks link, their email is confirmed and they are redirected to signup
- The signup URL has the email prefilled and upon signing up the user is logged into the site

### Generic Installation

```
pip install django-invitations

# Add to settings.py, INSTALLED_APPS
'invitations',

# Append to urls.py
url(r'^invitations/', include('invitations.urls', namespace='invitations')),

# Run migrations

python manage.py migrate
```

### Allauth Integration

As above but note that invitations must come after allauth in the INSTALLED_APPS

```
# Add to settings.py
ACCOUNT_ADAPTER = 'invitations.models.InvitationsAdapter'
```

### Sending Invites

First import the model:

```
from invitations.utils import get_invitation_model
```

Make an instance of the model:

```
Invitation = get_invitation_model()
```

Then finally pass the recipient to the model and send.

```
# inviter argument is optional
invite = Invitation.create('email@example.com', inviter=request.user)
invite.send_invitation(request)
```

To send invites via django admin, just add an invite and save.

### Bulk Invites

Bulk invites are supported via JSON. Post a list of comma separated emails to the dedicated URL and Invitations will return a data object containing a list of valid and invalid invitations.

### Testing

`python manage.py test` or `tox`

### Additional Configuration

- `INVITATIONS_INVITATION_EXPIRY` (default=`3`)

  Integer. How many days before the invitation expires.

- `INVITATIONS_INVITATION_ONLY` (default=`False`)

  Boolean. If the site is invite only, or open to all (only relevant when using allauth).

- `INVITATIONS_CONFIRM_INVITE_ON_GET` (default=`True`)

  Boolean. If confirmations can be accepted via a `GET` request.

- `INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP` (default=`False`)

  Boolean. If `True`, invitations will be accepted after users finish signup.
  If `False`, invitations will be accepted right after the invitation link is clicked.
  Note that this only works with Allauth for now, which means `ACCOUNT_ADAPTER` has to be
  `'invitations.models.InvitationsAdapter'`. If Allauth is not present, you will have to
  implement the `accept invite` action in your own codebase.

- `INVITATIONS_GONE_ON_ACCEPT_ERROR` (default=`True`)

  Boolean. If `True`, return an HTTP 410 GONE response if the invitation key
  is invalid, or the invitation is expired or previously accepted when
  accepting an invite. If `False`, display an error message and redirect on
  errors:

  - Redirects to `INVITATIONS_SIGNUP_REDIRECT` on an expired key
  - Otherwise, redirects to `INVITATIONS_LOGIN_REDIRECT` on other errors.

- `INVITATIONS_ALLOW_JSON_INVITES` (default=`False`)

  Expose a URL for authenticated posting of invitees

- `INVITATIONS_SIGNUP_REDIRECT` (default=`'account_signup'`)

  URL name of your signup URL.

- `INVITATIONS_LOGIN_REDIRECT` (default=`LOGIN_URL` from Django settings)

  URL name of your login URL.

- `INVITATIONS_ADAPTER` (default=`'invitations.adapters.BaseInvitationsAdapter'`)

  Used for custom integrations. Set this to `ACCOUNT_ADAPTER` if using django-allauth.

  `INVITATIONS_KEY_LENGTH` (default=`64`)

  Integer. Use it to customize the length of the invitation key. It should be smaller or equal to 64.

- `INVITATIONS_EMAIL_MAX_LENGTH` (default=`254`)

  If set to `None` (the default), invitation email max length will be set up to 254. Set this to an integer value to set up a custome email max length value.

- `INVITATIONS_EMAIL_SUBJECT_PREFIX` (default=`None`)

  If set to `None` (the default), invitation email subjects will be prefixed with the name of the current Site in brackets (such as `[example.com]`). Set this to a string to for a custom email subject prefix, or an empty string for no prefix.

  `INVITATIONS_EMAIL_NON_UNIQUE_AND_NULL` (default=`False`)

  Boolean. Specifies whether the email the invite is sent to can be `Null` and non-unique. Changing this value on an existing project requires creating/applying migrations and, if changing from `True` to `False`, making sure the existing email addresses in the database are unique. It is usefull when you want to generate invite codes for offline use and you don't know the email address of the user. Not tested with `django-allauth`

- `INVITATIONS_INVITATION_MODEL` (default=`invitations.Invitation`)

  App registry path of the invitation model used in the current project, for customization purposes.

### Signals

The following signals are emitted:

- `invite_url_sent`
- `invite_accepted`

### Management Commands

Expired and accepted invites can be cleared as so:

`python manage.py clear_expired_invitations`
