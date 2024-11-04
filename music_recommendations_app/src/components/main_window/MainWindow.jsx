import {Window, Player, Sidebar} from './components/components';
import '../../styles/main_window/MainWindow.css';
import {Circle} from '../Circle'; 

export function MainWindow(){

    let urlParams = new URLSearchParams(window.location.search);
    let params = {};

    urlParams.forEach((p, key) => {
        params[key] = p;
    });
 
    let userID = params['userID'];
    let isFirstEntry = params['isFirstEntry'];

    console.log(userID);
    console.log(isFirstEntry);

    return (
        <div id='main-window'>
            <Sidebar />
            <section id='window-and-player'>
                <Window userID={userID} isFirstEntryUser={isFirstEntry} />
                <Player />
            </section>

            {/* Левый нижний угол */}
            <Circle size='54px' zIndex='1' margin='81vh 0 0 19.5%' />

            {/* Правый нижний угол */}
            <Circle size='100px' zIndex='1' margin='81vh 0 0 90%' />
            <Circle size='100px' zIndex='1' margin='77vh 0 0 95%' />

            {/* Правый верхний угол */}
            <Circle size='100px' zIndex='1' margin='8vh 0 0 98%' />
            <Circle size='201px' zIndex='1' margin='-15vh 0 0 92%' />
            <Circle size='56px' zIndex='1' margin='-4vh 0 0 89.5%' />
        </div>
    )
}