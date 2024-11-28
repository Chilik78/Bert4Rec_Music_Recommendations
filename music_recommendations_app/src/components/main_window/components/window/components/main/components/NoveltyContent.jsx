import PlaylistItem from "./components/PlaylistItem";
import { useState, useEffect } from "react";
import FRANZ from "../../../../../../../assets/images/main/FRANZ.jpg";

export default function NoveltyContent() {

    const [noveltyPlaylist, setNoveltyPlaylist] = useState([]);

    const getNoveltyPlaylist = async () => {
        const playlists = [
            {
                img: FRANZ,
                title: "Новинки недели",
                authors: ["Franz Ferdinand", "Billiy Idol", "Artic Monleys"],
            },
        ];

        setNoveltyPlaylist(playlists);
    };

    useEffect(() => {
        getNoveltyPlaylist();
    }, []);

    return (
        <>
            {
                noveltyPlaylist.map((info, idx) => 
                    <PlaylistItem 
                    key={idx}
                    img={info.img} 
                    title={info.title} 
                    authors={info.authors} 
                    /> 
                )
            }
        </> 
    );
};