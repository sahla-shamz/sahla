/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, onWillStart,} from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { useService } from "@web/core/utils/hooks";




export class WeatherInfo extends Component {
    setup(){
//    console.log("this", this)
    this.orm = useService("orm")
    this.state = useState( {value : [], date : "", tdate : "", img : ""})


     onWillStart(async () => {
            await this.weather_info();
        });
    }

    async weather_info()
    {
        console.log(this, "thissssssssss")
        var company_state = await this.orm.call('res.company', 'get_location_details', [], {})
        console.log("weather")
//        console.log(company_state)

            var lat = "11.2488"
            var lon = "75.7839"
            var apiKey = "9179ea68b5b998972a330d3ecb51e3d6"
//            const weather_info = fetch(`https://api.openweathermap.org/data/2.5/weather?lat=11.2488&lon=75.7839&appid=${apiKey}`)
            const weather_info = fetch(`https://api.openweathermap.org/data/2.5/weather?q=${company_state}&appid=${apiKey}&units=metric`)

            const response = weather_info.then(response => {
                return response.json()
            })
            const new_data = await response.then()
            console.log("data", new_data)
            this.state.value = new_data
            var date = new Date()
            var tdate = date.toISOString().split('T')[0]
            this.state.tdate = tdate
            this.state.date = date
            this.state.img = `https://openweathermap.org/payload/api/media/file/${this.state.value.weather[0].icon}.png`
//            this.state.img = `https://openweathermap.org/payload/api/media/file/10d.png`
            var icon= this.state.value.weather[0].icon
            console.log(icon)

            console.log(this.state.img)


        }
    }



WeatherInfo.template = "systray_icon";
WeatherInfo.components = { Dropdown, DropdownItem };
export const systrayItem = {
   Component: WeatherInfo,
};

registry.category("systray").add("WeatherInfo", systrayItem, { sequence : 1} );