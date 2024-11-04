import FirstEntryWindow from "./components/first_entry_window/FirstEntryWindow";
import '../../../../styles/main_window/Window.css';
import { Component } from "react";

class Window extends Component{

    constructor(props){
        super(props);
        this.userID = props.userID;
        this.isFirstEntryUser = Boolean(props.isFirstEntryUser);
    }

    render(){
        return (
            <div id="window">
                {this.#getWindow()}
            </div>
        );
    }

    #getWindow(){

        if(this.isFirstEntryUser === true){
            return <FirstEntryWindow />
        }

        return <></> 
    }
}

export default Window;