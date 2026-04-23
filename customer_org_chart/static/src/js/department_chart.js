import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
import { onWillStart, useState, onWillUpdateProps, Component } from "@odoo/owl";

export class ContactChart extends Component {
    static template = "customer_org_chart.ContactChart";
//    static props = {
//        ...standardWidgetProps,
//    };

    setup() {
        super.setup();
        console.log("hlo")
        this.action = useService("action");
        this.orm = useService("orm");
        this.state = useState({
            hierarchy: {},
        });

        onWillStart(async () => {
            await this.fetchHierarchy();
        });

//        onWillUpdateProps(async () => {
//            await this.fetchHierarchy();
//        });
    }

    async fetchHierarchy() {
    console.log("hhuhuh")
//        this.state.hierarchy = await this.orm.call("res.partner", "get_contact_hierarchy", [], {});
//        var demo = await this.orm.call("res.partner", "get_contact_hierarchy", [], {});
        var picking_type= await this.orm.call("res.partner", "get_contact_hierarchy")

        console.log(picking_type)
    }


export const contactChart = {
    component: ContactChart,
};
registry.category("fields").add("contact_chart", contactChart);
