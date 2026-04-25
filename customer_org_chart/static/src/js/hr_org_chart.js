import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { usePopover } from "@web/core/popover/popover_hook";
import { user } from "@web/core/user";
//import { onEmployeeSubRedirect } from './hooks';
import { Component, useState } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useRecordObserver } from "@web/model/relational_model/utils";

class ContactOrgChartPopover extends Component {
    static template = "customer_org_chart.contact_orgchart_emp_popover";
//    static props = {
//        employee: Object,
//        close: Function,
//    };
    async setup() {
        super.setup();
        console.log("hayyyyy")

        this.orm = useService('orm');
        this.actionService = useService("action");
//        this._onEmployeeSubRedirect = onEmployeeSubRedirect();
    }


//    async _onEmployeeRedirect(employeeId) {
//        const action = await this.orm.call('hr.employee', 'get_formview_action', [employeeId]);
//        this.actionService.doAction(action);
//    }
}

export class ContactOrgChart extends Component {
    static template = "customer_org_chart.contact_org_chart";
    static props = {...standardFieldProps};
    async setup() {
        super.setup();

        this.orm = useService('orm');
        this.actionService = useService("action");
//        this.popover = usePopover(ContactOrgChartPopover);

//        this.state = useState({'employee_id': null});
        this.max_level = null;
//        this.lastEmployeeId = null;
//        this._onEmployeeSubRedirect = onEmployeeSubRedirect();

        useRecordObserver(async (record) => {
            const newParentId = record.data.parent_partner_id?.id || false;
            const newEmployeeId = record.resId || false;
            await this.fetchEmployeeData(newEmployeeId);

//            this.state.employee_id = newEmployeeId;
        });
    }

    async fetchEmployeeData(employeeId) {
            this.view_employee_id = employeeId;
            let orgData = await rpc(
                '/customer/get_org_chart',
                {
                    employee_id: employeeId,

                },
            );

            console.log("ORG DATA", orgData)

            this.managers = orgData.manager;
            this.children = orgData.children;
            this.render(true);
            console.log("managers", this.managers)
            console.log("children", this.children)

    }

//    _onOpenPopover(event, employee) {
//        this.popover.open(event.currentTarget, { employee });
//    }


    async _onEmployeeRedirect(employeeId) {
//        const action = await this.orm.call('hr.employee', 'get_formview_action', [employeeId]);
        this.actionService.doAction({
            name: "Redirect",
            type: "ir.actions.act_window",
            res_id: employeeId,
            res_model: "res.partner",
            views: [[false, "form"]],

        });
    }


}

export const contactOrgChart = {
    component: ContactOrgChart,
};

registry.category("fields").add("custom_org_chart", contactOrgChart);
