import '../../../../styles/main_window/Sidebar.css';
import logo from '../../../../assets/images/logo.png';
import errorLoadingLogo from '../../../../assets/images/error_load.png';
import { TabItem } from './components/TabItem';
import Avatar from './components/Avatar';
import { Component } from 'react';
import { WindowsType } from '../WindowsType';

class Sidebar extends Component{

    constructor(props){
        super(props);
        this.currentWindow = props.currentWindow;
        this.changeWindowFunc = props.changeWindowFunc;
        this.tabsInfo = [
            {
                key: 'main',
                logo:  <svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M6 13c0 1.105-1.12 2-2.5 2S1 14.105 1 13c0-1.104 1.12-2 2.5-2s2.5.896 2.5 2zm9-2c0 1.105-1.12 2-2.5 2s-2.5-.895-2.5-2 1.12-2 2.5-2 2.5.895 2.5 2z"/>
                            <path d="M14 11V2h1v9h-1zM6 3v10H5V3h1z"/>
                            <path d="M5 2.905a1 1 0 0 1 .9-.995l8-.8a1 1 0 0 1 1.1.995V3L5 4V2.905z"/>
                        </svg>,
                text: 'Главное',
            },
            {
                key: 'radio',
                logo:  <svg key='radio' xmlns="http://www.w3.org/2000/svg" width="19" height="19" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M3.05 3.05a7 7 0 0 0 0 9.9.5.5 0 0 1-.707.707 8 8 0 0 1 0-11.314.5.5 0 0 1 .707.707zm2.122 2.122a4 4 0 0 0 0 5.656.5.5 0 1 1-.708.708 5 5 0 0 1 0-7.072.5.5 0 0 1 .708.708zm5.656-.708a.5.5 0 0 1 .708 0 5 5 0 0 1 0 7.072.5.5 0 1 1-.708-.708 4 4 0 0 0 0-5.656.5.5 0 0 1 0-.708zm2.122-2.12a.5.5 0 0 1 .707 0 8 8 0 0 1 0 11.313.5.5 0 0 1-.707-.707 7 7 0 0 0 0-9.9.5.5 0 0 1 0-.707zM10 8a2 2 0 1 1-4 0 2 2 0 0 1 4 0z"/>
                       </svg>,
                text: 'Радио',
            },
        ];

        this.changeWindow = this.#changeWindow.bind(this);
    }

    render(){
        return (
            <div id="sidebar">
                <section>
                    <section id='heading'>
                        <img src={logo} alt={errorLoadingLogo}></img>
                        <h2>Музыкальный Гуру</h2>
                    </section>
    
                    <svg id='list-logo' xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5z"/>
                    </svg>
    
                    <section id='tabs'>
                        {this.tabsInfo.map((info) => <TabItem key={info.key} id={info.key} selected={this.#getSelected(info.key)} logo={info.logo} text={info.text} onClick={this.changeWindow}/>)}
                    </section>
                </section>
    
                <section>
                    <Avatar img = '' userName = 'Дмитрий Челядинов' />
                </section>
                
            </div>
        );
    }

    #getSelected(key){
        if(key.includes("main") && this.currentWindow === WindowsType.Main){
            return true;
        }
        else if(key.includes("radio") && this.currentWindow === WindowsType.Radio){
            return true;
        }

        return false;
    }

    #changeWindow(key){

        if(this.currentWindow === WindowsType.FirstEntryWindow){
            return;
        }
    
        if(key.includes("main") && this.currentWindow !== WindowsType.Main){
            this.changeWindowFunc(WindowsType.Main);
            return;
        }

        if(key.includes("radio") && this.currentWindow !== WindowsType.Radio){
            this.changeWindowFunc(WindowsType.Radio);
            return;
        }
    }
}

export default Sidebar;