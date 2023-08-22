
const widht = document.querySelector(".section2_cars_main"),
    leng = document.querySelectorAll(".section2_cars_main_divs .section2_cars_main_divs_car")
widht.style.width = `${leng.length / 3 * 1519}px`
let prev =document.getElementById('prev')
const next = document.querySelector(".section2_cars_main_next");
const rasm = document.querySelector(".section2_cars_main_divs");
let count = 0;

function ChangeImage() {
    if (count > leng.length - 3) {
        count = 0
    } else if (count < 0) {
        count = leng.length - 3
    }
    rasm.style.transform = ` translateX(${-count * 500}px)`
}

next.addEventListener("click", () => {
    count++;
    ChangeImage()
})
prev.addEventListener("click", () => {
    count--;
    ChangeImage()
})
let startX = 0;
rasm.addEventListener("mousedown", (e) => {
    startX = e.pageX;
});

rasm.addEventListener("mouseup", (e) => {
    const movementX = e.pageX - startX;
    if (movementX > 0) {
       count--;
    ChangeImage()
    } else {
      count++;
    ChangeImage()
    }
});