import { Component } from "react";

class GenreButton extends Component{
    
    constructor(props){
        super(props);
        this.logo = props.logo;
        this.name = props.name;

        this.СhangeChoiceBtn = this.#СhangeChoiceBtn.bind(this);

        this.state = {
            isChoise: false
        }
    }

    render(){
        return (
            <div className={this.#getClassName()} onClick={this.СhangeChoiceBtn}>
                {this.logo}
                <h2>{this.name}</h2>
            </div>
        );
    }

    #СhangeChoiceBtn(){
        this.setState({isChoise: !this.state.isChoise});
    }

    #getClassName(){
        if(this.state.isChoise === false){
            return "genre-btn";
        }
        return "genre-btn-selected";
    }
}

export default GenreButton;