import SearchMusic from "../../SearchMusic";
import ChartContent from "./components/ChartContent";
import MainContent from "./components/MainContent";
import NoveltyContent from "./components/NoveltyContent";


export default function Main() {
    return ( 
        <div id="main">
            
            <section>
                <SearchMusic />
                <MainContent />
            </section>
            
            <section>
                <h2>Новинки</h2>
                <section id="novelty-playlists">
                    <NoveltyContent />
                </section>
            </section>
            

            <section>
                <h2>Чарт</h2>
                <ChartContent />
            </section>
        </div>
    );
}