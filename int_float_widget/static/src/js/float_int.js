/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import { Component, useRef, onWillRender, onMounted, } from "@odoo/owl";
//import { parseFloat } from "@web/views/fields/parsers";


export class FloatInt extends Component{
   static template = "int_float_widget.FloatIntField";

   setup(){
       this.input = useRef('inputfloatint')
//       console.log("thisssss",this.props.record.data[this.props.name])
       var a= useInputField({
           getValue: () => this.props.record.data[this.props.name] || "" ,
           refName: "inputfloatint",
           });

//       console.log("aaaaaa",a)

       onWillRender(() =>  {
//        console.log("onwillrenderr")
           this.rounded()
       });
       onMounted(() =>  {
//       console.log("onmounteddd")
           this.rounded()
       });
   }
   rounded(){
       if (this.input.el)
           {
               this.props.record.data[this.props.name] = Math.round(this.input.el.value)
           }

//         console.log("new rounded",this.props.record.data[this.props.name])
   }
}
console.log("registryy", registry)

FloatInt.component = FloatInt
FloatInt.supportedTypes = ["float"]
registry.category("fields").add("int_float_widget", FloatInt);