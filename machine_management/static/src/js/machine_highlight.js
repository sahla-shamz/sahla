/** @odoo-module **/
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { useDateTimePicker } from "@web/core/datetime/datetime_picker_hook";

export function chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
publicWidget.registry.get_machine = publicWidget.Widget.extend({
    selector : '#machine_carousel',
    async willStart() {
        const data = await rpc('/get_machines', {});
        const[machine_name, machine_image, machine_id] = data
        Object.assign(this, {
            machine_name, machine_image, machine_id
        })

    },
    start(){
     const refEl = this.$target.find("#carousel_machine")
     const { machine_name, machine_image, machine_id} = this
     const chunkData= chunk(machine_name, 4)
     chunkData[0].is_active = true
     const now = new Date();
     var milli = now.getMilliseconds()

     refEl.html(renderToFragment('machine_management.machine_data', {chunkData: chunkData,
     milli: milli}))
    }

});

