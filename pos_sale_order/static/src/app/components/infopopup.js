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


    async createSaleOrder() {

        const session = this.pos.openOrder.session_id.id
        const description = this.state.desc
        const status = this.state.values
        const order_lines = this.pos.openOrder.lines
        console.log("order liness", order_lines)
        console.log("pos", this.pos)
        var arr_products = []
        for(const i of order_lines)
        {
            // console.log("iiiiiiiiii", i.tax_ids)

            var taxes =[]
            for (const j of i.tax_ids)
            {
                taxes.push(j.id)
                // console.log("kkkkkkkkkkk",j)
            }

            console.log("taxes", taxes)

            arr_products.push({'id' : i.product_id.id,
                            "qty" : i.quantityStr.unitPart,
                            'price' : i.displayPriceUnitExcl,
                            'tax' : taxes})

        }
        console.log("arrrrr", arr_products)

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
            const order_ref = await this.orm.call("sale.order", "create_sale_order",[status, arr_products, partner, description, session], {});

            this.props.close()
            this.dialog.add(AlertDialog, {
                title : _t("Sale Order Created"),
                body: _t(order_ref),
            });
        }


    }

}