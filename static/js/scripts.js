function loadMarketRates() {
    fetch("/get-market-rates/")
        .then(response => response.json())
        .then(data => {

            document.getElementById("goldPrice").innerText = "₹" + data.gold;
            document.getElementById("silverPrice").innerText = "₹" + data.silver;

            // Market Open / Close
            const hour = new Date().getHours();
            const marketStatus = document.getElementById("marketStatus");

            if (hour >= 9 && hour <= 17) {
                marketStatus.innerText = "OPEN";
                marketStatus.className = "fw-bold text-success ms-1";
            } else {
                marketStatus.innerText = "CLOSED";
                marketStatus.className = "fw-bold text-danger ms-1";
            }
        });
}

loadMarketRates();


document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.category-card');

    cards.forEach((card, index) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(30px)";

        setTimeout(() => {
            card.style.transition = "all 0.6s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, index * 200);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".input-group input").forEach(input => {
        input.setAttribute("required", "true");
    });
});



function createParticles() {
    const container = document.getElementById("gold-particles");

    for (let i = 0; i < 40; i++) {
        let particle = document.createElement("div");
        particle.classList.add("gold-particle");

        particle.style.left = Math.random() * 100 + "vw";
        particle.style.animationDuration = (5 + Math.random() * 10) + "s";
        particle.style.animationDelay = Math.random() * 5 + "s";
        particle.style.width = particle.style.height = 
            (3 + Math.random() * 6) + "px";

        container.appendChild(particle);
    }
}

createParticles();



fetch("/gold-chart/")
.then(res => res.json())
.then(data => {

const ctx = document.getElementById('goldChartCanvas').getContext('2d');

new Chart(ctx, {

type:'line',

data:{
labels:data.labels,

datasets:[{

label:'Gold Price ₹ / gram',

data:data.prices,

borderColor:'#FFD700',

backgroundColor:'rgba(255,215,0,0.2)',

borderWidth:3,

fill:true,

tension:0.4,

pointRadius:6,

pointBackgroundColor:'#ff9800'

}]
},

options:{

responsive:true,

animation:{
duration:2000,
easing:'easeInOutQuart'
},

plugins:{
legend:{
labels:{
color:'#fff'
}
}
},

scales:{

x:{
ticks:{
color:'#ddd'
}
},

y:{
ticks:{
color:'#ddd'
},
grid:{
color:'rgba(255,255,255,0.1)'
}
}

}

}

});

});
