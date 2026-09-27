(function () {
  var pageUrl = window.location.href.split('#')[0];
  var shareText = 'Check out the Sound Electronics product brochure: ' + pageUrl;
  var shareHref = 'https://wa.me/?text=' + encodeURIComponent(shareText);
  ['whatsappShareBtn', 'whatsappShareBtn2'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) el.setAttribute('href', shareHref);
  });

  var menuToggle = document.getElementById('menuToggle');
  var navDrawer = document.getElementById('navDrawer');

  menuToggle.addEventListener('click', function () {
    navDrawer.classList.toggle('open');
  });

  navDrawer.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () {
      navDrawer.classList.remove('open');
    });
  });

  var backToTop = document.getElementById('backToTop');
  window.addEventListener('scroll', function () {
    if (window.scrollY > 500) {
      backToTop.classList.add('show');
    } else {
      backToTop.classList.remove('show');
    }
  });
  backToTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();
