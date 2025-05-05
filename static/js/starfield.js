const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');
let width = canvas.width = window.innerWidth;
let height = canvas.height = window.innerHeight;
const stars = [];
const numStars = 400;

function init() {
  for (let i = 0; i < numStars; i++) {
    stars.push({
      x: Math.random() * width,
      y: Math.random() * height,
      z: Math.random() * width,
      o: '0.' + Math.floor(Math.random() * 99) + 1
    });
  }
}

function animate() {
  ctx.fillStyle = "black";
  ctx.fillRect(0,0,width,height);

  for (let i = 0; i < numStars; i++) {
    let s = stars[i];
    let x = (s.x - width/2) * (width / s.z) + width/2;
    let y = (s.y - height/2) * (width / s.z) + height/2;
    let size = (1 - s.z/width) * 2;
    ctx.beginPath();
    ctx.fillStyle = "rgba(255,255,255,"+s.o+")";
    ctx.arc(x,y,size,0,Math.PI*2);
    ctx.fill();
    s.z -= 2;
    if (s.z <= 0) {
      s.z = width;
    }
  }
  requestAnimationFrame(animate);
}

window.onresize = function() {
  width = canvas.width = window.innerWidth;
  height = canvas.height = window.innerHeight;
};

init();
animate();