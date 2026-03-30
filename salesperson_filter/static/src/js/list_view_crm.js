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


    }


    onChange(){
        console.log("hbbbbbbbbbd")
        console.log(this.state.salesperson.id)
//        this.env.searchModel.searchDomain = [['user_id' , '=', this.state.salesperson.id]]
//        this.env.searchModel._domain = [['user_id' , '=', Number(this.state.salesperson.id)]]
//        this.env.searchModel._context.default_type = oppor
        this.env.searchModel.searchItems[12].domain = [['user_id', '=', Number(this.state.salesperson.id)]]
//        this.env.searchModel._context.globalContext[search_default_assigned_to_me] = 1
        console.log("search", this.env.searchModel)
//        console.log("search", this.env.searchModel.clearQuery())
        this.env.searchModel.clearQuery()
        this.env.searchModel.toggleSearchItem(12)
        console.log("envvvv", this.env)
        const preFilter = {
                description : "New",
                tooltip : "Neww",
                domain: [['user_id', '=', Number(this.state.salesperson.id)]],
//                invisible: "True",
                type: "filter",
            };
        console.log(this.env.searchModel.createNewFilters(preFilter))

        console.log("fdddddddddddddd", this.env.searchModel)
//        console.log(this.action.currentAction.then())
//         this.action.doAction({
//                type: "ir.actions.act_window",
//                res_model: "crm.lead",
//                views: [
//                    [false, "list"],
//                    [false, "form"],
//                ],
//                context : [['user_id' , 'in' , [Number(this.state.salesperson.id)]]]
//            })
    }




};

export const crmListView = {
    ...listView,
    Renderer: CrmListRenderer
};

registry.category("views").add("crm_lead_list", crmListView);





