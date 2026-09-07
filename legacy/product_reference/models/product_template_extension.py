# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        # Define prefix mapping for each category
        prefix_mapping = {
            'Remote': 'Rem',
            'Incountry': 'Inc',
            'Overseas': 'Over',
        }

        for vals in vals_list:
            if not vals.get('default_code'):
                categ_id = vals.get('categ_id')
                if not categ_id:
                    raise ValidationError(_("You must select a product category to generate the internal reference."))

                # Retrieve and normalize the category name
                category = self.env['product.category'].browse(categ_id)
                category_name_clean = category.name.strip().title()

                # Match with prefix mapping
                prefix = prefix_mapping.get(category_name_clean)
                if not prefix:
                    raise ValidationError(_(
                        "The selected category (%s) is not configured for internal reference generation."
                    ) % category.name)

                # Build the sequence code using the cleaned name
                seq_code = 'product.internal.ref.' + category_name_clean.lower().replace(" ", "_")
                new_code = self.env['ir.sequence'].next_by_code(seq_code)

                if new_code:
                    vals['default_code'] = new_code
                else:
                    # Fallback: search last product with the same prefix and increment
                    last_product = self.search([('default_code', 'like', prefix + '%')], order='id desc', limit=1)
                    if last_product and last_product.default_code:
                        new_number = int(last_product.default_code) + 1
                    else:
                        new_number = int(prefix + '0001')
                    vals['default_code'] = str(new_number).zfill(5)

        return super(ProductTemplate, self).create(vals_list)
