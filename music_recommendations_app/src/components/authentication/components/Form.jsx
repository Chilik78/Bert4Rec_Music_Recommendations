import logo from '../../../assets/images/logo.png';
import errorLoadingLogo from '../../../assets/images/error_load.png';
import '../../../styles/authentication/Form.css';
import { Component } from 'react';
import { Circle } from '../../Circle';
import { Link } from 'react-router-dom';

class Form extends Component{

    constructor(props){
        super(props);
        this.className = this.props.className;
        this.inputsInfo = this.props.inputsInfo;

        this.state = {
            isChooseTel: false,
            lastClickChooseId: 'btn-email',
        };

        this.SwitchChooseEntry = this.#SwitchChooseEntry.bind(this);
    }

    render(){
        return (
            <>
                {this.#getArrowBack()}
                <form className={this.className}>
                    <img src={logo} alt={errorLoadingLogo}></img>
                    <h1>{this.#getHeadingText()}</h1>
                    {this.#getChooseEntry()}
                    <section id='inputs-form'>
                        {this.inputsInfo.map((info) => this.#getInputForm(this.className, info))}
                    </section>
                    <Link to="/main" id='btn-authentication' style={{padding: this.#getPaddingAuthButton()}}>{this.#getTextAuthenticationBtn()}</Link>
                    {this.#getTextForReg()}
                </form>

                {this.#getCircles()}
            </>
            
        );
    }

    #getArrowBack(){
        if(this.className === 'registration')
            return (
                <Link to="/">
                    <svg id='arrow-back' xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z"/>
                    </svg>
                </Link>
            )
    }

    #getHeadingText(){
        return this.className === 'entry' ? "Вход" : "Регистрация";
    }

    #getChooseEntry(){
        if(this.className === 'entry')
            return (
                <section id='choose-input-type-container'>
                    <button id={'btn-email'} type='button' className='choose-input-type-btn' autoFocus={true} onClick={this.SwitchChooseEntry}>Почта</button>
                    <button id={'btn-tel'} type='button' className='choose-input-type-btn' onClick={this.SwitchChooseEntry}>Телефон</button>
                </section>
            );
    }

    #SwitchChooseEntry(e){
        if(this.state.lastClickChooseId !== e.target.id)
            this.setState({isChooseTel: !this.state.isChooseTel, lastClickChooseId: e.target.id});
    }

    #getInputForm(className, info){

        if(className === 'entry' && info.type === 'tel' && this.state.isChooseTel === true)
            return <input className='input-form' type={info.type} placeholder={info.hintText} />
        else if(className === 'entry' && info.type !== 'tel' && this.state.isChooseTel === false)
            return <input className='input-form' type={info.type} placeholder={info.hintText} />
        else if(className !== 'entry')
            return <input key={info.id} className='input-form' type={info.type} placeholder={info.hintText} />
    }

    #getTextAuthenticationBtn(){
        return this.className === 'entry' ? "Войти" : "Зарегистрироваться";
    }

    #getTextForReg(){
        if(this.className === 'entry')
            return (
                <section id='text-for-reg'>
                    <p>Не зарегистрированы?</p>
                    <Link to="/reg" id='clickable-text-for-reg'>Зарегистрироваться</Link>
                    {/* <button id={'btn-reg'} type='button'>Зарегистрироваться</button> */}
                </section>
            );
    }

    #getPaddingAuthButton(){
        return this.className === 'entry' ? ".5em 2em .5em 2em" : ".5em 1.2em .5em 1.2em";
    }

    #getCircles(){
        if(this.className === 'entry')
            return (
                <>
                    {/* Левый верхний угол формы */}
                    <Circle size='100px' zIndex='-1' margin='21vh 0 0 39%'/>
                    <Circle size='49px' zIndex='-1' margin='32vh 0 0 38.8%'/>
                    <Circle size='26px' zIndex='-1' margin='23vh 0 0 45%'/>


                    {/* Правый верхний угол формы */}
                    <Circle size='100px' zIndex='-1' margin='32vh 0 0 56.5%'/>

                    {/* Левый нижний угол формы */}
                    <Circle size='100px' zIndex='-1' margin='69vh 0 0 38.8%'/>

                    {/* Правый нижний угол формы */}
                    <Circle size='49px' zIndex='-1' margin='74vh 0 0 57.6%'/>
                    <Circle size='26px' zIndex='-1' margin='79vh 0 0 56.8%'/>
                </>
            );

        return (
            <>
                {/* Левый верхний угол формы */}
                <Circle size='100px' zIndex='-1' margin='26vh 0 0 37.5%'/>
                <Circle size='100px' zIndex='-1' margin='35vh 0 0 38.6%'/>
                <Circle size='26px' zIndex='-1' margin='24vh 0 0 41%'/>

                {/* Правый верхний угол формы */}
                <Circle size='100px' zIndex='-1' margin='19vh 0 0 48%'/>
                <Circle size='100px' zIndex='-1' margin='30vh 0 0 56.5%'/>

                {/* Середина правой стороны */}
                <Circle size='100px' zIndex='-1' margin='52vh 0 0 56%'/>
                <Circle size='49px' zIndex='-1' margin='63vh 0 0 58%'/>

                {/* Левый нижний угол формы */}
                <Circle size='49px' zIndex='-1' margin='83vh 0 0 38.6%'/>
                <Circle size='49px' zIndex='-1' margin='86vh 0 0 40.6%'/>

                {/* Правый нижний угол формы */}
                <Circle size='26px' zIndex='-1' margin='90vh 0 0 54%'/>
                <Circle size='26px' zIndex='-1' margin='89vh 0 0 55.6%'/>
            </>
        )
    }
}

export default Form;