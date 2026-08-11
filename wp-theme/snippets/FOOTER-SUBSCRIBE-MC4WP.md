# Footer Subscribe — Mailchimp for WordPress (MC4WP)

## What was broken

The footer **Stay connected / Subscribe** block was a fake form:

```html
<form action="mailto:support@fix4u.co.nz" method="get">
  <input type="email" name="subject" ...>
  <button type="submit">Subscribe</button>
</form>
```

Browsers treat form navigation to `mailto:` as unsafe and block it (Chrome: “unsafe” / navigation aborted). It was **not** a working newsletter signup.

## App in use

| Plugin | Role |
|--------|------|
| **Mailchimp for WordPress (MC4WP) v4.14.0** | Real newsletter form |
| Form ID **1189** | “Join our newsletter for the latest offers and product news” |
| Shortcode | `[mc4wp_form id="1189"]` |

Also installed (not used for this footer): Contact Form 7 (contact page form 54), WPForms Lite. Jetpack Mailchimp is **not connected**.

## Fix applied (2026-08)

Across all blank-template pages/posts that shared the footer shell (48 items):

1. Removed the `mailto:` form.
2. Inserted a Shortcode block so WordPress can render MC4WP (shortcodes do not run inside Custom HTML blocks):

```html
<!-- /wp:html -->
<!-- wp:shortcode -->
[mc4wp_form id="1189"]
<!-- /wp:shortcode -->
<!-- wp:html -->
```

3. Added CSS marker `FIX4U_FOOTER_MC4WP` so the MC4WP fields match the dark footer newsletter panel.

## Verify

1. Open any page footer → **Stay connected**.
2. Confirm the form posts to the current page (`method="post"`, `data-id="1189"`), not `mailto:`.
3. Submit a test email → MC4WP success/error message in `.mc4wp-response` (depends on Mailchimp list connection in WP Admin → Mailchimp for WP).

## Admin

- WP Admin → **Mailchimp for WP → Forms** → form 1189 to edit fields/messages.
- Ensure Mailchimp API key / audience list is still connected if submissions fail after the UI works.
