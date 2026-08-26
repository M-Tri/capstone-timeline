let counter = 0;
let timer_id = 0;
const duration = 10;
function count() {
  counter++;
  let remaining = duration - counter;
  document.querySelector('#ADHD-button').value = remaining;
  document.querySelector('#ADHD-button').textContent = remaining;
  // Reset
  if (counter >= duration) {
    clearInterval(timer_id)
    counter = 0;
    revert_color()
    document.querySelector('#opinion-button').disabled = false;
    document.querySelector('#random-button').disabled = false;
  }
};

function change_color() {
    document.querySelector('#ADHD-button').classList.remove("bg-danger");
    document.querySelector('#ADHD-button').classList.add("bg-success");
    document.querySelector('#ADHD-button').value = "ADHD ON";
    document.querySelector('#ADHD-button').textContent = "ADHD ON";
}

function revert_color() {
    document.querySelector('#ADHD-button').classList.remove("bg-success");
    document.querySelector('#ADHD-button').classList.add("bg-danger");
    document.querySelector('#ADHD-button').value = "ADHD";
    document.querySelector('#ADHD-button').textContent = "ADHD OFF";
}

function change_ADHD_state() {
  // disable buttons
  document.querySelector('#opinion-button').disabled = true;
  document.querySelector('#random-button').disabled = true;
  // Change change_color
  change_color();

  counter = 0;

  timer_id = setInterval(count, 1000);
};

// Start
document.addEventListener('DOMContentLoaded', function() {
  // ADHD button : card.html
  const btn_ADHD = document.querySelector('#ADHD-button');
  if (btn_ADHD) {
    btn_ADHD.onclick = change_ADHD_state;
  }
});
