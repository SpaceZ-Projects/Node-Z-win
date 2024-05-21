Node-Z
======

## About the Project :

Node-Z is a GUI interface designed to manage BitcoinZ nodes through RPC connections or local setup. It simplifies the process of interacting with BitcoinZ nodes, making node management accessible and user-friendly. Key features include:

- Easy setup and configuration of local BitcoinZ nodes.
- Remote management of BitcoinZ nodes via RPC.
- Real-time monitoring and status updates.
- User-friendly interface for node operations.

## Getting Started :

### Requirements :
Python 3.8 or higher

### DEV Mode 
Create and activate a virtual environment :
```
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```
Install BeeWare tools :
pip install briefcase

<style>
.copy-btn {
    position: relative;
    display: inline-block;
    cursor: pointer;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    padding: 8px 12px;
    transition: background-color 0.3s;
}

.copy-btn:hover {
    background-color: #0056b3;
}

.copy-message {
    position: absolute;
    bottom: -30px;
    left: 50%;
    transform: translateX(-50%);
    background-color: rgba(0, 0, 0, 0.8);
    color: #fff;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 14px;
    display: none;
}
</style>

<!-- Copy Button HTML -->
<div>
    <pre>
        <code id="copy-text">
            <!-- Your command or text to copy -->
            python -m venv env
            source env/bin/activate  # On Windows, use `env\Scripts\activate`
            pip install briefcase
        </code>
    </pre>
    <button class="copy-btn" onclick="copyToClipboard()">Copy</button>
    <span class="copy-message" id="copy-message">Copied!</span>
</div>

<!-- Copy Button JavaScript -->
<script>
function copyToClipboard() {
    var copyText = document.getElementById("copy-text");
    var textarea = document.createElement("textarea");
    textarea.value = copyText.textContent;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
    var copyMessage = document.getElementById("copy-message");
    copyMessage.style.display = "block";
    setTimeout(function() {
        copyMessage.style.display = "none";
    }, 1500);
}
</script>
