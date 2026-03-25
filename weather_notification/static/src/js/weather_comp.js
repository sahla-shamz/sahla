/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { useService } from "@web/core/utils/hooks";


export class WeatherInfo extends Component {

    setup(){
    this.orm = useService("orm")
    this.state = useState( {value : [], date : "", img : "", sunrise : "", sunset : ""})

     onWillStart(async () => {
            await this.weather_info();
        });
    }

    async weather_info()
    {
        var company_state = await this.orm.call('res.company', 'get_location_details', [], {})
        var lat = "11.2488"
        var lon = "75.7839"
        var apiKey = "9179ea68b5b998972a330d3ecb51e3d6"
        const weather_info =
            fetch(`https://api.openweathermap.org/data/2.5/weather?q=${company_state}&appid=${apiKey}&units=metric`)
        const response = weather_info.then(response => {
            return response.json()
        })
        const new_data = await response.then()

        this.state.value = new_data
        this.state.img = `https://openweathermap.org/payload/api/media/file/${this.state.value.weather[0].icon}.png`

        var dateObj = new Date((this.state.value.dt+this.state.value.timezone) *1000)
        var utcString = dateObj.toUTCString();
        this.state.date = utcString

        var sunriseObj = new Date((this.state.value.sys.sunrise + this.state.value.timezone) * 1000)
        var utcSunrise = sunriseObj.toUTCString();
        this.state.sunrise = utcSunrise.slice(17,25)

        var sunsetObj = new Date((this.state.value.sys.sunset + this.state.value.timezone) * 1000)
        var utcSunset = sunsetObj.toUTCString();
        this.state.sunset = utcSunset.slice(17,25)

        }
    }



WeatherInfo.template = "systray_icon";
WeatherInfo.components = { Dropdown, DropdownItem };
export const systrayItem = {
   Component: WeatherInfo,
};

registry.category("systray").add("WeatherInfo", systrayItem, { sequence : 100} );