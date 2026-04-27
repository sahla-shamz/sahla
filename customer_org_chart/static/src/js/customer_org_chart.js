import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { usePopover } from "@web/core/popover/popover_hook";
import { Component } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useRecordObserver } from "@web/model/relational_model/utils";

class ContactOrgChartPopover extends Component {
    static template = "customer_org_chart.contact_orgchart_emp_popover_";
    async setup() {
        super.setup();
        this.actionService = useService("action");
    }

    async _onEmployeeRedirect(employeeId) {
        this.actionService.doAction({
            name: "Redirect",
            type: "ir.actions.act_window",
            res_id: employeeId,
            res_model: "res.partner",
            views: [[false, "form"]],

        });
    }
}

export class ContactOrgChart extends Component {
    static template = "customer_org_chart.contact_org_chart";
    static props = {...standardFieldProps};
    async setup() {
        super.setup();

        this.actionService = useService("action");
        this.popover = usePopover(ContactOrgChartPopover);

        useRecordObserver(async (record) => {
            const newEmployeeId = record.resId || false;
            await this.fetchEmployeeData(newEmployeeId, true);

        });
    }

    async fetchEmployeeData(employeeId, force= false) {
            this.view_employee_id = employeeId;
            let orgData = await rpc(
                '/customer/get_org_chart',
                {
                    employee_id: employeeId,
                },
            );

            this.managers = orgData.manager;
            this.children = orgData.children;
            this.render(true);

    }

    _onOpenPopover(event, child) {
        this.popover.open(event.currentTarget, { child });
    }

    async _onEmployeeRedirect(employeeId) {
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
