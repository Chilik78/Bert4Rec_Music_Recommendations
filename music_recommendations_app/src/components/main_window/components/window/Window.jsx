import FirstEntryWindow from "./components/first_entry_window/FirstEntryWindow";
import Main from "./components/main/Main";
import Radio from "./components/radio/Radio";
import '../../../../styles/main_window/Window.css';
import { Component } from "react";
import DI from "../../../../scripts/backend/di";
import { WindowsType } from "../WindowsType";

class Window extends Component{

    constructor(props){
        super(props);
        this.userID = props.userID;
        this.windowType = props.windowType; 
        this.changeWindowFunc = props.changeWindowFunc;
        this.activatePlayerFunc = props.activatePlayerFunc;
        this.updateStateFromFirstEntryUser = this.#updateStateFromFirstEntryUser.bind(this);
    }

    
    render(){
        return (
            <div id="window" style={this.windowType === WindowsType.FirstEntryWindow ? {height: "100vh"} : {}}>
                {this.#getWindow()}
            </div>
        );
    }

    #getWindow(){

        switch(this.windowType){
            case WindowsType.FirstEntryWindow: return <FirstEntryWindow musicApi={DI.musicApi} funcOnDone={this.updateStateFromFirstEntryUser}/>
            case WindowsType.Main: return <Main />
            case WindowsType.Radio: return <Radio />
            default: return <></> 
        }
    }

    #updateStateFromFirstEntryUser(){
        this.changeWindowFunc(WindowsType.Main);
    }
}

export default Window;