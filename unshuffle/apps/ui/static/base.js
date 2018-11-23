function preventDoubleSubmissions() {
  document.querySelectorAll('form').forEach(function(form) {
    form.addEventListener('submit', function() {
      form.classList.add('submitted');
      form.querySelectorAll('[type=submit]').forEach(function(button) {
        button.setAttribute('disabled', 'true');
      });
    });
  });
}

window.addEventListener('load', function() {
  preventDoubleSubmissions();
});
