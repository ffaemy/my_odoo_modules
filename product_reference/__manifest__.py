{
    'name': "Custom Product Internal Reference",
    'summary': "Auto-generate default_code based on product category.",
    'description': """
        When a new product is created, if its category (categ_id) is one of the top-level ones,
        the internal reference (default_code) is auto-generated. For example, if the category is 
        'Ingredients', the code will start with 1 (e.g. 10001, 10002, etc.).
    """,
    'author': 'M Farooq Rajput(farooq.rajput@gravitai.com)',
    'depends': ['product'],
    'data': [
         'data/product_internal_seq.xml',
    ],
    'installable': True,
    'application': False,
}
