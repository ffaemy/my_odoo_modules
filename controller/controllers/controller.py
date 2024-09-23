
from odoo import http
from odoo.http import request

class ProductCatalogController(http.Controller):
    @http.route('/product/catalog', auth='public', website=True)
    def product_catalog(self, search=None, category_id=None, sort_by='name'):
        domain = []
        
        # Apply search filter if provided
        if search:
            domain += [('name', 'ilike', search)]
        
        # Apply category filter if provided
        if category_id:
            domain += [('categ_id', '=', int(category_id))]

        # Fetch products based on search and filters
        products = request.env['product.template'].search(domain, order=f'{sort_by} asc')

        # Fetch product categories for filtering
        categories = request.env['product.category'].search([])

        return request.render('customization.product_catalog_template', {
            'products': products,
            'categories': categories,
            'search': search,
            'selected_category_id': int(category_id) if category_id else None,
            'sort_by': sort_by,
        })
