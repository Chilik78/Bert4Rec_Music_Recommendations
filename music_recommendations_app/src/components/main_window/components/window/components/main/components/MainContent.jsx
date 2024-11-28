import PlaylistItem from "./components/PlaylistItem";
import { useState, useEffect } from "react";

import FRANZ from "../../../../../../../assets/images/main/FRANZ.jpg";
import STARSET from "../../../../../../../assets/images/main/STARSET.jpg";

function MainContent() {

    const [mainPlaylist, setMainPlaylists] = useState([]);

    const getMainPlaylists = async () => {
        const playlists = [
            {
                img: FRANZ,
                title: "Сегодняшний плейлист",
                authors: ["Franz Ferdinand", "Billy Idol", "Artic Monleys", "STARSET", "The Anix"],
            },
            {
                img: STARSET,
                title: "Сегодняшний плейлист",
                authors: ["STARSET", "The Anix", "Euringer"],
            },
        ];

        setMainPlaylists(playlists);
    };

    useEffect(() => {
        getMainPlaylists();
    }, []);


    return ( 
        <section id='main-section'>
            <h1 id='main-header'>Главное</h1>
            <section>
                {
                    mainPlaylist.map((info, idx) => 
                        <PlaylistItem 
                            key={idx}
                            num={idx + 1}
                            img={info.img} 
                            title={info.title} 
                            authors={info.authors} 
                        /> 
                    )
                }
            </section>
        </section>
    );
}

export default MainContent;