// --- SAMPLE FORM BUTTON ---
document.getElementById('useSample').addEventListener('click', async () => {
  alert('Server will use the sample form (examples/sample_form.html). Click Generate.');
});

// --- GENERATE BUTTON ---
document.getElementById('generate').addEventListener('click', async () => {
  const html = document.getElementById('html_text').value;
  const fd = new FormData();
  fd.append('html_text', html);

  const output = document.getElementById('output');
  output.textContent = "Generating test cases... ";

  const resp = await fetch('/generate', { method: 'POST', body: fd });
  const json = await resp.json();

  const jsonString = JSON.stringify(json, null, 2);
  output.textContent = jsonString;
  Prism.highlightElement(output);

  // Summary bar
  document.getElementById('summary').classList.remove('hidden');
  document.getElementById('fieldSummary').textContent =
    `Fields Detected: ${json.fields.length} | Test Cases Generated: ${json.test_cases.length}`;

  // Store for copy/download
  window.generatedJSON = jsonString;
});

// --- COPY JSON ---
document.getElementById('copyOutput').addEventListener('click', () => {
  if (!window.generatedJSON) return alert("No JSON to copy yet!");
  navigator.clipboard.writeText(window.generatedJSON);
  alert(" JSON copied to clipboard!");
});

// --- DOWNLOAD JSON ---
document.getElementById('downloadJSON').addEventListener('click', () => {
  if (!window.generatedJSON) return alert("No JSON to download yet!");
  const blob = new Blob([window.generatedJSON], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "testcases_output.json";
  link.click();
});
