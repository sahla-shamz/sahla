/** @odoo-module **/
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
//import { ListController } from '@web/views/list/list_controller';
//import { ControlPanel } from "@web/search/control_panel/control_panel";
import { ListRenderer } from "@web/views/list/list_renderer";
import { onWillStart, useState, onMounted, onWillRender } from '@odoo/owl';
import { user } from "@web/core/user";
import { useService } from "@web/core/utils/hooks";




export class CrmListRenderer extends ListRenderer {
    static template = "salesperson_filter.CrmListTemplate";

    setup() {
        super.setup();
        this.orm = useService("orm")
        this.action = useService("action");
        this.state = useState({ salesperson: [] });

        onWillStart(async ()=>{
            await this.get_users()
        })



    }


    async get_users(){
        console.log(user)
        console.log("data", this.props)
        this.state.salesperson = await this.orm.searchRead("res.users", [] , ["id", "name"])
        console.log(this.state.salesperson)
        console.log("contextttt",this)
//        this.action.doAction({
//                            type: "ir.actions.act_window",
//                            res_model: "crm.lead",
//                            views: [
//                                [false, "list"],
//                                [false, "form"],
//                            ],
//                            domain : [['user_id' , '=' , this.state.salesperson.id]]
//                        })


    }


    onChange(){
        console.log("hbbbbbbbbbd")
        console.log(this.state.salesperson.id)
        console.log(this.action.currentAction.then())
//         this.action.doAction({
//                type: "ir.actions.act_window",
//                res_model: "crm.lead",
//                views: [
//                    [false, "list"],
//                    [false, "form"],
//                ],
//                domain : [['user_id' , 'in' , [Number(this.state.salesperson.id)]]]
//            })
    }



//    static components = {
//        ...ListRenderer.components,
//
//    };
};

export const crmListView = {
    ...listView,
    Renderer: CrmListRenderer
};

registry.category("views").add("crm_lead_list", crmListView);





