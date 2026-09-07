odoo.define('sale_line_product_pricelist.PopoverStockProduct', function (require) {
"use strict";

var core = require('web.core');

var PopoverWidgetField = require('stock.popover_widget');
var registry = require('web.field_registry');
var _t = core._t;

var PopoverStockProduct = PopoverWidgetField.extend({
    title: _t('Product Stock'),
    trigger: 'focus',
    color: 'text-info',
    icon: 'fa-exclamation-circle',
    _render: function () {
        this._super();
    },

});

registry.add('stock_product_popover', PopoverStockProduct);

return PopoverStockProduct;
});
