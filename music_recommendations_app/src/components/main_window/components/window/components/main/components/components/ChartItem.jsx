import { useState } from "react";

export default function ChartItem({num, img, title, author}) {

    const [state, setState] = useState({isHover: false});

    return ( 
        <div className="chart-item">
            <p className="chart-item-number">{num}</p>
            <section className="chart-item-content" onMouseEnter={() => setState({isHover: true})} onMouseLeave={() => setState({isHover: false})}>
                
                <div className="chart-item-img-and-play-icon">
                    <img className="chart-item-img" style={state.isHover ? {filter: "brightness(0.8)"} : {}} src={img} alt=""></img>

                    {   
                        state.isHover === true ? 
                        <svg className="chart-item-play-icon" xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                            <path d="M6.271 5.055a.5.5 0 0 1 .52.038l3.5 2.5a.5.5 0 0 1 0 .814l-3.5 2.5A.5.5 0 0 1 6 10.5v-5a.5.5 0 0 1 .271-.445z"/>
                        </svg>
                        : <></>
                    }
                </div>
                
                <section>
                    <p className="chart-item-title">{title}</p>
                    <p className="chart-item-author">{author}</p>
                </section>
            </section>  
        </div>
    );
};