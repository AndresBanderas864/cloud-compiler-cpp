const helloWorld = `#include <iostream>
using namespace std;

int main() {
  cout << "Hola, mundo!" << endl;
  return 0;
}`;

const code = document.querySelector('#code');
const lineNumbers = document.querySelector('#line-numbers');
const output = document.querySelector('#output');
const standard = document.querySelector('#standard');
const runButton = document.querySelector('#run');
const cancelButton = document.querySelector('#cancel');
const input = document.querySelector('#stdin');
const sendInput = document.querySelector('#send-input');
const runStatus = document.querySelector('#run-status');
const connectionStatus = document.querySelector('#connection-status');
let socket = null;

code.value = helloWorld;

function updateEditor() {
  const lines = code.value.split('\n').length;
  lineNumbers.textContent = Array.from({ length: lines }, (_, i) => i + 1).join('\n');
  document.querySelector('#char-count').textContent = `${code.value.length.toLocaleString('es-CO')} caracteres`;
}
function appendOutput(text, replace = false) {
  if (replace) output.textContent = '';
  output.textContent += text;
  output.scrollTop = output.scrollHeight;
}
function status(value) { runStatus.textContent = value; }
function setRunning(running) { runButton.disabled = running; cancelButton.disabled = !running; standard.disabled = running; runButton.textContent = running ? 'Ejecutando…' : '▶  Ejecutar código'; }
function sendStdin() { if (!socket || socket.readyState !== WebSocket.OPEN || !input.value) return; socket.send(JSON.stringify({ type:'stdin', value:input.value + '\n' })); appendOutput(`> ${input.value}\n`); input.value = ''; }

code.addEventListener('input', updateEditor);
code.addEventListener('scroll', () => { lineNumbers.scrollTop = code.scrollTop; });
input.addEventListener('keydown', (event) => { if (event.key === 'Enter') { event.preventDefault(); sendStdin(); } });
sendInput.addEventListener('click', sendStdin);
document.querySelector('#clear-output').addEventListener('click', () => { output.innerHTML = '<span class="terminal-placeholder">La salida del compilador aparecerá aquí.</span>'; });

runButton.addEventListener('click', () => {
  if (socket && socket.readyState === WebSocket.OPEN) return;
  output.textContent = '';
  setRunning(true); status('conectando'); connectionStatus.innerHTML = '<i></i> ejecutando';
  socket = new WebSocket(`${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/ws/run`);
  socket.onopen = () => { status('compilando'); socket.send(JSON.stringify({ type:'start', code:code.value, standard:standard.value })); };
  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.type === 'output') appendOutput(message.value);
    if (message.type === 'status') { status(message.value); if (['finalizado','error','cancelado','tiempo agotado','salida limitada'].includes(message.value)) setRunning(false); }
    if (message.type === 'error') { appendOutput(`[${message.error_id}] ${message.message}\n`); status('error'); setRunning(false); }
  };
  socket.onerror = () => { appendOutput('[CC-900] No se pudo conectar con el servicio.\n'); status('error'); setRunning(false); };
  socket.onclose = () => { connectionStatus.innerHTML = '<i></i> listo'; if (runButton.disabled) setRunning(false); };
});
cancelButton.addEventListener('click', () => { if (socket?.readyState === WebSocket.OPEN) socket.send(JSON.stringify({ type:'cancel' })); });
updateEditor();
