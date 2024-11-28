import SearchMusic from "../../SearchMusic";
import RadioContent from "./components/RadioContent";

export default function Radio() {
    return ( 
        <div id="radio">
            <section>
                <SearchMusic />
                <RadioContent />
            </section>
            
            <h2>Жанры</h2>
        </div>
    );
}