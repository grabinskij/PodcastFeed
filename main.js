function copyToClipboard() {
  const url = document.getElementById('rss-link').href;
  
  const tempInput = document.createElement('input');
  tempInput.value = url;
  document.body.appendChild(tempInput);
  
  tempInput.select();
  document.execCommand('copy');
  document.body.removeChild(tempInput);
}