# pos_receipt_custom_19/__manifest__.py
{
    "name": "POS Receipt Custom 19",
    "version": "1.0",
    "depends": ["point_of_sale"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_receipt_custom_19/static/src/js/pos_receipt_category.js",
            "pos_receipt_custom_19/static/src/css/pos_receipt.css",
            "pos_receipt_custom_19/static/src/js/pos_receipt_templates.xml",
        ],
    },
    "installable": True,
}
