import Player, {Sidebar, Window} from './components/components';
import '../../styles/main_window/MainWindow.css';
import {Circle} from '../Circle'; 

export function MainWindow(){
    return (
        <div id='main-window'>
            <Sidebar />
            <section id='window-and-player'>
                <Window />
                <Player />
            </section>

            {/* Левый нижний угол */}
            <Circle size='54px' zIndex='-1' margin='81vh 0 0 19.5%' />

            {/* Правый нижний угол */}
            <Circle size='100px' zIndex='-1' margin='81vh 0 0 90%' />
            <Circle size='100px' zIndex='-1' margin='77vh 0 0 95%' />

            {/* Правый верхний угол */}
            <Circle size='100px' zIndex='-1' margin='8vh 0 0 98%' />
            <Circle size='201px' zIndex='-1' margin='-15vh 0 0 92%' />
            <Circle size='56px' zIndex='-1' margin='-4vh 0 0 89.5%' />
        </div>
    )
}