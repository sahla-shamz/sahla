import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import { ListController } from '@web/views/list/list_controller';


export class CrmListController extends ListController
    {
        super(){
        console.log("helloo")
            super.setup()
            this.DemoFunction()
        }

       async DemoFunction()
       {
            console.log("demooo")
       }
    }


CrmListController.template = "salesperson_filter.CrmListTemplate"
registry.category('views').add('crm_lead_list', {
    ...listView,
    Controller: CrmListController,
});