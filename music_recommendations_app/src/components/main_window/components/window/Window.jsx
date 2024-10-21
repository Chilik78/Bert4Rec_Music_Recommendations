import FirstEntryWindow from "./components/first_entry_window/FirstEntryWindow";
import '../../../../styles/main_window/Window.css';
import { Component } from "react";
import { isFirstEntryUser } from "../../../../scripts/backend/user.js";

class Window extends Component{

    constructor(props){
        super(props);
        this.userID = props.userID;
    }

    render(){
        return (
            <div id="window">
                {this.#getWindow()}
            </div>
        );
    }

    #getWindow(){
        if(isFirstEntryUser(this.userID)){
            return <FirstEntryWindow />
        }

        return <></> 
    }
}

export default Window;