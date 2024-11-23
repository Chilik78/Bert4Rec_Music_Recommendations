import {Window, Player, Sidebar} from './components/components';
import '../../styles/main_window/MainWindow.css';
import {Circle} from '../Circle'; 
import DI from '../../scripts/backend/di';
import { useState, useEffect } from 'react';

export function MainWindow(){

    const [state, setState] = useState({userID: undefined, isFirstEntry: undefined});

    const getRandomKey = (max) => {
        return Math.floor(Math.random() * max);
    }

    const getCircles = () => {
        return <>
                {/* Левый нижний угол */}
                {state.isFirstEntry ? <></> : <Circle size='54px' zIndex='1' margin='81vh 0 0 19.5%' />}

                {/* Правый нижний угол */}
                {state.isFirstEntry ? <></> : <Circle size='100px' zIndex='1' margin='81vh 0 0 90%' />}
                {state.isFirstEntry ? <></> : <Circle size='100px' zIndex='1' margin='77vh 0 0 95%' />}

                {/* Правый верхний угол */}
                <Circle size='100px' zIndex='1' margin='8vh 0 0 98%' />
                <Circle size='201px' zIndex='1' margin='-15vh 0 0 92%' />
                <Circle size='56px' zIndex='1' margin='-4vh 0 0 89.5%' />
              </>
    };

    const activatePlayer = () => {
        setState({userID: state.userID, isFirstEntry: false});
    };

    useEffect(() => {
        const getUserInfo = () => {
            let urlParams = new URLSearchParams(window.location.search);
            let params = {};
        
            urlParams.forEach((p, key) => {
                params[key] = p;
            });
         
            let _userID = params['userID'];
            let _isFirstEntry = params['isFirstEntry'];
        
            console.log(_userID);
            console.log(_isFirstEntry);
    
            setState({userID: _userID, isFirstEntry: _isFirstEntry});
        };

        getUserInfo();
    }, []);

    return (
        <div id='main-window'>
            <Sidebar />
            <section id='window-and-player'>
                <Window key={getRandomKey(1000000)} userID={state.userID} isFirstEntryUser={state.isFirstEntry} activatePlayerFunc = {activatePlayer}/>
                {state.isFirstEntry ? <></> : <Player key={getRandomKey(1000000)} musicApi={DI.musicApi}/>}
            </section>

            {getCircles()}
        </div>
    );
}