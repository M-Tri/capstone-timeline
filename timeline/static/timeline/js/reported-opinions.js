
document.addEventListener('DOMContentLoaded', function() {
  const buttons = document.querySelectorAll('.remove-reported-button');
  // Remove opinion
  buttons.forEach(button => {
    button.addEventListener("click", function (e) {
      const opinionId = this.dataset.opinionId;
      const parent_container = this.closest('.remove-reported-opinion-id');
      delete_opinion(opinionId, parent_container);
    });
  });
});


function delete_opinion(opinion_id, container) {
  // Add animation class
  if (container) {
    container.style.animationPlayState = 'running';

    // Delete post from the browser
    container.addEventListener('animationend', function() {
      container.remove(); 
    },{ once: true });
  }

  // Delete from the backend
  const csrftoken = getCookie('csrftoken');
  fetch('/delete/opinion/' + opinion_id + '/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
    }
    //...
  });
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}