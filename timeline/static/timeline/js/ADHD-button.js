let counter = 0;
let timer_id = 0;
const duration = 10;

function count() {
  counter++;
  let remaining = duration - counter;
  
  const adhdBtn = document.querySelector('#ADHD-button');
  adhdBtn.value = remaining;
  adhdBtn.textContent = remaining;

  // Reset when time is up
  if (counter >= duration) {
    clearInterval(timer_id);
    timer_id = 0;
    counter = 0;
    
    revert_color();
    
    // Re-enable all buttons
    adhdBtn.disabled = false;
    document.querySelector('#opinion-button').disabled = false;
    document.querySelector('#random-button').disabled = false;
  }
}

function change_color() {
  const adhdBtn = document.querySelector('#ADHD-button');
  adhdBtn.classList.remove("bg-danger");
  adhdBtn.classList.add("bg-success");
  adhdBtn.value = "ADHD ON";
  adhdBtn.textContent = "ADHD ON";
}

function revert_color() {
  const adhdBtn = document.querySelector('#ADHD-button');
  adhdBtn.classList.remove("bg-success");
  adhdBtn.classList.add("bg-danger");
  adhdBtn.value = "ADHD OFF";
  adhdBtn.textContent = "ADHD OFF";
}

function change_ADHD_state() {
  // 1. Guard clause: If timer is already running, ignore the click
  if (timer_id !== 0) {
    return;
  }

  const adhdBtn = document.querySelector('#ADHD-button');
  
  // 2. Disable the ADHD button itself to prevent further clicks
  adhdBtn.disabled = true;

  // Disable other buttons
  document.querySelector('#opinion-button').disabled = true;
  document.querySelector('#random-button').disabled = true;
  
  // Change color
  change_color();

  counter = 0;
  timer_id = setInterval(count, 1000);
}

// Start
document.addEventListener('DOMContentLoaded', function() {
  const btn_ADHD = document.querySelector('#ADHD-button');
  if (btn_ADHD) {
    btn_ADHD.onclick = change_ADHD_state;
  }
});