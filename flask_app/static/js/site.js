// console.log("js file!")
var breedName = ""

// get user input breed name
const setBreedName = (event) =>{
    breedName = event.value
}

function show_all_breed(){
    // send request to fetch data
    fetch("https://api.thecatapi.com/v1/breeds/")
        .then(response => response.json())
        .then(data => {
            breed_html = []
            // iterate all data and access all breed name, push all name with p tag into breed_html
            for (let i = 0; i < data.length; i++ ){
                var html = `<p> ${i + 1}: ${data[i].name} </p>`
                breed_html.push(html)
            }
            // display all breed
            document.getElementById("display").innerHTML = breed_html.join("")
        })
        .catch(err => console.log(err))
}

function get_breed_info() {
    fetch("https://api.thecatapi.com/v1/breeds/")
        .then(response => response.json())
        .then(data => {
            // store all breed info for specific breed
            breed_info_html = []
            // iterate all data we fetched
            for (let i = 0; i < data.length; i++) {
                // when we read single breed(user input), access the attributes we need, push them into breed_info_html
                if (data[i].name == breedName){
                    var html = `
                        <img src = ${data[i].image.url} alt="${data[i].name}'s image" width="280" height="230">
                        <div style="width:750px">
                            <p style="color:darkolivegreen;font-weight:bold;"> Description: ${data[i].description} </p>
                        </div>
                        <p> Temperament: ${data[i].temperament} </p>
                    `
                    breed_info_html.push(html)
                    // display specific breed info
                    document.getElementById("display_info").innerHTML = breed_info_html

                    var myChart = echarts.init(document.getElementById('main'));

                    // specify chart configuration item and data
                    option = {
                        xAxis: {
                            max: 'dataMax',
                        },
                        yAxis: {
                            data: ["Child Friendly", "Dog Friendly", "Stranger Friendly", "Energy", "Health Issue", "Intelligence", "Social Needs"],
                            inverse: true,
                            axisLabel: { interval: 0, rotate: 45 },
                            animationDuration: 300,
                            animationDurationUpdate: 300,
                            max: 6
                        },
                        series: [{
                            realtimeSort: true,
                            name: 'Level',
                            type: 'bar',
                            data: [data[i].child_friendly, data[i].dog_friendly, data[i].stranger_friendly, data[i].energy_level, data[i].health_issues, data[i].intelligence, data[i].social_needs],
                            label: {
                                show: true,
                                position: 'right',
                                valueAnimation: true
                            }
                        }],
                        legend: {
                            data: ['Level'],
                            top: 20,
                            right: 10
                        },
                        animationDuration: 0,
                        animationDurationUpdate: 3000,
                        animationEasing: 'linear',
                        animationEasingUpdate: 'linear'
                    };
                    // use configuration item and data specified to show chart
                    myChart.setOption(option);
                }
            }
        })
        .catch(err => console.log(err))
}
