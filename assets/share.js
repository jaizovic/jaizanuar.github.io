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
    let copied = false;

    try {
      await navigator.clipboard.writeText(button.dataset.shareUrl);
      copied = true;
    } catch (_error) {
      const field = document.createElement('textarea');
      field.value = button.dataset.shareUrl;
      field.setAttribute('readonly', '');
      field.style.position = 'fixed';
      field.style.opacity = '0';
      document.body.appendChild(field);
      field.select();
      copied = document.execCommand('copy');
      field.remove();
    }

    button.classList.toggle('is-copied', copied);
    button.title = copied ? 'Link copied' : 'Copy article link';
    status.textContent = copied
      ? 'Article link copied to your clipboard.'
      : 'Select the address in your browser to copy this article link.';

    window.setTimeout(() => {
      button.classList.remove('is-copied');
      button.title = 'Copy article link';
      status.textContent = '';
    }, 3000);
  });
});
