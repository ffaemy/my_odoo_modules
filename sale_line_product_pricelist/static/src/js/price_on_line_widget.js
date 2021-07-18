odoo.define('sale_line_product_pricelist.PriceOnLineWidget', function (require) {
"use strict";

var core = require('web.core');
var QWeb = core.qweb;

var Widget = require('web.Widget');
var widget_registry = require('web.widget_registry');
var config = require('web.config');

var _t = core._t;

var PriceOnLineWidget = Widget.extend({
    template: 'sale_line_product_pricelist.priceOnLine',
    events: _.extend({}, Widget.prototype.events, {
        'click .fa-info-circle': '_onClickButton',
    }),

    init: function (parent, params) {
        this.data = params.data;
        this._super(parent);
    },

    start: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            self._setPopOver();
        });
    },

    updateState: function (state) {
        this.$el.popover('dispose');
        var candidate = state.data[this.getParent().currentRow];
        if (candidate) {
            this.data = candidate.data;
            this.renderElement();
            this._setPopOver();
        }
    },
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------
    _setPopOver: function () {
        var self = this;
        if (!this.data.product_id){
        	return 
        }
        this.data.debug = config.debug;
        var $content = $(QWeb.render('sale_line_product_pricelist.PriceOnLinePopOver', {
            data: this.data,
        }));
        var options = {
            content: $content,
            html: true,
            placement: 'left',
            title: _t('Quantity on Hand'),
            trigger: 'focus',
            delay: {'show': 0, 'hide': 100 },
        };
        this.$el.popover(options);
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------
    _onClickButton: function () {
        this.$el.find('.fa-info-circle').prop('special_click', true);
    },
});

widget_registry.add('price_on_line_widget', PriceOnLineWidget);

return PriceOnLineWidget;
});
