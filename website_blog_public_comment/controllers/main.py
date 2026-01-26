# See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_blog.controllers.main import WebsiteBlog


class WebsiteBlogInherit(WebsiteBlog):

    @http.route()
    def blog_post(self, blog, blog_post, tag_id=None, page=1, enable_editor=None, **post):
        response = super().blog_post(
            blog, blog_post, tag_id, page, enable_editor, **post
        )

        if request.env.user._is_public() and hasattr(response, 'qcontext'):
            # Get, or generate, the access_token
            token = blog_post._portal_ensure_token()

            # Get public partner from the default 'base.public_user' in Odoo.
            public_partner = request.env.ref('base.public_user').partner_id

            # Sign the token and link it to the public partner
            hash_value = blog_post._sign_token(public_partner.id)

            response.qcontext.update({
                'token': token,
                'hash': hash_value,
                'pid': public_partner.id,
            })

        return response