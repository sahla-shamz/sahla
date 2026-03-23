/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";



export class WeatherInfo extends Component {
    setup(){
    console.log("this", this)

    this.state = useState( {value : [], date : ""})


     onWillStart(async () => {
            await this.weather_info();
        });
    }

    async weather_info()
    {
        console.log("weather")

            var lat = "11.2488"
            var lon = "75.7839"
            var apiKey = "9179ea68b5b998972a330d3ecb51e3d6"
            const weather_info = fetch(`https://api.openweathermap.org/data/2.5/weather?lat=11.2488&lon=75.7839&appid=${apiKey}`)
            const response = weather_info.then(response => {
                return response.json()
            })
            const new_data = await response.then()
//            console.log("data", new_data)
            this.state.value = new_data
            var date = new Date()
            this.state.date = date
//            console.log(this.state)

        }
    }



WeatherInfo.template = "systray_icon";
WeatherInfo.components = { Dropdown, DropdownItem };
export const systrayItem = {
   Component: WeatherInfo,
};

registry.category("systray").add("WeatherInfo", systrayItem, { sequence : 1} );