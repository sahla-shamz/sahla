import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { _t } from "@web/core/l10n/translation";
import { SelectionPopup } from "@point_of_sale/app/components/popups/selection_popup/selection_popup";
import { useService } from "@web/core/utils/hooks";


patch(ControlButtons.prototype,{

    async onClickOrderType() {

        const selectionList = this.pos.config.order_type_id.map((type) => ({
            id: type.id,
            label: type.name,
            isSelected: this.currentOrder.pos_order_type_id && type.id === this.currentOrder.pos_order_type_id.id,
            item: type,
        }));

        selectionList.push(
        {   id : 0,
        label : "None",
        isSelected: !this.currentOrder.pos_order_type_id,
        item : null
        })


       const type = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Select Order Type"),
            list: selectionList,
            size: "md"

        });
        if(type)
            this.currentOrder.pos_order_type_id = type.id
        else
            this.currentOrder.pos_order_type_id = null

    }
});
