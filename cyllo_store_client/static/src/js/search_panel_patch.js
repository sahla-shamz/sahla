/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { SearchPanel } from "@web/search/search_panel/search_panel";

patch(SearchPanel.prototype, {
    setup() {
        super.setup(...arguments);
        this.cylloAction = useService("action");
        this.cylloOrm = useService("orm");
    },

    async toggleCategory(category, value) {
        const model = this.env.searchModel.resModel;
        // Apps page -> "Cyllo App Store" entry: open the store as the Apps page
        if (model === "ir.module.module" && value.id === "cyllo_store") {
            return this.cylloAction.doAction(
                "cyllo_store_client.action_open_cyllo_store",
                { clearBreadcrumbs: true }
            );
        }
        // Store page -> All / Official Apps / Industries: back to Apps page
        if (
            model === "cyllo.store.app" &&
            category.fieldName === "panel_type" &&
            value.id !== "cyllo_store"
        ) {
            const action = await this.cylloOrm.call(
                "cyllo.store.app", "action_open_apps", [value.id || false]
            );
            return this.cylloAction.doAction(action, { clearBreadcrumbs: true });
        }
        return super.toggleCategory(...arguments);
    },
});
