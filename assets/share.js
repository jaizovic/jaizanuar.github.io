document.querySelectorAll('.share-link').forEach((link) => {
  link.addEventListener('click', (event) => {
    if (window.innerWidth <= 700) return;

    event.preventDefault();
    window.open(
      link.href,
      'article-share',
      'popup=yes,width=720,height=620,noopener,noreferrer'
    );
  });
});

document.querySelectorAll('.share-copy').forEach((button) => {
  button.addEventListener('click', async () => {
    const panel = button.closest('.article-share');
    const status = panel.querySelector('.share-status');

    try {
      await navigator.clipboard.writeText(button.dataset.shareUrl);
      button.textContent = 'Copied';
      status.textContent = 'Article link copied to your clipboard.';
    } catch (_error) {
      const field = document.createElement('textarea');
      field.value = button.dataset.shareUrl;
      field.setAttribute('readonly', '');
      field.style.position = 'fixed';
      field.style.opacity = '0';
      document.body.appendChild(field);
      field.select();
      const copied = document.execCommand('copy');
      field.remove();

      button.textContent = copied ? 'Copied' : 'Copy failed';
      status.textContent = copied
        ? 'Article link copied to your clipboard.'
        : 'Select the address in your browser to copy this article link.';
    }

    window.setTimeout(() => {
      button.textContent = 'Copy link';
      status.textContent = '';
    }, 3000);
  });
});
