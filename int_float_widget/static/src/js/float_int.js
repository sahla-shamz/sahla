/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import { Component } from "@odoo/owl";

export class FloatInt extends Component{
   static template = "int_float_widget.FloatIntField";

   setup(){
       this.input =  useInputField({
           getValue: () => this.props.record.data[this.props.name],
           refName: "inputfloatint",
           parse: (v) => Math.round(v)
           });
   }
}

export const floatInt = {
    component: FloatInt,
    displayName: "Float Int",
    supportedTypes: ["float"]
}

registry.category("fields").add("int_float_widget", floatInt);