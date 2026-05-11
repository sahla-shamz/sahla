import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import {Component, useState} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";


export class InfoPopup extends Component {
     static template = "pos_sale_order.InfoPopup";
     static components = { Dialog };

     setup(){
        this.pos= usePos();
        this.state = useState({ values : 'draft', desc : "" })
        this.orm = useService("orm");
        this.dialog = useService("dialog")
     }

     async discard() {
        this.props.close();
    }


    async createSaleOrder()
    {
        const session = this.pos.openOrder.session_id.id
        const description = this.state.desc
        const status = this.state.values
        const order_lines = this.pos.openOrder.lines
        if(this.pos.openOrder.pricelist_id)
        {
            var pricelist = this.pos.openOrder.pricelist_id.id
        }
        else{
            var pricelist = false
        }
        var arr_products = []
        for(const line of order_lines)
        {
            var taxes =[]
            for (const tax of line.tax_ids)
            {
                taxes.push(tax.id)
            }

            arr_products.push({'id' : line.product_id.id,
                            "qty" : line.quantityStr.unitPart,
                            'price' : line.price_unit,
                            'tax' : taxes,
                            'discount' : line.discount})
        }


        if (! this.pos.openOrder.partner_id)
        {
            this.props.close()
            this.dialog.add(AlertDialog, {
                title : _t("Customer Required"),
                body: _t("Please Select Customer"),
            });
        }
        else if(! order_lines.length)
        {
            this.props.close()
            this.dialog.add(AlertDialog, {
                title : _t("Empty Order"),
                body: _t("Please Add some Products."),
            });
        }
        else {
            var partner = this.pos.openOrder.partner_id.id
            const order_ref = await this.orm.call("sale.order", "create_sale_order",[status, arr_products, partner,
                description, session, pricelist], {});
            for (const line of this.pos.openOrder.lines)
            {
                this.pos.openOrder.removeOrderline(line)
            }
            this.props.close()
            this.dialog.add(AlertDialog, {
                title : _t("Sale Order Created"),
                body: _t(order_ref),
            });
        }

    }

}
