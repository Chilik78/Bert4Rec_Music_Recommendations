import { useState, useEffect } from "react";
import ChartItem from "./components/ChartItem";

import BilleEilish from "../../../../../../../assets/images/main/BillieEilish.jpg"
import FRANZ from "../../../../../../../assets/images/main/FRANZ.jpg";
import STARSET from "../../../../../../../assets/images/main/STARSET.jpg";
import DepecheMode from "../../../../../../../assets/images/main/DepecheMode.jpg";

export default function ChartContent() {

    const [chartItemInfo, setChartItemInfo] = useState([]);

    const getChart = async () => {
        const musicsForChart = [
            {
                img: DepecheMode,
                title: "Ghosts Again",
                author: "Depeche Mode",
            },
            {
                img: FRANZ,
                title: "Take Me Out",
                author: "Franz Ferdinand",
            },
            {
                img: STARSET,
                title: "DIE FOR YOU",
                author: "STARSET",
            },
            {
                img: BilleEilish,
                title: "Bury a friend",
                author: "Billie Eilish",
            },
            {
                img: BilleEilish,
                title: "Bury a friend",
                author: "Billie Eilish",
            },
            {
                img: BilleEilish,
                title: "Bury a friend",
                author: "Billie Eilish",
            },
            {
                img: BilleEilish,
                title: "Bury a friend",
                author: "Billie Eilish",
            },
            {
                img: BilleEilish,
                title: "Bury a friend",
                author: "Billie Eilish",
            },
            {
                img: BilleEilish,
                title: "Bury a friend",
                author: "Billie Eilish",
            },
        ];

        setChartItemInfo(musicsForChart);
    };

    useEffect(() => {
        getChart();
    }, []);

    return ( 
        <section id="chart">
            {
                chartItemInfo.map((info, idx) => 
                <ChartItem 
                num={idx + 1}
                title={info.title}
                img={info.img}
                author={info.author}
                />
            )
            }        
        </section>
    );
};