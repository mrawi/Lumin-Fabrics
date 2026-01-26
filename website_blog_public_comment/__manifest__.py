# See LICENSE file for full copyright and licensing details.
{
    'name': 'Blog Public Comments',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'summary': 'Blog Public Comments',
    'description': """
                   
    """,
    'category': 'Website/Website',
    'author': 'Mustafa Rawi',
    'website': 'https://www.mrawi.com',
    'price': 0,
    'currency': 'EUR',
    'images': [],
    'depends': ['portal', 'website_blog'],
    'data': [
        # Security
        'security/ir_rules.xml',
        # Data Files

        # Views
        'views/website_blog_templates.xml',
        # Menus

    ],
    'demo': [
    ],
    'qweb': [
    ],
    'assets': {
        'web.assets_frontend': [
            'website_blog_public_comment/static/src/js/portal_chatter.js'
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
