/** @odoo-module **/
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import { ListRenderer } from "@web/views/list/list_renderer";
import { onWillStart, useState } from '@odoo/owl';
import { useService } from "@web/core/utils/hooks";

export class CrmListRenderer extends ListRenderer {
    static template = "salesperson_filter.CrmListTemplate";

    setup() {
        super.setup();
        this.orm = useService("orm")
        this.state = useState({ salesperson: [], name : "" });

        onWillStart(async ()=>{
            await this.get_users()
        })

    }


    async get_users(){
        this.state.salesperson = await this.orm.searchRead("res.users", [["share", "=", false]] , ["id", "name"])
    }


    onChange(){
        this.env.searchModel.clearQuery()
        for(var i =0; i<this.state.salesperson.length; i++)
        {   if (this.state.salesperson[i].id == this.state.salesperson.id)
                this.state.name =  this.state.salesperson[i].name
        }

        var preFilter = {
            description : `Salesperson contains ${this.state.name}`,
            domain: [['user_id', '=', Number(this.state.salesperson.id)]],
            type: "filter",
        }

        this.env.searchModel.createNewFilters([preFilter])

        if (this.state.salesperson.id == 'select'){
            this.env.searchModel.clearQuery()
        }

    }

};

export const crmListView = {
    ...listView,
    Renderer: CrmListRenderer
};

registry.category("views").add("crm_lead_list", crmListView);





