import { Component } from 'react';
// import errorLoadImg from '../../../../../assets/images/error_load.png';

class MusicInfo extends Component{

    constructor(props){
        super(props);
        this.name = props.name;
        this.author = props.author;
    }

    render(){
        return (
            <div id="music-info">
                <div id='music-info-img'></div>
                <section id="music-info-text">
                    <h1>{this.name}</h1>
                    <p>{this.author}</p>
                </section>
            </div>
        );
    }
}

export default MusicInfo;