import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import {Component, useState} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";



export class InfoPopup extends Component {
     static template = "pos_sale_order.InfoPopup";
     static components = { Dialog };
     setup(){
        this.pos= usePos();
        this.state = useState({ values : 'draft' })
         this.orm = useService("orm");
     }

     async discard() {
        this.props.close();
    }


    async createSaleOrder() {
         console.log("jijijiji", this.state.values)
        const items = await this.orm.call("sale.order", "create_sale_order",[this.state.values], {});
    }



}