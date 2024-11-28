import { useState } from "react";

export default function PlaylistItem({num, img, title, authors}) {

    const [state, setState] = useState({isHover: false});

    const getAuthors = () => {
        return authors.join(", ");
    };
    
    return ( 
        <div className="playlist-item">
            <section onMouseEnter={() => setState({isHover: true})} onMouseLeave={() => setState({isHover: false})}>
                <img className="playlist-item-img" style={state.isHover ? {filter: "brightness(0.8)"} : {}} src={img} alt="" />
                
                {   state.isHover === true ? 
                    <svg className="playlist-item-play-icon" xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                        <path d="M6.271 5.055a.5.5 0 0 1 .52.038l3.5 2.5a.5.5 0 0 1 0 .814l-3.5 2.5A.5.5 0 0 1 6 10.5v-5a.5.5 0 0 1 .271-.445z"/>
                    </svg>
                    : <></>
                }
                
                {num === undefined ? <></> : <div style={state.isHover ? {filter: "brightness(0.8)"} : {}} className="mix-day">Умный микс #{num}</div>}
            </section>
            
            <p className="playlist-item-title">{title}</p>
            <p className="playlist-item-authors">{getAuthors()}</p>
        </div>
    );


};