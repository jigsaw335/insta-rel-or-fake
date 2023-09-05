document.addEventListener('DOMContentLoaded', function() {
  const button = document.querySelector('.rectangle1-button');
  button.addEventListener('click', async function() {
    const loadingIndicator = document.querySelector('.loading');
    loadingIndicator.style.display = 'inline-block';

    const username = document.querySelector('input[name="username"]').value;
    const response = await fetch('/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username: username }),
    });

    loadingIndicator.style.display = 'none'; // Hide loading indicator

    const data = await response.json();
    console.log(data)
    if (data.error === 'Invalid username') {
      const resultContainer = document.querySelector('.result-container');
      resultContainer.innerHTML = `<p class="result-error">The account does not exist or is private.</p>`;
    } else {
      const result = data.result;
      const probability = data.probability;

      const resultText = document.createElement('p');
      resultText.textContent = `Result: ${result} (${probability}% probability)`;

      // Remove previous result if it exists
      const previousResult = document.querySelector('.result-container p');
      if (previousResult) {
        previousResult.remove();
      }

      resultText.classList.add('result');
      const resultContainer = document.querySelector('.result-container');
      resultContainer.appendChild(resultText);
    }
  });
});
