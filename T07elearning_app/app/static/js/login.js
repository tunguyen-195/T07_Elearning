var design = anime({
  targets: "svg #XMLID5",
  keyframes: [
    { translateX: -500 },
    { rotateY: 180 },
    { translateX: 920 },
    { rotateY: 0 },
    { translateX: -500 },
    { rotateY: 180 },
    { translateX: -500 },
  ],
  easing: "easeInOutSine",
  duration: 60000,
});

anime({
  targets: "#dust-paarticle path",
  translateY: [10, -150],
  direction: "alternate",
  loop: true,
  delay: function (el, i, l) {
    return i * 100;
  },
  endDelay: function (el, i, l) {
    return (l - i) * 100;
  },
});

// Add click effect to login button
document.querySelector('.btn-primary').addEventListener('click', function(event) {
  console.log('Login button clicked');
  event.preventDefault(); // Prevent default to check if the event is triggered
  console.log('Form will be submitted');
  document.querySelector('form').submit(); // Manually submit the form
  anime({
    targets: '.btn-primary',
    scale: [1, 1.1, 1],
    duration: 500,
    easing: 'easeInOutQuad'
  });
});

// Add hover effect to social buttons
document.querySelectorAll('.social-buttons a').forEach(button => {
  button.addEventListener('mouseenter', function() {
    anime({
      targets: button,
      scale: 1.1,
      duration: 300,
      easing: 'easeInOutQuad'
    });
  });

  button.addEventListener('mouseleave', function() {
    anime({
      targets: button,
      scale: 1,
      duration: 300,
      easing: 'easeInOutQuad'
    });
  });
});
