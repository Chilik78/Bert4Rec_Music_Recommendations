import FirstEntryWindow from "./components/first_entry_window/FirstEntryWindow";
import '../../../../styles/main_window/Window.css';
import { Component } from "react";
import DI from "../../../../scripts/backend/di";

class Window extends Component{

    constructor(props){
        super(props);
        this.userID = props.userID;
        this.isFirstEntryUser = Boolean(props.isFirstEntryUser);
        this.activatePlayerFunc = props.activatePlayerFunc;
        this.updateStateFromFirstEntryUser = this.#updateStateFromFirstEntryUser.bind(this);
    }

    
    render(){
        return (
            <div id="window" style={this.isFirstEntryUser ? {height: "100vh"} : {}}>
                {this.#getWindow()}
            </div>
        );
    }

    #getWindow(){

        if(this.isFirstEntryUser === true){
            return <FirstEntryWindow musicApi={DI.musicApi} funcOnDone={this.updateStateFromFirstEntryUser}/>
        }

        return <></> 
    }

    #updateStateFromFirstEntryUser(){
        this.activatePlayerFunc();
    }
}

export default Window;