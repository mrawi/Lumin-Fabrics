# See LICENSE file for full copyright and licensing details.

from odoo import models, tools, _
from odoo.exceptions import ValidationError
from odoo.http import request

from markupsafe import Markup

class BlogPost(models.Model):
    """
    Inherit Portal Mixin to enable access tokens for blog posts

    Method _portal_ensure_token() will set the access token if it doesn't exist using uuid.uuid4()

    Override message_post() to sanitize message contents and avoid potential XSS
    This also allows data management on the server side if needed to be stored later.
    """
    _name = 'blog.post'
    _inherit = ['blog.post', 'portal.mixin']

    def message_post(self, **kwargs):
        if request.env.user._is_public():
            public_params = request.params.get('post_data', {})
            p_name = public_params.get('public_author_name')
            p_email = public_params.get('public_author_email')
            p_website = public_params.get('public_author_website')

            if not p_name or not p_email:
                raise ValidationError(_("Name and Email are required."))

            kwargs['email_from'] = f"\"{p_name}\" <{p_email}>"  # Store email in mail.message for now.
            kwargs['subtype_xmlid'] = 'website_blog_public_comment.mt_blog_public_comment'

            clean_name = tools.html_escape(p_name)
            clean_url = tools.html_escape(p_website) if p_website else None
            if clean_url:
                signature = Markup("<br/><br/>---<br/>Comment by: <b>%s</b> (%s)") % (clean_name, clean_url)
            else:
                signature = Markup("<br/><br/>---<br/>Comment by: <b>%s</b>") % clean_name

            kwargs['body'] = (kwargs.get('body') or '') + signature
            kwargs['author_id'] = False  # Ensure the author is not linked

            # # Create the message with __system__ user
            # # Otherwise, any visitor will be able to edit all anonymous messages.
            # root_user = self.env.ref('base.user_root').sudo()
            # return super(BlogPost, self.with_user(root_user)).message_post(**kwargs)

        return super().message_post(**kwargs)
