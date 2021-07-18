# -*- coding: utf-8 -*-

import datetime

from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from lxml import etree

import logging
_logger = logging.getLogger(__name__)

class GoogleFeed(http.Controller):

    @http.route('/googlefeed.xml', type='http', auth="none")
    def googlefeed(self):
        domain = '%s://%s' % (request.httprequest.environ.get('wsgi.url_scheme', 'https'), request.httprequest.environ.get('HTTP_HOST', ''))
        website = request.env['website'].get_current_website()
        atom_namespace = 'http://www.w3.org/2005/Atom'
        atom = '{%s}' % atom_namespace
        google_namespace = 'http://base.google.com/ns/1.0'
        google = '{%s}' % google_namespace
        nsmap = {
            None: atom_namespace,
            'g': google_namespace
        }
        feed = etree.Element('feed', nsmap=nsmap)
        etree.SubElement(feed, 'title').text = 'Spiral Direct Product Feed'
        etree.SubElement(feed, 'link', attrib={
            'href': domain,
            'rel': 'self'
        })
        etree.SubElement(feed, 'updated').text = datetime.datetime.now().replace(microsecond=0).isoformat()
        author = etree.SubElement(feed, 'author')
        etree.SubElement(author, 'name').text = 'Spiral Direct'
        mailorder_website_id = request.env['website'].search([('domain','ilike','spiraldirect.com')], limit=1)
        #Add products

        query = 'SELECT id, default_code from product_product AS pp WHERE pp.product_tmpl_id in (SELECT id FROM product_template AS pt WHERE pt.sd_sales_count > 0 ORDER BY pt.sd_sales_count desc LIMIT 100)'
        request.env.cr.execute(query)
        data = request.env.cr.fetchall()
        top_seller_products_ids = [elem[0] for elem in data]

        # Pricelist
        gbp_currency_id = request.env['res.currency'].sudo().search([('name','=','GBP')], limit=1)
        mailorder_pricelist_id = request.env['product.pricelist'].sudo().search([('name','ilike','Mailorder'),('currency_id','=',gbp_currency_id.id)], limit=1)

        mailorder_pricelist_item_ids = mailorder_pricelist_id.item_ids

        for product in request.env['product.product'].sudo().search([
                ('website_published','=',True),
                ('website_id','in',[mailorder_website_id.id if mailorder_website_id else False, False]),
                ('default_code','!=',False),
                ('active','=',True)]):
            #Get age group
            age_group = product.attribute_value_ids.filtered(lambda value: value.attribute_id.id == website.company_id.google_age_group.id).name
            if age_group == 'Adults':
                age_group = 'adult'
            elif age_group == 'Kids':
                age_group = 'kids'
            elif age_group == 'Babies':
                age_group = 'infant'
            else:
                default_code = product.default_code
                if default_code and len(default_code) >= 8:
                    if default_code[4:6] == 'K0':
                        age_group = 'toddler'
                    elif default_code[4] == 'K':
                        age_group = 'kids'
                    else:
                        age_group = 'adult'
            #Get colour
            color = product.attribute_value_ids.filtered(lambda value: value.attribute_id.id == website.company_id.google_color.id)
            if color and len(color) > 1:
                color = '/'.join(color.mapped('name'))
            else:
                color = color.name
            #Get gender
            gender = product.attribute_value_ids.filtered(lambda value: value.attribute_id.id == website.company_id.google_gender.id).name
            #Get material
            material = product.attribute_value_ids.filtered(lambda value: value.attribute_id.id == website.company_id.google_material.id).name
            #Get size
            size = product.attribute_value_ids.filtered(lambda value: value.attribute_id.id == website.company_id.google_size.id).name
            size_system = False
            try:
                if not size:
                    size_ids = product.attribute_value_ids.filtered(lambda value: value.attribute_id.name in ['Mens Sneakers (EU-US-UK)', 'Ladies Sneakers (EU-US-UK)'])
                    if size_ids and len(size_ids) == 1:
                        size = size_ids.name[1:3]
                        size_system = True
                        #size = size_ids.name
            except Exception as e:
                _logger.info('--Error Getting Size Attribute==> {}'.format(e))

            if product.description_sale:
                description_sale = product.description_sale
            elif product.website_description:
                if '<p>' in product.website_description:
                    description_sale = product.website_description.replace('<p>','').replace('</p>','')
                else:
                    description_sale = product.website_description
            else:
                description_sale = ''

            link = '%s/%s' % (domain, product.url_key)
            if mailorder_website_id and mailorder_website_id.use_suffix:
                link = link = '%s/%s%s' % (domain, product.url_key, '.htm' if mailorder_website_id.suffix_product else mailorder_website_id.suffix_product)

            entry = etree.SubElement(feed, 'entry')
            etree.SubElement(entry, google + 'id').text = product.default_code if product.default_code else str(product.id)
            etree.SubElement(entry, google + 'title').text = product.name
            etree.SubElement(entry, google + 'description').text = description_sale
            etree.SubElement(entry, google + 'link').text = link
            etree.SubElement(entry, google + 'image_link').text = '%s/web/image/product.product/%s/image_zoom' % (domain, product.id)
            etree.SubElement(entry, google + 'availability').text = 'in stock' if (product.qty_available_not_res > 0 or product.type == 'service') else 'out of stock'
            #etree.SubElement(entry, google + 'price').text = '%.2f %s' % (round(product.lst_price, 2), product.currency_id.name)

            p_item_id = mailorder_pricelist_item_ids.filtered(lambda item: item.product_id.id == product.id)
            p_tmpl_item_id = mailorder_pricelist_item_ids.filtered(lambda item: item.product_tmpl_id.id == product.product_tmpl_id.id)
            if p_item_id and p_item_id[0].fixed_price !=0:
                price = round(p_item_id[0].fixed_price, 2)
            elif p_tmpl_item_id and p_tmpl_item_id[0].fixed_price !=0:
                price = round(p_tmpl_item_id[0].fixed_price, 2)
            else:
                price = round(product.lst_price, 2)

            if price < round(product.lst_price, 2):
                etree.SubElement(entry, google + 'price').text = '%.2f %s' % (round(product.lst_price, 2), product.currency_id.name)
                etree.SubElement(entry, google + 'sale_price').text = '%.2f %s' % (price, mailorder_pricelist_id.currency_id.name)
            else:
                etree.SubElement(entry, google + 'price').text = '%.2f %s' % (round(price, 2), mailorder_pricelist_id.currency_id.name)

            etree.SubElement(entry, google + 'google_product_category').text = product.google_category or ''
            etree.SubElement(entry, google + 'brand').text = product.company_id.name or website.company_id.name
            etree.SubElement(entry, google + 'mpn').text = product.default_code or ''
            etree.SubElement(entry, google + 'condition').text = 'new'
            etree.SubElement(entry, google + 'age_group').text = age_group or ''
            etree.SubElement(entry, google + 'color').text = color or ''
            etree.SubElement(entry, google + 'gender').text = gender and gender.lower() or ''
            etree.SubElement(entry, google + 'material').text = material or ''
            etree.SubElement(entry, google + 'size').text = str(size) or ''
            if size_system:
                etree.SubElement(entry, google + 'size_system').text = 'EU'
            etree.SubElement(entry, google + 'custom_label_0').text = product.collection_id.name or ''
            etree.SubElement(entry, google + 'custom_label_1').text = product.categ_id.name or ''
            etree.SubElement(entry, google + 'custom_label_2').text = 'On sale' if product.sd_product_sale_state == 'sale' else ''
            etree.SubElement(entry, google + 'custom_label_3').text = 'Top Seller' if product.id in top_seller_products_ids else ''
            etree.SubElement(entry, google + 'custom_label_4').text = 'NEW' if product.sd_product_sale_state == 'new' else ''
            etree.SubElement(entry, google + 'item_group_id').text = product.product_tmpl_id.default_code or ''
        content = etree.tostring(feed, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        return request.make_response(content, [('Content-Type', 'text/xml')])


    @http.route('/doofinderfeed.xml', type='http', auth="none")
    def doofinderfeed(self):
        domain = '%s://%s' % (request.httprequest.environ.get('wsgi.url_scheme', 'https'), request.httprequest.environ.get('HTTP_HOST', ''))
        website = request.env['website'].get_current_website()
        atom_namespace = 'http://www.w3.org/2005/Atom'
        atom = '{%s}' % atom_namespace
        google_namespace = 'http://base.google.com/ns/1.0'
        google = '{%s}' % google_namespace
        nsmap = {
            None: atom_namespace,
            'g': google_namespace
        }
        feed = etree.Element('feed', nsmap=nsmap)
        etree.SubElement(feed, 'title').text = 'Spiral Direct Product Feed'
        etree.SubElement(feed, 'link', attrib={
            'href': domain, 
            'rel': 'self'
        })
        etree.SubElement(feed, 'updated').text = datetime.datetime.now().replace(microsecond=0).isoformat()
        author = etree.SubElement(feed, 'author')
        etree.SubElement(author, 'name').text = 'Spiral Direct'
        #Add products
        for product in request.env['product.product'].sudo().search([('website_published','=',True)]):
            #Get age group
            age_group = product.attribute_value_ids.filtered(lambda value: value.attribute_id.id == website.company_id.google_age_group.id).name
            if age_group == 'Adults':
                age_group = 'adult'
            elif age_group == 'Kids':
                age_group = 'kids'
            elif age_group == 'Babies':
                age_group = 'infant'
            #Get colour
            color = product.attribute_value_ids.filtered(lambda value: value.attribute_id.id == website.company_id.google_color.id).name
            #Get gender
            gender = product.attribute_value_ids.filtered(lambda value: value.attribute_id.id == website.company_id.google_gender.id).name
            #Get material
            material = product.attribute_value_ids.filtered(lambda value: value.attribute_id.id == website.company_id.google_material.id).name
            #Get size
            size = product.attribute_value_ids.filtered(lambda value: value.attribute_id.id == website.company_id.google_size.id).name

            entry = etree.SubElement(feed, 'entry')
            etree.SubElement(entry, google + 'id').text = product.default_code if product.default_code else str(product.id)
            etree.SubElement(entry, google + 'title').text = product.name
            etree.SubElement(entry, google + 'description').text = product.description_sale or ''
            etree.SubElement(entry, google + 'link').text = '%s/shop/product/%s' % (domain, slug(product.product_tmpl_id))
            etree.SubElement(entry, google + 'image_link').text = '%s/web/image/product.product/%s/image_zoom' % (domain, product.id)
            etree.SubElement(entry, google + 'availability').text = 'in stock' if (product.qty_available_not_res > 0 or product.type == 'service') else 'out of stock'
            etree.SubElement(entry, google + 'price').text = '%.2f %s' % (round(product.lst_price, 2), product.currency_id.name)

            item_id = product.item_ids.filtered(lambda item: item.pricelist_id.id == 7) # Mail order price
            if item_id and len(item_id) == 1 and item_id.fixed_price !=0 and round(product.lst_price, 2) > round(item_id.fixed_price, 2):
                etree.SubElement(entry, google + 'sale_price').text = '%.2f %s' % (round(item_id.fixed_price, 2), item_id.currency_id.name)

            etree.SubElement(entry, google + 'google_product_category').text = product.google_category or ''
            etree.SubElement(entry, google + 'brand').text = product.company_id.name or website.company_id.name
            etree.SubElement(entry, google + 'mpn').text = product.default_code or ''
            etree.SubElement(entry, google + 'condition').text = 'new'
            etree.SubElement(entry, google + 'age_group').text = age_group or ''
            etree.SubElement(entry, google + 'color').text = color or ''
            etree.SubElement(entry, google + 'gender').text = gender and gender.lower() or ''
            etree.SubElement(entry, google + 'material').text = material or ''
            etree.SubElement(entry, google + 'size').text = size or ''
            etree.SubElement(entry, google + 'item_group_id').text = product.product_tmpl_id.default_code or ''
            etree.SubElement(entry, google + 'score').text = str(product.sd_sales_count)
        content = etree.tostring(feed, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        return request.make_response(content, [('Content-Type', 'text/xml')])
