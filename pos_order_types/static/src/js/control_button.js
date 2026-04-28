import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { InfoPopup } from "@pos_order_types/app/components/info_popup";
import { _t } from "@web/core/l10n/translation";
import { SelectionPopup } from "@point_of_sale/app/components/popups/selection_popup/selection_popup";
import { useService } from "@web/core/utils/hooks";



patch(ControlButtons.prototype,{
     setup() {
        super.setup(...arguments);
        console.log("jjjjjjjjjjjjjj")
        this.orm = useService("orm")
        console.log(this.orm)


    },

    async onClickOrderType() {

       console.log("onclickkkkkkkkkk")
       console.log(this)

//        var selectionList = await this.orm.searchRead(
//                    "pos.order.type",
//                    [["id", "=", this.pos.config.order_type_id]],
//                    ["id", "label"]
//                );

        console.log("lala", this.pos.models["pos.order.type"])
        const selectionList = this.pos.models["pos.order.type"].map((type) => ({
            id: type.id,
            label: type.name,
            isSelected: this.currentOrder.pos_order_type_id && type.id === this.currentOrder.pos_order_type_id.id,
            item: type,
        }));

         console.log("eeeeeeeeeeeeeeeee", selectionList)


       const type = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Select Order Type"),
            list: selectionList,
            size: "md"

        });
        console.log("before", this.currentOrder.pos_order_type_id)
        this.currentOrder.pos_order_type_id = type.id
        console.log("hehehe", this.currentOrder.pos_order_type_id)
        console.log("yess", this.currentOrder.pos_order_type_id)


       console.log("payloaddd", type)


    }
});


//
//const selectionList = this.models["pos.preset"].map((preset) => ({
//                id: preset.id,
//                label: preset.name,
//                isSelected: order.preset_id && preset.id === order.preset_id.id,
//                item: preset,
//            }));
//preset = await makeAwaitable(this.dialog, SelectionPopup, {
//                title: _t("Select preset"),
//                list: selectionList,
//                size: "md",
//            });

