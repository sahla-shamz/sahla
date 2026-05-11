import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { InfoPopup } from "@pos_sale_order/app/components/infopopup";


patch(ControlButtons.prototype, {
    setup() {
        super.setup();
    },
    async onClickCreateSaleOrder(){
        await makeAwaitable(this.dialog, InfoPopup);
    }
});
