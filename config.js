window.ITSUNARA_API = 'https://script.google.com/macros/s/AKfycbwt_JHyuElbah-a0gaTcM7_D7b803AleRauZjSTnKSeYJ92yw0JncUYEcgIVE20pDnosA/exec';

// 相手が自分のGoogleカレンダーに入れるためのURL（ログイン先の本人のカレンダーで開く）
window.gcalUrl = function (title, startIso, endIso, details, location) {
  function f(iso) {
    var d = new Date(iso);
    if (isNaN(d)) return '';
    return d.toLocaleString('sv-SE', { timeZone: 'Asia/Tokyo' }).replace(/[-: ]/g, '').replace(/^(\d{8})(\d{6})$/, '$1T$2');
  }
  var a = f(startIso), b = f(endIso);
  if (!a || !b) return '';
  return 'https://calendar.google.com/calendar/render?action=TEMPLATE&ctz=Asia/Tokyo'
    + '&text=' + encodeURIComponent(title) + '&dates=' + a + '/' + b
    + (details ? '&details=' + encodeURIComponent(details) : '')
    + (location ? '&location=' + encodeURIComponent(location) : '');
};
